from server import db
from server.models import Project, ProjectStatus

import json

from flask import (
    Blueprint, Response, make_response, flash, g, redirect, render_template, request, session, url_for
)

project_bp = Blueprint('project', __name__)

# cred = credentials.Certificate('./keys/block_research_key.json')
# firebase_app = firebase_admin.initialize_app(cred)



def change_project_status(request_data, status_to_change):
    db.session.begin()
    projects = db.session.query(Project).filter_by(id=request_data['id']).all()
    for proj in projects:
        setattr(proj, "status", status_to_change)
    db.session.commit()



@project_bp.route('/upload_project', methods=['POST'])
def upload_project():
    print()
    if request.method == 'POST':
        request_data = request.json
        print(request_data)
        proj = Project()

        try:
            db.session.begin()
            for key in request_data.keys():
                setattr(proj, key, request_data[key])
            print(proj)
            db.session.add(proj)
        except Exception as e:
            db.session.rollback()
            return Response("{'result':'{}'}".format(e), status=400, mimetype='application/json')
        else:
            db.session.commit()
            return Response("{'result':'success'}", status=201, mimetype='application/json')



@project_bp.route('/withdraw_project', methods=['POST'])
def withdraw_project():
    print("withdraw_project")
    if request.method == 'POST':
        request_data = request.json
        print(request_data)

        try:
            change_project_status(request_data, ProjectStatus.withdrawn)
            return Response("{'result':'success'}", status=201, mimetype='application/json')
        except Exception as e:
            return Response("{'result':'{}'}".format(e), status=400, mimetype='application/json')
        



@project_bp.route('/complete_project', methods=['POST'])
def complete_project():
    print("complete_project")
    if request.method == 'POST':
        request_data = request.json
        print(request_data)

        try:
            change_project_status(request_data, ProjectStatus.successful)
            return Response("{'result':'success'}", status=201, mimetype='application/json')
        except Exception as e:
            return Response("{'result':'{}'}".format(e), status=400, mimetype='application/json')

    

@project_bp.route('/abort_project', methods=['POST'])
def upload_project():
    print("abort_project")
    if request.method == 'POST':
        request_data = request.json
        print(request_data)

        try:
            change_project_status(request_data, ProjectStatus.unsuccessful)
            return Response("{'result':'success'}", status=201, mimetype='application/json')
        except Exception as e:
            return Response("{'result':'{}'}".format(e), status=400, mimetype='application/json')



@project_bp.route('/get_project', methods=['GET'])
# expects a user firebase ID token
def get_project():
    print("get_project")
    if request.method == 'GET':
        print(request.args.get('id'))
        id = request.args.get('id')
        db.session.begin()
        projects = db.session.query(Project).filter_by(id=id).all()
        
        to_dict = lambda obj : obj.as_dict()
        projects = list(map(to_dict, projects))
        print(projects)
        return Response(json.dumps(projects, indent=4, sort_keys=True, default=str), status=201, mimetype='application/json')




