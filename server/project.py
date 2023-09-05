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



@project_bp.route('/withdraw', methods=['POST'])
def withdraw_project():
    logger.info("/project/withdraw")
    if request.method == 'POST':
        request_data = request.json['data']
        try:
            change_project_status(request_data, ProjectStatus.withdrawn.value)
            return create_json_response('', status_code=201)
        except Exception as e:
            logger.error(f"request_data : {json.dumps(request_data, indent=0)}")
            logger.exception(e)
            return create_json_error_response(e.args[0])
        



@project_bp.route('/complete', methods=['POST'])
def complete_project():
    logger.info("/project/complete")
    if request.method == 'POST':
        request_data = request.json['data']
        print(request_data)
        try:
            change_project_status(request_data, ProjectStatus.successful.value)
            return create_json_response('', status_code=201)
        except Exception as e:
            logger.error(f"request_data : {json.dumps(request_data, indent=0)}")
            logger.exception(e)
            return create_json_error_response(e.args[0])

    

@project_bp.route('/abort', methods=['POST'])
def abort_project():
    logger.info("/project/abort")
    if request.method == 'POST':
        request_data = request.json['data']
        print(request_data)
        try:
            change_project_status(request_data, ProjectStatus.unsuccessful.value)
            return create_json_response('', status_code=201)
        except Exception as e:
            logger.error(f"request_data : {json.dumps(request_data, indent=0)}")
            logger.exception(e)
            return create_json_error_response(e.args[0])




@project_bp.route('/<int:project_id>', methods=['GET'])
# expects a user firebase ID token
def get_project(project_id):
    logger.info(f"project/{project_id}")
    if request.method == 'GET':
        try:
            db.session.begin()
            projects = db.session.query(Project, func.count(Application.id).label('application_count'))\
                .outerjoin(Application, Project.id == Application.project_id)\
                .filter(Project.id==project_id)\
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



@project_bp.route('/get_projects', methods=['POST'])
def get_projects():
    logger.info("/project/get_projects")
    if request.method == 'POST':
        try:
            request_data = request.json['data']
            db.session.begin()
            cursor = request_data.pop('cursor', None)
            projects = None
            request_data = { getattr(Project, key):value for key, value in request_data.items()}

            projects = db.session.query(Project, func.count(Application.id).label('application_count'))\
                .outerjoin(Application, Project.id == Application.project_id)

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
            # application owner check logic
            db.session.begin()
            projects = db.session.query(Project)\
                .filter(Project.id==project_id)\
                .limit(25)\
                .all()
            
            if user_info['uid'] != projects[0].owner_uid:
                return create_json_error_response({
                        'error_code': 'invalid_action_error',
                        'error_message': "not the owner of the project"
                    }, status_code=400)

            print(str(db.session.query(Application)\
                .filter(or_(Application.id == id for id in app_ids))\
                .limit(25)\
                .statement))
            applications = db.session.query(Application)\
                .filter(or_(Application.id == id for id in app_ids))\
                .limit(25)\
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
            return create_json_response('', 201)
