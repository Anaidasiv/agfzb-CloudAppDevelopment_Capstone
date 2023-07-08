from django.db import models
from django.utils.timezone import now


# Create your models here.

class CarMake(models.Model):
    name = models.CharField(null=False, max_length=50)
    description = models.CharField(null=True, max_length=500)

    def __str__(self):
        return self.name


class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, null=True, on_delete=models.CASCADE)
    name = models.CharField(null=False, max_length=50)
    dealer_id = models.IntegerField(null=True)
    SEDAN = "Sedan"
    SUV = "SUV"
    VAN="Van"
    WAGON = "Wagon"
    JEEP="Jeep"
    CHOICES = [(SEDAN, "Sedan"), (SUV, "SUV"),(VAN,"Van"),(WAGON, "wagon"),(JEEP,"Jeep")]
    types = models.CharField(null=False, max_length=15, choices=CHOICES)
    year = models.DateField()

    def __str__(self):
        return self.name + ", " + str(self.year) 

# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
