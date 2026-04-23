import asyncio

import aiohttp
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from .models import Reactor
import random
import requests
from .config import Params

parameters = Params()
team_id = parameters.team_id
BaseURL = 'https://mephi.opentoshi.net/api/v1'

def get_data(id):
    url = f'{BaseURL}/reactor/data?team_id={id}'
    connection = requests.get(url)
    data = connection.json()
    return data

data = get_data(team_id)
print(f'data: {data}')

def data_btn(request):
    return JsonResponse(get_data(team_id))

def get_temperature(data:dict):
    temperature = data.get('data').get('reactor_state').get('temperature')
    return temperature

def get_water(data:dict):
    temperature = data.get('data').get('reactor_state').get('water_level')
    return temperature

def get_radiation(data:dict):
    radiation = data.get('data').get('reactor_state').get('radiation')
    return radiation

# Create your views here.
def home(request):
    if request.method == "POST":
        print('home POST')
        if 'temp' in request.POST:
            print(f'TEMP: {get_temperature(get_data(team_id))}')
        elif 'water' in request.POST:
            print('WATER')
        elif 'rad' in request.POST:
            print('RAD')
        else:
            print('No')
    return render(request, 'RockAndRoll/home.html')

def temp_chart(request):
    data = {
        'data': {}
    }

    return JsonResponse(data)

TemperatureDataAll = []



class Storage():
    def __init__(self):
        self.temperature = []
        self.water = []
        self.rad = []

class Team():
    def __init__(self):
        self.data = get_data(team_id)

storage = Storage()
team = Team()

def chart(request):
    TemperatureData = storage.temperature
    data = get_data(team_id)
    temperature = get_temperature(data)
    if len(TemperatureData) < 10:
        print(f'TemperatureData -10 {TemperatureData}')
        TemperatureData.append(temperature)
    else:
        VarData = [None] * 10
        print(f'BEFORE TemperatureData +10 {TemperatureData}')
        print(f'BEFORE VarData +10 {VarData}')
        for i in range(len(TemperatureData)-1):
            VarData[i] = TemperatureData[i+1]
        VarData[len(TemperatureData)-1] = temperature
        print(f'VarData +10 {VarData}')
        # TemperatureData = VarData
        storage.temperature = VarData
        print(f'TemperatureData +10 {TemperatureData}')


    data = {
        'labels':['1','2','3','4','5','6','7','8','9','10'],
        'values':TemperatureData
    }
    return JsonResponse(data)

def chart2(request):
    WaterData = storage.water
    data = get_data(team_id)
    water = get_water(data)
    if len(WaterData) < 10:
        print(f'TemperatureData -10 {WaterData}')
        WaterData.append(water)
    else:
        VarData = [None] * 10
        print(f'BEFORE TemperatureData +10 {WaterData}')
        print(f'BEFORE VarData +10 {VarData}')
        for i in range(len(WaterData)-1):
            VarData[i] = WaterData[i+1]
        VarData[len(WaterData)-1] = water
        print(f'VarData +10 {VarData}')
        # TemperatureData = VarData
        storage.water = VarData
        print(f'TemperatureData +10 {WaterData}')


    data = {
        'labels':['1','2','3','4','5','6','7','8','9','10'],
        'values':WaterData
    }
    return JsonResponse(data)

def chart3(request):
    RadiationData = storage.rad
    data = get_data(team_id)
    radiation = get_radiation(data)
    if len(RadiationData) < 10:
        print(f'TemperatureData -10 {RadiationData}')
        RadiationData.append(radiation)
    else:
        VarData = [None] * 10
        print(f'BEFORE TemperatureData +10 {RadiationData}')
        print(f'BEFORE VarData +10 {VarData}')
        for i in range(len(RadiationData)-1):
            VarData[i] = RadiationData[i+1]
        VarData[len(RadiationData)-1] = radiation
        print(f'VarData +10 {VarData}')
        # TemperatureData = VarData
        storage.rad = VarData
        print(f'TemperatureData +10 {RadiationData}')


    data = {
        'labels':['1','2','3','4','5','6','7','8','9','10'],
        'values':RadiationData
    }
    return JsonResponse(data)