import requests
from config import Params

parameters = Params()
team_id =parameters.team_id

def register_team():
    url = f'https://mephi.opentoshi.net/api/v1/team/register'
    connection = requests.get(url)
    data = connection.json()
    return data

def get_data(id):
    url = f'https://mephi.opentoshi.net/api/v1/reactor/data?team_id={id}'
    print(url)
    connection = requests.get(url)
    data = connection.json()
    return data

def create_reactor(id):
    url = f'https://mephi.opentoshi.net/api/v1/reactor/create_reactor?team_id={id}'
    connection = requests.post(url)
    data = connection.json()
    return data

print(f'RESULTS:'
      # f'\nteam_id: {team_id}'
      # f'\ncreate_reactor(team_id): {create_reactor(team_id)}'
      f'\nget_data(team_id): {get_data(team_id)}')

# url = 'https://mephi.opentoshi.net/api/v1/team/register'
#
# connection = requests.get(url)
# answer = connection.text
#
# print(connection)
# print(answer)

