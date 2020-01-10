import requests
import json
import os
import logging
import coloredlogs


def log_rep(stdin):
    coloredlogs.install()
    logging.info(stdin)


def log_err(stdin):
    coloredlogs.install()
    logging.error(stdin)


def send_http(url, data, headers=None):
    json_data = json.dumps(data)
    try:
        send = requests.post(url, data=json_data, headers=headers)
        respons = send.json()
        response_time = send.elapsed.total_seconds()
    except requests.exceptions.RequestException:
        respons = {
            "result": False,
            "Error": "Failed to establish a new connection",
            "description": None,
        }
        return respons
    else:
        result = {
            "result": respons["result"],
            "time": response_time,
            "data": respons["data"],
            "status": respons["status"],
        }
        return result


def get_http(url, params=None):
    try:
        response = requests.get(url, params)
    except requests.exceptions.RequestException as e:
        log_err(e)
        return False
    except Exception as a:
        log_err(a)
        return False
    else:
        data = response.json()
        return data
