from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), # Оснвоной адрес
    path('api/data/', views.chart, name='chart'), #Обращения к функциям получения графиков
    path('api/data2/', views.chart2, name='chart2'),
    path('api/data3/', views.chart3, name='chart3'),
    # path('api/temp_btn', views.data_btn, name='data_btn'),
]