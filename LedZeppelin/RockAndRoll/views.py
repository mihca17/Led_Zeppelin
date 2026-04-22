from django.shortcuts import render
from .models import Reactor

# Create your views here.
def home(request):
    return render(request, 'RockAndRoll/home.html')

base = Reactor.objects.create(
    temperature = 100.0,
    water_level = 10.0,
    radiation = 100.0
)
