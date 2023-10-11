import json
from flask import Response
from server.models import RootModel
import datetime





def query_result_to_json(query_results: list[RootModel]):
    to_dict = lambda obj : obj.to_dict()
    query_results = list(map(to_dict, query_results))
    return query_results

# expects data to be a list of json objects
def create_json_response(data, success: bool=True, status_code: int = 200):
    response_data = dict({})
    response_data['result'] = 'success' if success else 'error'
    response_data['data'] = data
    print(response_data)
    print(json.dumps(response_data))
    return Response(json.dumps(response_data), status=status_code, mimetype='application/json')

# expects data to be a json object
def create_json_error_response(data, status_code: int = 400):
    return create_json_response(data, success=False, status_code=status_code)


# this function assumes timestamp is in seconds
# returns year-month-date in UTC
def timestamp_to_year_month_date(timestamp):
    return datetime.datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d')