from requests import request
from requests.auth import HTTPBasicAuth
from binascii import b2a_hex
from os import urandom
import json
import random
import string

# FUNCTIONS


def get_types(url, username, password):
    types_id = []
    get_resp = request('GET', url + '/ca/api/devices/types/', verify=False, auth=HTTPBasicAuth(username, password))
    if get_resp.status_code == 200:
        json_data = json.loads(get_resp.text)

        for i in range(len(json_data)):
            types_id.append({'id': json_data[i]['id'], 'name': json_data[i]['name']})
        return types_id, get_resp
    else:
        return [], get_resp


def add_sensor(url, username, password, typeId, typeName, sensorName, bleId):

    uuid_end = b2a_hex(urandom(6)).decode("utf-8")
    add_sensor_query = {
    "typeId": typeId,
    "type": typeName,
    "uuid": "88888888-8888-8888-8888-%s" % uuid_end,
    "name": sensorName,
    "registrationKey": "regkey-" + ''.join(random.choice(string.digits) for _ in range(4)),
    "additionalIds": {
        "values": {
            "CA_BLE_ID": bleId
        }
    }
    }

    post_resp = request('POST', url + '/ca/api/devices/', verify=False, auth=HTTPBasicAuth(username, password), json=add_sensor_query)

    if post_resp.status_code == 200:
        post_web = request('POST', url + '/ca/api/devices/pair/key/%s' % add_sensor_query['registrationKey'], verify=False, auth=HTTPBasicAuth(username, password))
        return add_sensor_query, str(post_resp), str(post_web)
    else:
        return add_sensor_query, str(post_resp), "N/A"

# BASE PROGRAM


