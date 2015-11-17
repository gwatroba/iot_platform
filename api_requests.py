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


def get_hub_id(url, username, password):

    get_resp = request('GET', url + '/ca/api/devices?size=5000', verify=False, auth=HTTPBasicAuth(username, password))

    if get_resp.status_code == 200:
        json_data = json.loads(get_resp.text)
        hub_id = False
        for hub in json_data['content']:
            if hub['type'] == 'ACTIVE_HUB':
                hub_id = hub['id']
        if bool(hub_id):
            return hub_id
        else:
            return False


def get_device_id(url, username, password, uuid):
    get_resp = request('GET', url + '/ca/api/devices?size=5000', verify=False, auth=HTTPBasicAuth(username, password))

    if get_resp.status_code == 200:
        json_data = json.loads(get_resp.text)
        device_id = False
        for device in json_data['content']:
            if device['uuid'] == uuid:
                device_id = device['id']
        if bool(device_id):
            return device_id
        else:
            return False


def add_to_hub(url, username, password, hub_id, device_id):

    query = '["%s"]' % device_id
    query_json = json.loads(query)
    post_resp = request('POST', url + '/ca/api/devices/%s/topology' % hub_id, verify=False, auth=HTTPBasicAuth(username, password), json=query_json)
    if post_resp.status_code == 200:
        return post_resp
    else:
        return post_resp


def add_sensor(url, username, password, type_id, type_name, sensor_name, ble_id):

    uuid_end = b2a_hex(urandom(6)).decode("utf-8")
    add_sensor_query = {
    "typeId": type_id,
    "type": type_name,
    "uuid": "88888888-8888-8888-8888-%s" % uuid_end,
    "name": sensor_name,
    "registrationKey": "regkey-" + ''.join(random.choice(string.digits) for _ in range(4)),
    "additionalIds": {
        "values": {
            "CA_BLE_ID": ble_id
        }
    }
    }
    post_resp = request('POST', url + '/ca/api/devices/', verify=False, auth=HTTPBasicAuth(username, password), json=add_sensor_query)

    if post_resp.status_code == 200:
        post_web = request('POST', url + '/ca/api/devices/pair/key/%s' % add_sensor_query['registrationKey'], verify=False, auth=HTTPBasicAuth(username, password))
        return add_sensor_query, post_resp, post_web, add_sensor_query['uuid']
    else:
        return add_sensor_query, post_resp, "N/A"


def add_hub(url, username, password, hub_name):
    uuid_end = b2a_hex(urandom(6)).decode("utf-8")

    add_hub_query = {
    "typeId" : "55d1a6d5e4b010f33a027cfd",
    "type" : "ACTIVE_HUB",
    "uuid" : "88888888-8888-8888-8888-%s" % uuid_end,
    "name" : hub_name,
    "registrationKey" : "regkey-" + ''.join(random.choice(string.digits) for _ in range(4)),
    "additionalIds" : {
        "values": {
        }
    }
    }
    post_resp = request('POST', url + '/ca/api/devices/', verify=False, auth=HTTPBasicAuth(username, password), json=add_hub_query)

    if post_resp.status_code == 200:
        post_web = request('POST', url + '/ca/api/devices/pair/key/%s' % add_hub_query['registrationKey'], verify=False, auth=HTTPBasicAuth(username, password))
        return add_hub_query, post_resp, post_web
    else:
        return add_hub_query, post_resp, "N/A"

# BASE PROGRAM