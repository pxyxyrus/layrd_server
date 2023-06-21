from server import db
from server.models import Project, Application
from server.types import ProjectStatus, ApplicationStatus

from flask import (
    Blueprint, Response, make_response, flash, g, redirect, render_template, request, session, url_for
)

app_bp = Blueprint('application', __name__)

# cred = credentials.Certificate('./keys/block_research_key.json')
# firebase_app = firebase_admin.initialize_app(cred)



@app_bp.route('/apply', methods=['POST'])
# expects a user firebase ID token
def authenticate():
    print("apply")
    if request.method == 'POST':
        print(request.json)
        return Response("{'result':'success'}", status=201, mimetype='application/json')



# debug functionality
@app_bp.route('/applications', methods=['GET'])
# expects a user firebase ID token
def authenticate():
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
def authenticate():
    print("project_application")
    if request.method == 'POST':
        print(request.json)

        # project owner authentication logic

        applications = db.session.query(Application).filter_by(**request.args).all()
        to_dict = lambda obj : obj.as_dict()
        applications = list(map(to_dict, applications))
        print(applications)
        return Response("{'result':'success'}", status=201, mimetype='application/json')



@app_bp.route('/my_applications', methods=['POST'])
# expects a user firebase ID token
def authenticate():
    print("apply")
    if request.method == 'POST':
        print(request.json)

        # application owner check logic

        applications = db.session.query(Application).filter_by(**request.args).all()
        to_dict = lambda obj : obj.as_dict()
        applications = list(map(to_dict, applications))
        print(applications)
        return Response("{'result':'success'}", status=201, mimetype='application/json')