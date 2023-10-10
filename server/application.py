from server import db
from server.models import Project, Application
from server.types import ProjectStatus, ApplicationStatus
from flask import (
    Blueprint, render_template, request,
)
import json
from server.util import *
import server.firebase_helper as firebase_helper
from logger import logger
import server.azure_helper as azure_helper

app_bp = Blueprint('application', __name__)




@app_bp.route('/submit', methods=['POST'])
# expects a user firebase ID token
def apply():
    logger.info("/application/submit")
    if request.method == 'POST':
        try:
            request_data = request.json['data']
            request_auth_data = request.json['auth']
            user_info = firebase_helper.authenticate(request_auth_data)
            project_application = Application(**request_data)
            db.session.begin()
            db.session.add(project_application)
        except Exception as e:
            logger.error(f"request_data : {json.dumps(request_data, indent=0)}")
            logger.exception(e)
            db.session.rollback()
            return create_json_error_response(e.args[0], status_code=400)
        else:
            db.session.commit()
            recipients = [
                {
                    "address": user_info["email"],
                    "displayName": user_info["email"]
                }
            ]
            title = "Congratuation on your application!"
            body = render_template("email/application_submit.html", application_link=request_data['resume_link'])
            azure_helper.send_email(title, recipients, body, body)

            return create_json_response('', 201)


# debug functionality
@app_bp.route('/<int:application_id>', methods=['POST'])
# expects a user firebase ID token
def get_application(application_id):
    logger.info(f"/application/{application_id}")
    if request.method == 'POST':
        try:
            print(request.json)
            request_data = request.json['data']
            request_auth_data = request.json['auth']
            user_info = firebase_helper.authenticate(request_auth_data)
            applications = db.session.query(Application).filter_by(
                id=application_id, owner_uid=user_info['uid']
            ).all()
        except Exception as e:
            logger.error(f"request_data : {json.dumps(request_data, indent=0)}")
            logger.exception(e)
            db.session.rollback()
            return create_json_error_response(e.args[0], status_code=400)
        else:
            response_data = query_result_to_json(applications)
            db.session.commit()
            return create_json_response(response_data)
        

@app_bp.route('/get_applications', methods=['POST'])
# expects a user firebase ID token
def get_applications():
    logger.info("/application/get_applications")
    if request.method == 'POST':
        try:
            request_data = request.json['data']
            request_auth_data = request.json['auth']
            user_info = firebase_helper.authenticate(request_auth_data)
            cursor = request_data.pop('cursor', None)
            if cursor is not None:
                applications = db.session.query(Application).filter(Application.id > cursor).filter_by(
                    owner_uid=user_info['uid'],
                    **request_data
                ).limit(25).all()
            else:
                applications = db.session.query(Application).filter_by(
                    **request_data
                ).limit(25).all()
        except Exception as e:
            logger.error(f"request_data : {json.dumps(request_data, indent=0)}")
            logger.exception(e)
            db.session.rollback()
            return create_json_error_response(e.args[0], status_code=400)
        else:
            response_data = query_result_to_json(applications)
            db.session.commit()
            return create_json_response(response_data)



@app_bp.route('/confirm', methods=['POST'])
def confirm_project():
    logger.info("/application/confirm")
    if request.method == 'POST':
        try:
            print(request.json)
            request_data = request.json['data']
            request_auth_data = request.json['auth']
            user_info = firebase_helper.authenticate(request_auth_data)
            id = request_data.pop(id)

            db.session.begin_nested()

            application = db.session.query(Application).filter_by(
                    id=id,
                    owner_uid=user_info['uid'],
                    status=ApplicationStatus.accepted.value
                )\
                .with_for_update()\
                .first()

            if application is None:
                # TODO need to define better errors
                return create_json_error_response({
                    'error_code': 'invalid_action_error',
                    'error_message': "invalid application"
                }, status_code=400)

            # check the number of confirmed applicants
            project_participants = db.session.query(Application.owner_uid)\
                .filter(Application.status == ApplicationStatus.confirmed.value)\
                .filter(Application.project_id == application.project_id)\
                .with_for_update()\
                .all()
            
            cur_participant_num = len(project_participants)
            
            # get the project
            project = db.session.query(Project)\
                .filter(Project.id == application.project_id)\
                .filter(Project.status == ProjectStatus.open.value)\
                .first()
            
            # if the project is non existent
            # or the project is already full
            if project is None\
                or (cur_participant_num >= project.participant_num):
                # TODO need to define better errors
                return create_json_error_response({
                    'error_code': 'invalid_action_error',
                    'error_message': "invalid project"
                }, status_code=400)
            
            elif cur_participant_num < project.participant_num:
                application.status = ApplicationStatus.confirmed.value
                cur_participant_num += 1
                if cur_participant_num == project.participant_num:
                    project.status = ProjectStatus.ongoing.value

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
            
            # add the user that was just added right now
            accepted_user_email = firebase_helper.get_user_email_from_uid(application.owner_uid)
            recipients.append(                                {
                "address": accepted_user_email,
                "displayName": accepted_user_email
            })

            # add all other users that are in the project
            for p_uid in project_participants:
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
                project_start_date=project.start_date,
                project_end_date=project.end_date
            )
            azure_helper.send_email(title, recipients, body, body)

            # need to explicitly call session.close
            # because ORM objects are accessed again
            db.session.close()

            return create_json_response('', status_code=201)



@app_bp.route('/withdraw', methods=['POST'])
def withdraw_project():
    logger.info("/application/withdraw_project")
    if request.method == 'POST':
        try:
            print(request.json)
            request_data = request.json['data']
            request_auth_data = request.json['auth']
            user_info = firebase_helper.authenticate(request_auth_data)
            id = request_data.pop(id)

            application = db.session.query(Application).filter_by(
                    id=id,
                    owner_uid=user_info['uid'],
                    status=ApplicationStatus.accepted.value
                )\
                .with_for_update()\
                .first()

            application.status = ApplicationStatus.withdrawn.value

        except Exception as e:
            logger.error(f"request_data : {json.dumps(request_data, indent=0)}")
            logger.exception(e)
            db.session.rollback()
            return create_json_error_response(e.args[0], status_code=400)
        else:
            db.session.commit()
            return  create_json_response('', status_code=201)
