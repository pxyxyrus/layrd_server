# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import auth

from flask import (
    Blueprint, Response, make_response, flash, g, redirect, render_template, request, session, url_for
)

auth_bp = Blueprint('authenticate', __name__)

# cred = credentials.Certificate('./keys/block_research_key.json')
# firebase_app = firebase_admin.initialize_app(cred)


@auth_bp.route('/authenticate', methods=['POST'])
def authenticate():
    print("authenticate registered")
    if request.method == 'POST':
        return "post_success"
    elif request.method == 'GET':
        return "get_success"
