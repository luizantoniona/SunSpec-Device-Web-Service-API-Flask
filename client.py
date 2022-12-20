import requests
import json
from requests.auth import HTTPBasicAuth

#HOST = "http://169.254.135.221"
HOST = 'http://127.0.0.1'
PORT = 5000
MODELS = "/models"
SUMMARY = "?summary="
INSTANCES = "/instances/"
POINTS = "?points="

endpoint = HOST + ":" + str(PORT) + MODELS

method = input("GET ou PATCH: ")

if method == "GET":
    summary = input("SUMMARY: ")
    if summary == "true":
        endpoint += SUMMARY + str(summary)
    else:
        model_id = input("MODEL_ID: ")
        model_instance = input("MODEL_INSTANCE: ")
        points = input("POINTS: ")

        endpoint += "/" + str(model_id) + INSTANCES + str(model_instance)

        if points != "":
            endpoint += POINTS + points

elif method == "PATCH":
    model_id = input("MODEL_ID: ")
    model_instance = input("MODEL_INSTANCE: ")
    
    endpoint += "/" + str(model_id) + INSTANCES + str(model_instance)

    points = list()

    point = " "
    while point != "":
        point = input("POINT TO ALTERAR: ")
        value = input("VALOR: ")

        if point == "" or value == "":
            continue

        points.append({str(point): value})

    payload = {
        "ID": model_id,
        "Pt": points
    }
else:
    pass

USERNAME = 'luiz'
PASSWORD = 'CHAVE_DE_ACESSO'

if method == 'PATCH':
    json_headers = {'Content-Type': 'application/json'}
    response = requests.patch(endpoint, headers=json_headers, data=json.dumps(payload), auth=HTTPBasicAuth(USERNAME, PASSWORD))
else:
    response = requests.get(endpoint, auth=HTTPBasicAuth(USERNAME, PASSWORD))


print(response)
if 'application/json' in response.headers.get('Content-Type', ''):
    print(response.json())
else:
    print(response.text)