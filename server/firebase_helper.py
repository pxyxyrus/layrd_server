import firebase_admin
from firebase_admin import (credentials, auth)
import json
from logger import logger


cred = credentials.Certificate('./keys/firebase_block_research_key.json')
firebase_app = firebase_admin.initialize_app(cred)
logger.info("firebase app initialized")


uid_cache = {}



# TODO utilize the cache you have
def authenticate(auth_data):
    try:
        id_token = auth_data['id_token']
        uid = auth_data['uid']
        # Verify the ID token while checking if the token is revoked by
        # passing check_revoked=True.
        decoded_token = auth.verify_id_token(id_token, check_revoked=True)
        if decoded_token['uid'] != uid:
            logger.error(f"uid, id_token mismatch \t\t uid : {uid}, uid_from_id_token : {decoded_token['uid']}")
            raise Exception({
                'error_code': 'auth_error',
                'error_message': "uid, id_token mismatch"
            }) from None
        # Token is valid and not revoked.
        uid_cache[decoded_token['uid']] = decoded_token
        return decoded_token
    except (auth.RevokedIdTokenError, auth.InvalidIdTokenError) as e:
        logger.error(f"id_token is invalid \t\t uid : {uid}")
        logger.exception(e)
        # Token revoked, inform the user to reauthenticate or signOut().
        raise Exception({'error_code': 'auth_error',  'error_message': e.default_message}) from None
    except (auth.UserDisabledError) as e:
        logger.error(f"user is disabled \t\t uid : {uid}")
        logger.exception(e)
        raise Exception({'error_code': 'user_disabled', 'error_message': e.default_message}) from None
    except Exception as e:
        # TODO logging needed, including stacktrace
        logger.exception(e)
        raise Exception({
                'error_code': 'auth_error',
                'error_message': "internal_error" if hasattr(e, "default_message") else getattr(e, "default_message")
            }) from None

        

def get_user_email_from_uid(uid):
    user = auth.get_user(uid)
    return user.email




