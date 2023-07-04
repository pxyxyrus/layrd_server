import server.firebase_helper as firebase_helper
import json
from flask import (
    Blueprint, Response, make_response, flash, g, redirect, render_template, request, session, url_for, abort
)
from server import db
from server.models import User
from server.util import *

user_bp = Blueprint('user', __name__)


@user_bp.route('/register', methods=['POST'])
def register_user():
    print("register_user")
    print(request.method)
    if request.method == 'POST':
        try:
            request_data = request.json
            print(request_data['id_token'])
            db.session.begin()
            user_info = firebase_helper.authenticate_id_token(request_data['id_token'])
            users = db.session.query(User).filter_by(uid=request_data['uid']).all()
            if len(users) == 0:
                user = User(
                    uid=user_info['uid'],
                    email=user_info['email'],
                )
                print(user)
                db.session.add(user)
        except Exception as e:
            db.session.rollback()
            return create_json_error_response(e.args[0])
        else:
            db.session.commit()
            return create_json_response('', status_code=201)






@user_bp.route('/update', methods=['POST'])
# expects a user firebase ID token
def update_user():
    print("update_user")
    if request.method == 'POST':
        request_data = request.json
        print(request_data['id_token'])
        user_info = firebase_helper.authenticate_id_token(request_data['id_token'])
        print(user_info)
        try:
            db.session.begin()
            users = db.session.query(User).filter_by(uid=request_data['uid']).all()
            for user in users:
                for key, value in request_data.items():
                    setattr(user, key, value)
        except Exception as e:
            db.session.rollback()
            return create_json_error_response(e.args[0])
        else:
            db.session.commit()
            return create_json_response('', status_code=201)
        


@user_bp.route('/get_info', methods=['POST'])
def get_user_info():
    print("get_user_info")
    if request.method == 'POST':
        request_data = request.json
        print(request_data['id_token'])
        user_info = firebase_helper.authenticate_id_token(request_data['id_token'])
        print(user_info)
        try:
            db.session.begin()
            users = db.session.query(User).filter_by(uid=request_data['uid']).all()
            print(users)
        except Exception as e:
            db.session.rollback()
            return create_json_error_response(e.args[0])
        else:
            db.session.commit()
            return create_json_response(query_result_to_json_str(users))