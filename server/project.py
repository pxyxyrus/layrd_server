from server import db
from server.models import Project, Application
from server.types import ProjectStatus, ApplicationStatus
from server.util import *
import server.azure_helper as azure_helper
from sqlalchemy import func, or_
import json
from flask import (
    Blueprint, Response, make_response, flash, g, redirect, render_template, request, session, url_for
)
import server.firebase_helper as firebase_helper
from logger import logger



project_bp = Blueprint('project', __name__)



def change_project_status(request_data, status_to_change):
    with db.session.begin() as s:
        projects = s.query(Project).filter_by(id=request_data['id']).all()
        print(status_to_change)
        print(projects)
        for proj in projects:
            setattr(proj, "status", status_to_change)
    db.session.commit()



@project_bp.route('/upload', methods=['POST'])
def upload_project():
    logger.info("/project/upload")
    if request.method == 'POST':
        try:
            print(request.json['data'])
            request_data = request.json['data']
            request_auth_data = request.json['auth']
            user_info = firebase_helper.authenticate(request_auth_data)
            print(request_data)
            proj = Project(**request_data)
            print(proj)
            db.session.begin()
            if 'id' in request_data:
                # if there is an 'id' field passed we need to check if the status is saved or not
                # and if the current sender is the owner
                exist_proj = db.session.query(Project).filter(Project.id == request_data['id']).first()
                if exist_proj is not None:
                    if user_info['uid'] != exist_proj.owner_uid:
                        # TODO need to define better errors
                        return create_json_error_response({
                                'error_code': 'invalid_action_error',
                                'error_message': "not the owner of the project"
                            }, status_code=400)
                    elif exist_proj.status != ProjectStatus.saved.value:
                        # TODO need to define better errors
                        return create_json_error_response({
                            'error_code': 'invalid_project_status_error',
                            'error_message': "project status is not saved"
                        })

            db.session.add(proj)
        except Exception as e:
            logger.error(f"request_data : {json.dumps(request_data, indent=0)}")
            logger.exception(e)
            db.session.rollback()
            return create_json_error_response(e.args[0])
        else:
            db.session.commit()
            proj_id = proj.id
            recipients = [
                {
                    "address": user_info["email"],
                    "displayName": user_info["email"]
                }
            ]
            title = "Congratuation on your proposal!"
            body = render_template("email/project_submit.html", proposal_link=f"layrd.xyz/{proj_id}")
            azure_helper.send_email(title, recipients, body, body)

            # need to explicitly call session.close
            # because proj was accessed again for proj_id
            db.session.close() 

            return create_json_response('', status_code=201)



# @project_bp.route('/withdraw', methods=['POST'])
# def withdraw_project():
#     logger.info("/project/withdraw")
#     if request.method == 'POST':
#         request_data = request.json['data']
#         try:
#             change_project_status(request_data, ProjectStatus.withdrawn.value)
#             return create_json_response('', status_code=201)
#         except Exception as e:
#             logger.error(f"request_data : {json.dumps(request_data, indent=0)}")
#             logger.exception(e)
#             return create_json_error_response(e.args[0])
        



# @project_bp.route('/complete', methods=['POST'])
# def complete_project():
#     logger.info("/project/complete")
#     if request.method == 'POST':
#         request_data = request.json['data']
#         print(request_data)
#         try:
#             change_project_status(request_data, ProjectStatus.successful.value)
#             return create_json_response('', status_code=201)
#         except Exception as e:
#             logger.error(f"request_data : {json.dumps(request_data, indent=0)}")
#             logger.exception(e)
#             return create_json_error_response(e.args[0])

    

# @project_bp.route('/abort', methods=['POST'])
# def abort_project():
#     logger.info("/project/abort")
#     if request.method == 'POST':
#         request_data = request.json['data']
#         print(request_data)
#         try:
#             change_project_status(request_data, ProjectStatus.unsuccessful.value)
#             return create_json_response('', status_code=201)
#         except Exception as e:
#             logger.error(f"request_data : {json.dumps(request_data, indent=0)}")
#             logger.exception(e)
#             return create_json_error_response(e.args[0])




@project_bp.route('/<int:project_id>', methods=['GET'])
# expects a user firebase ID token
def get_project(project_id):
    logger.info(f"project/{project_id}")
    if request.method == 'GET':
        try:
            db.session.begin()
            projects = db.session.query(Project, func.count(Application.id).label('application_count'))\
                .outerjoin(Application, Project.id == Application.project_id)\
                .filter(Project.id == project_id)\
                .filter(Project.status != ProjectStatus.saved.value)\
                .group_by(Project.id)\
                .limit(25)\
                .all()
        except Exception as e:
            print(e)
            request_data = {"id": project_id}
            logger.error(f"request_data : {json.dumps({request_data}, indent=0)}")
            logger.exception(e)
            db.session.rollback()
            return create_json_error_response(e.args[0])
        else:
            response_data = []
            for p in projects:
                p = p._asdict()
                d = p["Project"].to_dict()
                d["application_count"] = p["application_count"]
                response_data.append(d)
            db.session.commit()
            return create_json_response(response_data)


# this api endpoint is being used both in main and user page, the condition project.status needs to be removed. And handle displaying saved and open projects.
@project_bp.route('/get_projects', methods=['POST'])
def get_projects():
    logger.info("/project/get_projects")
    if request.method == 'POST':
        try:
            request_data = request.json['data']
            db.session.begin()
            cursor = request_data.pop('cursor', None)
            projects = None
            request_data = { getattr(Project, key):value for key, value in request_data.items() }

            projects = db.session.query(Project, func.count(Application.id).label('application_count'))\
                .outerjoin(Application, Project.id == Application.project_id)\
                # .filter(Project.status != ProjectStatus.saved.value) ## Paul - maybe we can handle this in frontend?

            # if cursor was passed, apply the cursor condition first
            if cursor is not None:
                projects = projects.filter(Project.id > cursor)

            # now add conditions given by api call
            for key, value in request_data.items():
                projects = projects.filter(key == value)

            # group by and limit
            projects = projects.group_by(Project.id)\
                .limit(25)\
                .all()


        except Exception as e:
            logger.error(f"request_data : {json.dumps(request_data, indent=0)}")
            logger.exception(e)
            db.session.rollback()
            return create_json_error_response(e.args[0])
        else:
            response_data = []
            if projects is not None:
                for p in projects:
                    p = p._asdict()
                    d = p["Project"].to_dict()
                    d["application_count"] = p["application_count"]
                    response_data.append(d)
            db.session.commit()
            return create_json_response(response_data)
        


@project_bp.route('/select_application', methods=['POST'])
def select_application():
    logger.info("/project/select_application")
    if request.method == 'POST':
        try:
            request_data = request.json['data']
            request_auth_data = request.json['auth']
            user_info = firebase_helper.authenticate(request_auth_data)

            project_id = request_data['project_id']
            app_ids = request_data['ids']

            db.session.begin()
            project = db.session.query(Project)\
                .filter(Project.id == project_id)\
                .limit(25)\
                .first()
            
            if user_info['uid'] != project.owner_uid:
                # TODO need to define better errors
                return create_json_error_response({
                        'error_code': 'invalid_action_error',
                        'error_message': "not the owner of the project"
                    }, status_code=400)
            elif project.status != ProjectStatus.open.value:
                # TODO need to define better errors
                return create_json_error_response({
                    'error_code': 'invalid_project_status_error',
                    'error_message': "project status is not opened"
                })

            applications = db.session.query(Application)\
                .filter(Application.status == ApplicationStatus.applied.value)\
                .filter(or_(Application.id == id for id in app_ids))\
                .filter(Application.project_id == project.id)\
                .all()
            print(applications)


            for app in applications:
                app.status = ApplicationStatus.accepted.value

        except Exception as e:
            logger.error(f"request_data : {json.dumps(request_data, indent=0)}")
            logger.exception(e)
            db.session.rollback()
            return create_json_error_response(e.args[0], status_code=400)
        else:
            db.session.commit()
            
            recipients = []

            for app in applications:
                accepted_user_email = firebase_helper.get_user_email_from_uid(app.owner_uid)
                recipients.append(
                    {
                        "address": accepted_user_email,
                        "displayName": accepted_user_email
                    }
                )

            title = "Congratuation! your application is accepted."
            body = render_template("email/project_accept_application.html", project_name=project.title, accept_link="")
            azure_helper.send_email(title, recipients, body, body)

            # need to explicitly call session.close
            # because proj was accessed again for proj_id
            db.session.close()

            return create_json_response('', 201)



@project_bp.route('/start', methods=['POST'])
def start_project():
    logger.info("/project/start")
    if request.method == 'POST':
        try:
            request_data = request.json['data']
            request_auth_data = request.json['auth']
            user_info = firebase_helper.authenticate(request_auth_data)

            project_id = request_data['id']

            db.session.begin()
            project = db.session.query(Project)\
                .filter(Project.id==project_id)\
                .limit(25)\
                .first()
            
            if user_info['uid'] != project.owner_uid:
                # TODO need to define better errors
                return create_json_error_response({
                        'error_code': 'invalid_action_error',
                        'error_message': "not the owner of the project"
                    }, status_code=400)
            elif project.status != ProjectStatus.open.value:
                # TODO need to define better errors
                return create_json_error_response({
                    'error_code': 'invalid_project_status_error',
                    'error_message': "project status is not opened"
                })
            
            project.status = ProjectStatus.ongoing.value

            project_participants = db.session.query(Application.owner_uid)\
                .filter(Application.status == ApplicationStatus.confirmed.value)\
                .filter(Application.project_id == project_id)\
                .all()

            db.session.commit()
        except Exception as e:
            logger.error(f"request_data : {json.dumps(request_data, indent=0)}")
            logger.exception(e)
            db.session.rollback()
            return create_json_error_response(e.args[0], status_code=400)
        else:
            recipients = []

            # add the project owner to the emailing list
            owner_user_email = firebase_helper.get_user_email_from_uid(project.owner_uid)
            recipients.append(                                {
                "address": owner_user_email,
                "displayName": owner_user_email
            })
            
            # add all other users that are in the project
            for (p_uid,) in project_participants:
                accepted_user_email = firebase_helper.get_user_email_from_uid(p_uid)
                recipients.append(
                    {
                        "address": accepted_user_email,
                        "displayName": accepted_user_email
                    }
                )

            title = "Team formation complete"
            body = render_template(
                "email/project_team_formation_complete.html",
                project_start_date=timestamp_to_year_month_date(project.start_date),
                project_end_date=timestamp_to_year_month_date(project.end_date)
            )
            azure_helper.send_email(title, recipients, body, body)

            # need to explicitly call session.close
            # because ORM objects are accessed again
            db.session.close()

            return create_json_response('', 201)




@project_bp.route('/save', methods=['POST'])
def save_project():
    logger.info("/project/save")
    if request.method == 'POST':
        try:
            request_data = request.json['data']
            request_auth_data = request.json['auth']
            user_info = firebase_helper.authenticate(request_auth_data)
            proj = Project(**request_data)

            db.session.begin()

            # set exist project to null as we don't know if its new project being saved or not
            exist_proj = None

            # if id not null then it means that its existing project
            if 'id' in request_data and request_data['id']:
                # If 'id' is present and not empty, then try to find the existing project - query the existing project
                exist_proj = db.session.query(Project)\
                            .filter(Project.id == request_data['id'])\
                            .filter(Project.owner_uid == user_info['uid'])\
                            .first()
                
                if not exist_proj:
                    # either the project doesn't exist or the user is not authorized
                    return create_json_error_response({
                        'error_code': 'not_authorized_or_nonexistent_project',
                        'error_message': "Project not found or user not authorized"
                    }, status_code=400)

                # if exist saved project found in db, check status saved or not
                elif exist_proj.status != ProjectStatus.saved.value:
                    return create_json_error_response({
                        'error_code': 'invalid_project_status_error',
                        'error_message': "project status is already submitted"
                    })

            # if exist saved project found in db, check uid matches or not. Or check current project's uid - this is redundant but i think its good to keep track
            if (exist_proj and exist_proj.owner_uid != user_info['uid']) or proj.owner_uid != user_info['uid']:
                return create_json_error_response({
                    'error_code': 'not_authorized_user',
                    'error_message': "not the owner of the project"
                }, status_code=400)

            if exist_proj:
                # if no error were found and saved project already exists, update the existing project with retrieved data from frontend
                for key, value in request_data.items():
                    if hasattr(exist_proj, key) and key not in ['id', 'created_at']:
                        setattr(exist_proj, key, value)  
                exist_proj.status = ProjectStatus.saved.value
            else:
                # if no existing project, then save a new project
                proj = Project(**request_data)
                proj.status = ProjectStatus.saved.value
                db.session.add(proj)

        except Exception as e:
            logger.error(f"request_data : {json.dumps(request_data, indent=0)}")
            logger.exception(e)
            db.session.rollback()
            return create_json_error_response(e.args[0])
        else:
            db.session.commit()
            # create new id for new proj or keep the existing proj id for one already existing
            proj_id = exist_proj.id if exist_proj else proj.id
            db.session.close() 
            return create_json_response({'id': proj_id}, status_code=201) 



@project_bp.route('/load', methods=['POST'])
def load_project():
    logger.info("/project/load")
    if request.method == 'POST':
        try:
            # getting infos from database, then authenticate using info from auth
            request_data = request.json['data']
            request_auth_data = request.json['auth']
            user_info = firebase_helper.authenticate(request_auth_data)

            # check if project id is provided
            if 'id' not in request_data:
                return create_json_error_response({
                    'error_code': 'project_not_found',
                    'error_message': 'Project not found',
                }, status_code=400)

            # query the database
            saved_project = db.session.query(Project)\
                            .filter(Project.id == request_data['id'])\
                            .filter(Project.owner_uid == user_info['uid'])\
                            .first()

            # handle cases where the project does not exist or status is not saved or the user is not authorized
            if not saved_project:
                return create_json_error_response({
                    'error_code': 'project_access_error',
                    'error_message': 'Project not found or access denied or project status not saved',
                }, status_code=400)

            elif saved_project.status != ProjectStatus.saved.value:
                return create_json_error_response({
                    'error_code': 'project_not_in_saved_status',
                    'error_message': 'Project is not in saved status',
                })

        except Exception as e:
            logger.error(f"request_data : {json.dumps(request_data, indent=0)}")
            logger.exception(e)
            db.session.rollback()
            return create_json_error_response(e.args[0])

        else:
            # if no errors, then serialize the saved project data and return the response
            serialized_saved_project = saved_project.to_dict()

            # create_json_response default to 200 code
            return create_json_response(serialized_saved_project)
    ## paul's implementation
    pass