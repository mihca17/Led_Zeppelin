from django.db import models

# Create your models here.
class Reactor(models.Model):
    temperature = models.FloatField()
    water_level = models.FloatField()
    radiation = models.FloatField()

    def __str__(self):
        return self.__name__