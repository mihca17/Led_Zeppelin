from django.http import JsonResponse
from django.shortcuts import render
from .models import Reactor
import random

# Create your views here.
def home(request):
    return render(request, 'RockAndRoll/home.html')

def chart(request):
    data = {
        'labels':['1','2','3','4','5','6','7','8','9'],
        'values':[random.randint(10,30) for _ in range(5)]
    }
    return JsonResponse(data)