from server import db
from server.models import Project, Application
from server.types import ProjectStatus, ApplicationStatus
from flask import (
    Blueprint, Response, make_response, flash, g, redirect, render_template, request, session, url_for
)
import json
from server.util import *

app_bp = Blueprint('application', __name__)

# cred = credentials.Certificate('./keys/block_research_key.json')
# firebase_app = firebase_admin.initialize_app(cred)



@app_bp.route('/submit', methods=['POST'])
# expects a user firebase ID token
def apply():
    print("apply")
    if request.method == 'POST':
        request_data = request.json
        print(request_data['id_token'])
        project_application = Application(**request_data['application_data'])
        try:
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
        print(request.json)
        request_data = request.json
        applications = db.session.query(Application).filter_by(
            # TODO : add constraints
        ).all()
        response_data = query_result_to_json_str(applications)
        return create_json_response(response_data)





@app_bp.route('/select', methods=['POST'])
def select_application():
    print(select_application)
    if request.method == 'POST':
        request_data = request.json
        print(request_data['id_token'])

        # application owner check logic
        try:
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

    