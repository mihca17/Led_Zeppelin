import time

import requests
from config import Params
from abc import ABC, abstractmethod

parameters = Params()
team_id = parameters.team_id
print('start')
BaseURL = 'https://mephi.opentoshi.net/api/v1'
temperature_range = {'critical':1200,'mid':1180,'range': [1150,1300]}
water_range = {'critical':0,'mid':40,'range':[0,100]}
radiation_range = {'critical':150,'mid':120,'range':[100,250]}

class Reactor(abs):
    @abstractmethod
    def __init__(self):
        pass

    def get_data(self, id):
        url = f'{BaseURL}/reactor/data?team_id={id}'
        # print(url)
        connection = requests.get(url)
        self.data = connection.json()
        return self.data

    def create_reactor(self, id):
        # url = f'https://mephi.opentoshi.net/api/v1/reactor/create_reactor?team_id={id}'
        url = f'{BaseURL}/reactor/create_reactor?team_id={id}'
        connection = requests.post(url)
        data = connection.json()
        return data

class TemperatureSensor(Reactor):
    def __init__(self):


def register_team():
    # url = f'https://mephi.opentoshi.net/api/v1/team/register'
    url = f'{BaseURL}/team/register'
    connection = requests.get(url)
    data = connection.json()
    return data

def get_data(id):
    # url = f'https://mephi.opentoshi.net/api/v1/reactor/data?team_id={id}'
    url = f'{BaseURL}/reactor/data?team_id={id}'
    # print(url)
    connection = requests.get(url)
    data = connection.json()
    return data

def create_reactor(id):
    # url = f'https://mephi.opentoshi.net/api/v1/reactor/create_reactor?team_id={id}'
    url = f'{BaseURL}/reactor/create_reactor?team_id={id}'
    connection = requests.post(url)
    data = connection.json()
    return data

def reset_reactor(id):
    url = f'{BaseURL}/reactor/reset_reactor?team_id={id}'
    connection = requests.post(url)
    data = connection.json()
    return data

def refill_water(id, amount:float):
    url = f'{BaseURL}/reactor/refill-water?team_id={id}&amount={amount}'
    connection = requests.post(url)
    data = connection.json()
    return data

def emergency_shutdown(id):
    url = f'{BaseURL}/reactor/refill_water?team_id={id}'
    connection = requests.post(url)
    data = connection.json()
    return data

def activate_cooling(id, amount:int):
    url = f'{BaseURL}/reactor/activate_cooling?team_id={id}&amount={amount}'
    connection = requests.post(url)
    data = connection.json()
    return data

def get_history(id):
    url = f'{BaseURL}/reactor/history?team_id={id}'
    connection = requests.get(url)
    data = connection.json()
    return data

def get_temperature(data:dict):
    temperature = data.get('data').get('reactor_state').get('temperature')
    return temperature

def get_reactor_info(data:dict) -> dict:
    temperature = data.get('data').get('reactor_state').get('temperature')
    water_level = data.get('data').get('reactor_state').get('water_level')
    radiation = data.get('data').get('reactor_state').get('radiation')
    warnings = data.get('data').get('reactor_state').get('warnings')
    history = data.get('data').get('reactor_state').get('history')
    return {
        'temperature': temperature,
        'water_level': water_level,
        'radiation': radiation,
        'warnings': warnings,
        'history': history,
    }

# reset = reset_reactor(team_id)

data = get_data(team_id)

import asyncio
import aiohttp
print('monitor start')
async def monitor():
    async with aiohttp.ClientSession() as session: # соединение
        while True:
            id = team_id
            async with session.get(f'https://mephi.opentoshi.net/api/v1/reactor/data?team_id={id}') as response: # дополнили соединение конкретным url
                data = await response.json()
                print(data)
                print(f'RESULTS:'
                      f'\ntemperature: {get_reactor_info(data).get("temperature")}'
                      f'\nwater_level: {get_reactor_info(data).get("water_level")}'
                      f'\nradiation: {get_reactor_info(data).get("radiation")}')
            await asyncio.sleep(1)

asyncio.run(monitor())
print('monitor end')

print(f'RESULTS:'
      # f'\nteam_id: {team_id}'
      # f'\ncreate_reactor(team_id): {create_reactor(team_id)}'
      #   f'\nget_data(team_id): {data}'
      #   f'\ntemperature: {get_temperature(data)}'
      #   f'\nreset_reactor: {reset}'
      #   f'\nrefill_water: {refill_water(team_id, 10.0)}'
        f'\ninfo: {get_reactor_info(data)}'
        f'\ntemperature: {get_reactor_info(data).get("temperature")}'
        f'\nwater_level: {get_reactor_info(data).get("water_level")}'
        f'\nradiation: {get_reactor_info(data).get("radiation")}'
        f'\nhistory: {get_history(team_id)}')

# url = 'https://mephi.opentoshi.net/api/v1/team/register'
#
# connection = requests.get(url)
# answer = connection.text
#
# print(connection)
# print(answer)

