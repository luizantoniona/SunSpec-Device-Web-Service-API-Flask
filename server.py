import json
from flask import Flask
from flask import request

files = ['models/model_1.json', 'models/model_307.json', 'models/model_1_extra.json']

server_data = list()

for file in files:
    with open(file, 'r') as openned_file:
        server_data.append(json.load(openned_file)) 

server = Flask(__name__)

USERNAME = 'luiz'
PASSWORD = 'CHAVE_DE_ACESSO'

@server.get('/models/')
def models():

    if request.authorization.username != USERNAME or request.authorization.password != PASSWORD:
        return 'ERRO DE AUTENTICAÇÃO. USUARIO E SENHA INVALIDOS.', 401

    summary = request.args.get('summary', default="false", type=str)
    data_model_list = list()
    points_model_list = list()

    for group in server_data:
        if summary == "false":
            for point in group['group']['points']:
                if 'name' in point:
                    if 'value' in point:
                        points_model_list.append({
                            str(point['name']): point['value']
                        })

            data_model_list.append({
            "name": group['group']['name'],
            "ID": group['group']['id'],
            "points": points_model_list.copy()
        })
        
        else:    
            data_model_list.append({
                "name": group['group']['name'],
                "ID": group['group']['id'],
                'count': len(group['group']['points'])
            })

        points_model_list.clear()

    request_return = {
        "models": data_model_list
    }

    return request_return

@server.get('/models/<int:model_number>/instances/<int:instance_index>/')
def get_model(model_number, instance_index):

    if request.authorization.username != USERNAME or request.authorization.password != PASSWORD:
        return 'ERRO DE AUTENTICAÇÃO. USUARIO E SENHA INVALIDOS.', 401

    point_request = request.args.get('points', default="", type=str)
    points_request = point_request.split(',')

    models = list()

    for group in server_data:
        if group['group']['id'] == model_number:
            models.append(group)

    if instance_index > len(models):
        instance_index = len(models)

    data_model_list = list()
    points_model_list = list()        

    if len(models) <= 0:
        return 'BAD REQUEST, NO MODEL_ID!', 400
    
    group = models[instance_index - 1]

    for point in group['group']['points']:
        if point_request != "" and len(points_request) > 0:
            if 'name' in point and points_request.count(point['name']) > 0:
                if 'value' in point:
                    points_model_list.append({
                        str(point['name']): point['value']
                    })
        else:
            if 'name' in point:
                if 'value' in point:
                    points_model_list.append({
                        str(point['name']): point['value']
                    })
    
    data_model_list.append({
        "name": group['group']['label'],
        "ID": group['group']['id'],
        "information": points_model_list
    })

    request_return = {
        'models': data_model_list
    }

    return request_return

@server.patch('/models/<int:model_number>/instances/<int:instance_index>')
def patch_model_instance(model_number, instance_index):
    
    if request.authorization.username != USERNAME or request.authorization.password != PASSWORD:
        return 'ERRO DE AUTENTICAÇÃO. USUARIO E SENHA INVALIDOS.', 401

    request_data = request.json

    models = list()

    for group in server_data:
        if group['group']['id'] == model_number:
            models.append(group)

    if instance_index > len(models):
        instance_index = len(models)     

    if len(models) <= 0:
        return 'BAD REQUEST, NO MODEL_ID!', 400
    
    group = models[instance_index - 1]

    for point in group['group']['points']:
        for point_to_alter in request_data['Pt']:
            if point['name'] in point_to_alter.keys() :
                if 'static' in point:
                    return 'METHOD NOT ALLOWED, read-only', 405
                point['value'] = (point_to_alter[point['name']])

    return request_data

@server.route('/')
def opcoes():
    return 'SUNSPEC DEVICE SERVER - LUIZ ANTONIO NICOLAU ANGHINONI'