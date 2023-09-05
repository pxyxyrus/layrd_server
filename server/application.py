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
            print(request.json)
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


