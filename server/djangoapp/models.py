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
class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip
    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self, dealership, id, name, purchase, review, car_make=None, car_model=None, car_year=None, purchase_date=None, sentiment="neutral"):
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.dealership = dealership
        self.id = id 
        self.name = name 
        self.purchase = purchase 
        self.purchase_date = purchase_date
        self.review = review 
        self.sentiment = sentiment 

    def __str__(self):
        return "Name: " + self.name + " Review: " + self.review