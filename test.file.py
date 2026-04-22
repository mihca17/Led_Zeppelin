import requests
from config import Params

parameters = Params()
team_id =parameters.team_id
print(team_id)

def get_data(id):
    url = f'https://mephi.opentoshi.net/api/v1/team/data?team_id={id}'
    connection = requests.get(url)
    data = connection.json()
    return data

def create_reactor(id):
    url = f'https://mephi.opentoshi.net/api/v1/reacor/create_reactor?team_id={id}'
    connection = requests.post(url)
    data = connection.json()
    return data

print(f'RESULTS:\nteam_id: {team_id}\nget_data(team_id): {get_data(team_id)}\ncreate_reactor(team_id): {create_reactor(team_id)}')

# url = 'https://mephi.opentoshi.net/api/v1/team/register'
#
# connection = requests.get(url)
# answer = connection.text
#
# print(connection)
# print(answer)

