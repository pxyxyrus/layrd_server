import server.firebase_helper as firebase_helper
import json
from flask import (
    Blueprint, Response, make_response, flash, g, redirect, render_template, request, session, url_for, abort
)
from server import db
from server.models import User
from server.util import *
from logger import logger

user_bp = Blueprint('user', __name__)


@user_bp.route('/register', methods=['POST'])
def register_user():
    logger.info("user/register")
    if request.method == 'POST':
        try:
            request_data = request.json['data']
            request_auth_data = request.json['auth']
            db.session.begin()
            user_info = firebase_helper.authenticate(request_auth_data)
            users = db.session.query(User).filter_by(uid=user_info['uid']).all()
            if len(users) == 0:
                user = User(
                    uid=user_info['uid'],
                    email=user_info['email'],
                )
                print(user)
                logger.info(f"User added \t\t email: {user_info['email']}, uid: {user_info['uid']}")
                db.session.add(user)
        except Exception as e:
            logger.error(f"request_data : {json.dumps(request_data, indent=0)}")
            logger.exception(e)
            db.session.rollback()
            return create_json_error_response(e.args[0])
        else:
            db.session.commit()
            return create_json_response('', status_code=201)



@user_bp.route('/update', methods=['POST'])
# expects a user firebase ID token
def update_user():
    logger.info("/user/update")
    if request.method == 'POST':
        try:
            request_data = request.json['data']
            request_auth_data = request.json['auth']
            user_info = firebase_helper.authenticate(request_auth_data)
            db.session.begin()
            users = db.session.query(User).filter_by(uid=request_data['uid']).all()
            for user in users:
                for key, value in request_data.items():
                    setattr(user, key, value)
        except Exception as e:
            logger.error(f"request_data : {json.dumps(request_data, indent=0)}")
            logger.exception(e)
            db.session.rollback()
            return create_json_error_response(e.args[0])
        else:
            db.session.commit()
            return create_json_response('', status_code=201)
        


@user_bp.route('/get_info', methods=['POST'])
def get_user_info():
    logger.info("/user/get_info")
    if request.method == 'POST':
        try:
            request_data = request.json['data']
            request_auth_data = request.json['auth']
            user_info = firebase_helper.authenticate(request_auth_data)
            db.session.begin()
            users = db.session.query(User).filter_by(uid=request_data['uid']).all()
            print(users)
        except Exception as e:
            logger.error(f"request_data : {json.dumps(request_data, indent=0)}")
            logger.exception(e)
            db.session.rollback()
            return create_json_error_response(e.args[0])
        else:
            response_data = query_result_to_json(users)
            db.session.commit()
            return create_json_response(response_data)