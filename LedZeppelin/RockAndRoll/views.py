import asyncio

import aiohttp
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from .models import Reactor
import random
import requests
from .config import Params

parameters = Params() #Объект параметров команды
team_id = parameters.team_id #Айди команды
BaseURL = 'https://mephi.opentoshi.net/api/v1'

#Регистрация новой команды
def register_team():
    url = f'{BaseURL}/team/register'
    connection = requests.get(url)
    data = connection.json()
    return data

#Получение инфомарции о команде
def get_data(id):
    url = f'{BaseURL}/reactor/data?team_id={id}'
    connection = requests.get(url)
    data = connection.json()
    return data

#Создать новый реактор
def create_reactor(id):
    url = f'{BaseURL}/reactor/create_reactor?team_id={id}'
    connection = requests.post(url)
    data = connection.json()
    return data

#Перезапустить реактор
def reset_reactor(id):
    url = f'{BaseURL}/reactor/reset_reactor?team_id={id}'
    connection = requests.post(url)
    data = connection.json()
    return data

#Наполнить воду
def refill_water(id, amount:float):
    url = f'{BaseURL}/reactor/refill-water?team_id={id}&amount={amount}'
    connection = requests.post(url)
    data = connection.json()
    return data

#Внезапная остановка
def emergency_shutdown(id):
    url = f'{BaseURL}/reactor/emergency-shutdown?team_id={id}'
    connection = requests.post(url)
    data = connection.json()
    return data

#Охлаждение
def activate_cooling(id, amount:int):
    url = f'{BaseURL}/reactor/activate-cooling?team_id={id}&amount={amount}'
    connection = requests.post(url)
    data = connection.json()
    return data

#Получить историю
def get_history(id):
    url = f'{BaseURL}/reactor/history?team_id={id}'
    connection = requests.get(url)
    data = connection.json()
    return data

#Три основные функции получения температуры, уровня воды и радиации:

def get_temperature(data:dict):
    temperature = data.get('data').get('reactor_state').get('temperature')
    return temperature

def get_water(data:dict):
    temperature = data.get('data').get('reactor_state').get('water_level')
    return temperature

def get_radiation(data:dict):
    radiation = data.get('data').get('reactor_state').get('radiation')
    return radiation

# Это наша основная функция, генерации главной страницы:
def home(request):
    print(f'request {request}')
    if request.method == "POST":
        # print('home POST')
        if 'reset' in request.POST:
            reset_reactor(team_id)
            print('RESET')
        elif 'cooling' in request.POST:
            activate_cooling(team_id, 10)
        elif 'shutdown' in request.POST:
            emergency_shutdown(team_id)
        elif 'refill' in request.POST:
            refill_water(team_id, 10.0)
        else:
            print('Error')
    return render(request, 'RockAndRoll/home.html')

def temp_chart(request):
    data = {
        'data': {}
    }

    return JsonResponse(data)

class Storage(): # Хранит промежуточные данные
    def __init__(self):
        self.temperature = []
        self.water = []
        self.rad = []

class Team(): #Чтобы несколько раз не искать информацию, сохраним его в объект
    def __init__(self):
        self.data = get_data(team_id)

storage = Storage()
team = Team()

def chart(request): #График номер 1. Темпераутра. автоматическое регулирование
    TemperatureData = storage.temperature
    data = get_data(team_id)
    temperature = get_temperature(data)

    if len(TemperatureData) < 20:
        TemperatureData.append(temperature)
    else:
        VarData = [None] * 20
        for i in range(len(TemperatureData)-1):
            VarData[i] = TemperatureData[i+1]
        VarData[len(TemperatureData)-1] = temperature
        # TemperatureData = VarData
        storage.temperature = VarData
    if temperature >= 1200:
        activate_cooling(team_id, 10)

    data = {
        'labels':['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20'],
        'values':TemperatureData
    }

    print(f'Temp {temperature}')
    return JsonResponse(data)

def chart2(request):
    WaterData = storage.water
    data = get_data(team_id)
    water = get_water(data)
    if len(WaterData) < 20:
        WaterData.append(water)
    else:
        VarData = [None] * 20
        for i in range(len(WaterData)-1):
            VarData[i] = WaterData[i+1]
        VarData[len(WaterData)-1] = water
        storage.water = VarData
    print(f'Water LEVEL {water}')
    if water <= 40:
        print('WATER~~~~~')
        activate_cooling(team_id, 50)

    data = {
        'labels':['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20'],
        'values':WaterData
    }
    print(f'Water {water}')
    return JsonResponse(data)

def chart3(request):
    RadiationData = storage.rad
    data = get_data(team_id)
    radiation = get_radiation(data)
    if len(RadiationData) < 20:
        RadiationData.append(radiation)
    else:
        VarData = [None] * 20
        for i in range(len(RadiationData)-1):
            VarData[i] = RadiationData[i+1]
        VarData[len(RadiationData)-1] = radiation
        storage.rad = VarData
    if radiation > 150:
        activate_cooling(team_id, 150)

    data = {
        'labels':['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20'],
        'values':RadiationData
    }

    print(f'Rad {radiation}')
    return JsonResponse(data)


def data_btn(request):
    return JsonResponse(get_data(team_id))