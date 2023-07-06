from server import db
from server.models import Project, Application
from server.types import ProjectStatus, ApplicationStatus
from flask import (
    Blueprint, Response, make_response, flash, g, redirect, render_template, request, session, url_for
)
import json
from server.util import *
import server.firebase_helper as firebase_helper

app_bp = Blueprint('application', __name__)

# cred = credentials.Certificate('./keys/block_research_key.json')
# firebase_app = firebase_admin.initialize_app(cred)



@app_bp.route('/submit', methods=['POST'])
# expects a user firebase ID token
def apply():
    print("apply")
    if request.method == 'POST':
        try:
            request_data = request.json.data
            request_auth_data = request.json.auth
            user_info = firebase_helper.authenticate(request_auth_data)
            project_application = Application(**request_data)
            db.session.begin()
            db.session.add(project_application)
        except Exception as e:
            db.session.rollback()
            return create_json_error_response(e.args[0], status_code=400)
        else:
            db.session.commit()
            return create_json_response('', 201)


# debug functionality
@app_bp.route('/get', methods=['POST'])
# expects a user firebase ID token
def get_applications():
    print("apply")
    if request.method == 'POST':
        try:
            print(request.json)
            request_data = request.json.data
            request_auth_data = request.json.auth
            applications = db.session.query(Application).filter_by(
                # TODO : add constraints
            ).all()
            response_data = query_result_to_json(applications)
            return create_json_response(response_data)
        except Exception as e:
            db.session.rollback()
            return create_json_error_response(e.args[0], status_code=400)







@app_bp.route('/select', methods=['POST'])
def select_application():
    print(select_application)
    if request.method == 'POST':
        try:
            request_data = request.json.data
            request_auth_data = request.json.auth
            print(request_data['id_token'])
            # application owner check logic
            db.session.begin()
            applications = db.session.query(Application).filter_by(
                # TODO : add constraints
            ).all()
            application = applications[0]
            # TODO : change application to selected state
        except Exception as e:
            db.session.rollback()
            return create_json_error_response(e.args[0], status_code=400)
        else:
            db.session.commit()
            return create_json_response('', 201)

    