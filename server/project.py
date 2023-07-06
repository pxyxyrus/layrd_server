from server import db
from server.models import Project
from server.types import ProjectStatus
from server.util import *
import json
from flask import (
    Blueprint, Response, make_response, flash, g, redirect, render_template, request, session, url_for
)
import server.firebase_helper as firebase_helper



project_bp = Blueprint('project', __name__)

# cred = credentials.Certificate('./keys/block_research_key.json')
# firebase_app = firebase_admin.initialize_app(cred)



def change_project_status(request_data, status_to_change):
    db.session.begin()
    projects = db.session.query(Project).filter_by(id=request_data['id']).all()
    print(status_to_change)
    print(projects)
    for proj in projects:
        setattr(proj, "status", status_to_change)
    db.session.commit()



@project_bp.route('/upload', methods=['POST'])
def upload_project():
    print()
    if request.method == 'POST':
        try:
            request_data = request.json.data
            request_auth_data = request.json.auth
            user_info = firebase_helper.authenticate(request_auth_data)
            print(request_data)
            proj = Project(**request_data)
            print(proj)
            db.session.begin()
            db.session.add(proj)
        except Exception as e:
            db.session.rollback()
            return create_json_error_response(e.args[0])
        else:
            db.session.commit()
            return create_json_response('', status_code=201)



@project_bp.route('/withdraw', methods=['POST'])
def withdraw_project():
    print("withdraw_project")
    if request.method == 'POST':
        request_data = request.json.data
        print(request_data)
        try:
            change_project_status(request_data, ProjectStatus.withdrawn.value)
            return create_json_response('', status_code=201)
        except Exception as e:
            return create_json_error_response(e.args[0])
        



@project_bp.route('/complete', methods=['POST'])
def complete_project():
    print("complete_project")
    if request.method == 'POST':
        request_data = request.json.data
        print(request_data)
        try:
            change_project_status(request_data, ProjectStatus.successful.value)
            return create_json_response('', status_code=201)
        except Exception as e:
            return create_json_error_response(e.args[0])

    

@project_bp.route('/abort', methods=['POST'])
def abort_project():
    print("abort_project")
    if request.method == 'POST':
        request_data = request.json.data
        print(request_data)
        try:
            change_project_status(request_data, ProjectStatus.unsuccessful.value)
            return create_json_response('', status_code=201)
        except Exception as e:
            return create_json_error_response(e.args[0])




@project_bp.route('/<int:project_id>', methods=['GET'])
# expects a user firebase ID token
def get_project(project_id):
    print("get_project")
    if request.method == 'GET':
        try:
            db.session.begin()
            projects = db.session.query(Project).filter_by(id=id).all()
            return create_json_response(query_result_to_json(projects))
        except Exception as e:
            return create_json_error_response(e.args[0])



# @project_bp.route('/get_projects', methods=['GET'])
# # expects a user firebase ID token
# def get_project(project_id):
#     print("get_project")
#     if request.method == 'GET':
#         print(request.args.get('id'))
#         db.session.begin()
#         projects = db.session.query(Project).filter_by(id=id).all()
#         return create_json_response(query_result_to_json_str(projects))