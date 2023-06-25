import server.firebase_helper as firebase_helper

from flask import (
    Blueprint, Response, make_response, flash, g, redirect, render_template, request, session, url_for
)

from server import db
from server.models import User

auth_bp = Blueprint('authenticate', __name__)


@auth_bp.route('/register_user', methods=['POST'])
# expects a user firebase ID token
def register_user():
    print("register_user")
    print(request.method)
    if request.method == 'POST':
        request_data = request.json
        print(request_data['id_token'])
        user_info = firebase_helper.authenticate_id_token(request_data['id_token'])
        print(user_info)
        user = User(
            uid=user_info['uid'],
            email=user_info['email'],
        )
        print(user)
        try:
            db.session.begin()
            db.session.add(user)
        except Exception as e:
            db.session.rollback()
            response = Response("{'result':'{}'}".format(e), status=400, mimetype='application/json')
            return response
        else:
            db.session.commit()
            response = Response("{'result':'success'}", status=201, mimetype='application/json')
            return response
        


@auth_bp.route('/update_user', methods=['POST'])
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
            users = db.session.query(User).filter_by(id=request_data['id']).all()
            for user in users:
                for key, value in request_data.items():
                    setattr(user, key, value)
        except Exception as e:
            db.session.rollback()
            return Response("{'result':'{}'}".format(e), status=400, mimetype='application/json')
        else:
            db.session.commit()
            return Response("{'result':'success'}", status=201, mimetype='application/json')
        


