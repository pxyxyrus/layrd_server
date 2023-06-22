from server import db
from server.models import Project, Application
from server.types import ProjectStatus, ApplicationStatus

from flask import (
    Blueprint, Response, make_response, flash, g, redirect, render_template, request, session, url_for
)

import json

app_bp = Blueprint('application', __name__)

# cred = credentials.Certificate('./keys/block_research_key.json')
# firebase_app = firebase_admin.initialize_app(cred)



@app_bp.route('/apply', methods=['POST'])
# expects a user firebase ID token
def apply():
    print("apply")

    if request.method == 'POST':
        request_data = request.json
        project_application = Application(**request_data)
        try:
            db.session.begin()
            db.session.add(project_application)
        except Exception as e:
            db.session.rollback()
            return Response("{'result':'{}'}".format(e), status=400, mimetype='application/json')
        else:
            db.session.commit()
            return Response("{'result':'success'}", status=201, mimetype='application/json')


# debug functionality
@app_bp.route('/get_applications', methods=['GET'])
# expects a user firebase ID token
def get_applications():
    print("apply")
    if request.method == 'GET':
        print(request.json)
        applications = db.session.query(Application).filter_by(**request.args).all()
        to_dict = lambda obj : obj.as_dict()
        applications = list(map(to_dict, applications))
        print(applications)
        return Response("{'result':'success'}", status=201, mimetype='application/json')



@app_bp.route('/project_applications', methods=['POST'])
# expects a user firebase ID token
def project_applications():
    print("project_application")
    if request.method == 'POST':
        print(request.json)

        # project owner authentication logic

        applications = db.session.query(Application).filter_by(**request.args).all()
        to_dict = lambda obj : obj.as_dict()
        applications = list(map(to_dict, applications))
        print(applications)
        return Response(json.dumps(applications, indent=4, sort_keys=True, default=str), status=201, mimetype='application/json')



@app_bp.route('/my_applications', methods=['POST'])
# expects a user firebase ID token
def my_applications():
    print("apply")
    if request.method == 'POST':
        print(request.json)

        # application owner check logic

        applications = db.session.query(Application).filter_by(**request.args).all()
        to_dict = lambda obj : obj.as_dict()
        applications = list(map(to_dict, applications))
        print(applications)
        return Response(json.dumps(applications, indent=4, sort_keys=True, default=str), status=201, mimetype='application/json')