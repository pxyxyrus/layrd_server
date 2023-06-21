# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import auth

from flask import (
    Blueprint, Response, make_response, flash, g, redirect, render_template, request, session, url_for
)

auth_bp = Blueprint('authenticate', __name__)

# cred = credentials.Certificate('./keys/block_research_key.json')
# firebase_app = firebase_admin.initialize_app(cred)

from server import db
from server.models import User


@auth_bp.route('/register_user', methods=['POST'])
# expects a user firebase ID token
def register_user():
    print("register_user")
    if request.method == 'POST':
        request_data = request.json
        print(request_data)
        user = User(**request_data)
        print(user)
        try:
            db.session.begin()
            db.session.add(user)
        except Exception as e:
            db.session.rollback()
            return Response("{'result':'{}'}".format(e), status=400, mimetype='application/json')
        else:
            db.session.commit()
            return Response("{'result':'success'}", status=201, mimetype='application/json')
        


@auth_bp.route('/update_user', methods=['POST'])
# expects a user firebase ID token
def update_user():
    print("update_user")
    if request.method == 'POST':
        request_data = request.json
        print(request_data)
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
        


@auth_bp.route('/authenticate_user', methods=['POST'])
# expects a user firebase ID token
def authenticate_user():
    print("authenticate_user")
    if request.method == 'POST':
        print(request.json)
        return Response("{'result':'success'}", status=201, mimetype='application/json')

