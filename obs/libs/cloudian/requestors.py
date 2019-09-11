import requests
from obs.libs.utils import env_utils


def request(url, data=None, json=None, method="GET"):
    env_data = env_utils.get_env_values_cloudian()
    root_url = env_data["root_url"]
    port = env_data["port"]
    user = env_data["username"]
    password = env_data["password"]

    request = dict()
    request["method"] = method

    if data is not None:
        request["data"] = data.pop("data", None)
        for index, (key, value) in enumerate(data.items()):
            url += "{symbol}{key}={value}".format(
                symbol="&" if index else "?", key=key, value=value
            )
    elif json is not None:
        request["json"] = json

    api_call = "{url}:{port}/{call}".format(url=root_url, port=port, call=url)

    try:
        response = requests.request(
            verify=False,
            method=method,
            url=api_call,
            data=request["data"] if data is not None else None,
            json=request["json"] if json is not None else None,
            auth=(user, password),
        )

        if response.status_code == 200:
            try:
                return {
                    "status_code": response.status_code,
                    "status_message": "ok",
                    "data": response.json(),
                }
            except ValueError:
                return {
                    "status_code": response.status_code,
                    "status_message": response.text,
                    "data": {},
                }
        else:
            return {
                "status_code": response.status_code,
                "status_message": response.reason,
            }

    except requests.exceptions.ConnectionError as err:
        return {"status_code": err.errno, "status_message": err.message}
