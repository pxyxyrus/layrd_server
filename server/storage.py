from flask import (
    Blueprint, Response, make_response, flash, g, redirect, render_template, request, session, url_for
)
import json
from server.util import *
from logger import logger
import server.azure_helper as azure_helper
import server.firebase_helper as firebase_helper


storage_bp = Blueprint('storage', __name__)


@storage_bp.route('/get_token', methods=['POST'])
# expects a user firebase ID token
def apply():
    if request.method == 'POST':
        try:
            request_auth_data = request.json['auth']
            user_info = firebase_helper.authenticate(request_auth_data)
            token = azure_helper.create_account_sas()
            print(token)
        except Exception as e:
            logger.error(f"request_data : {json.dumps(request_data, indent=0)}")
            logger.exception(e)
            return create_json_error_response(e.args[0], status_code=400)
        else:
            return create_json_response(token, 201)


