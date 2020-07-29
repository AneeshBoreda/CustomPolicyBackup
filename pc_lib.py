import json
import requests
import time

# --Description-- #
# Prisma Cloud Helper library. Contains
# --End Description-- #


# --Helper Methods-- #
# Main API Call Function
def pc_call_api(action, api_url, config, data=None, params=None, try_count=0, max_retries=2, auth_count=0, auth_retries=1):
    retry_statuses = [429, 500, 502, 503, 504]
    auth_statuses = [401]
    retry_wait_timer = 5
    headers = {'Content-Type': 'application/json', 'x-redlock-auth': config['jwt']}

    # Make the API Call
    response = requests.request(action, api_url, params=params, headers=headers, data=json.dumps(data))


    # Check for an error to retry, re-auth, or fail
    if response.status_code in retry_statuses:
        try_count = try_count + 1
        if try_count <= max_retries:
            time.sleep(retry_wait_timer)
            return pc_call_api(action=action, api_url=api_url, config=config, data=data, params=params,
                               try_count=try_count, max_retries=max_retries, auth_count=auth_count, auth_retries=auth_retries)
        else:
            response.raise_for_status()
    elif response.status_code in auth_statuses and config['jwt'] is not None:
        auth_count = auth_count + 1
        if auth_count <= auth_retries:
            config = pc_jwt_get(config)
            return pc_call_api(action=action, api_url=api_url, config=config, data=data, params=params,
                               try_count=try_count, max_retries=max_retries, auth_count=auth_count,auth_retries=auth_retries)
        else:
            response.raise_for_status()
    else:
        response.raise_for_status()

    # Check for valid response and catch if blank or unexpected
    api_response_package = {}
    api_response_package['statusCode'] = response.status_code
    try:
        api_response_package['data'] = response.json()
    except ValueError:
        if response.text == '':
            api_response_package['data'] = None
        else:
            raise Exception("Unexpected Server response.")
    return  api_response_package


# Get JWT for access
def pc_jwt_get(config):
    url = "https://" + config['apiBase'] + "/login"
    action = "POST"
    resp=requests.post(url, json={'username':config['username'],'password':config['password']})
    config['jwt'] = resp.json()['token']
    return config


# Get policy list
def api_policy_list_get(params):
    action = "GET"
    url = "https://" + config['apiBase'] + "/policy"
    return pc_call_api(action, url, config, params=params)

def api_search_get(param):
    action = "GET"
    url = "https://" + config['apiBase'] + "/search/history/"+param
    return pc_call_api(action, url, config)

def api_policy_add(params):
    action = "POST"
    url = "https://" + config['apiBase'] + "/policy"
    return pc_call_api(action, url, config, data=params)

def api_policy_update(policyid,params):
    action = "PUT"
    url = "https://" + config['apiBase'] + "/policy/"+policyid
    return pc_call_api(action, url, config,data=params)
config=json.load(open('settings.conf','r'))
config['apiBase']='api'+config['apiBase'][3:]
pc_jwt_get(config)