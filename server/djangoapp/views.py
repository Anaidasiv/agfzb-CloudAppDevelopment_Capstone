from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel, CarMake, CarDealer, DealerReview
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

from . import models
from . import restapis

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
def about(request):
    context = {}
    return render(request, 'djangoapp/about.html', context)


def contact(request):
    context = {}
    return render(request, 'djangoapp/contact.html', context)
    

def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            user.is_superuser = True
            user.is_staff=True
            user.save()  
            login(request, user)
            return redirect("djangoapp:index")
        else:
            messages.warning(request, "The user already exists.")
            return redirect("djangoapp:registration")


def login_request(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            #messages.success(request, "Login successfully!")
            return redirect('djangoapp:index')
        else:
            messages.warning(request, "Invalid username or password.")
            return redirect("djangoapp:index")


def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')


def get_dealerships(request):
    if request.method == "GET":
        context = {}
        url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/e81514e9-de36-4069-8e3b-01724008e3b0/dealership-package/get-dealership"
        dealerships = get_dealers_from_cf(url)
        context["dealerships"] = dealerships
        return render(request, 'djangoapp/index.html', context)


def get_dealer_details(request,dealer_id):
    if request.method == "GET":
        context = {}
        review_url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/e81514e9-de36-4069-8e3b-01724008e3b0/dealership-package/get-review"
        reviews = get_dealer_reviews_from_cf(review_url,dealer_id=dealer_id)
        print(reviews)
        context["reviews"] = reviews
        
        return render(request, 'djangoapp/dealer_details.html', context)

def add_review(request, dealer_id):
    print("add_review function called")
    if request.method == "GET":
        dealersid = dealer_id
        url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/e81514e9-de36-4069-8e3b-01724008e3b0/dealership-package/get-dealership"
        # Get dealers from the URL
        context = {
            "cars": models.CarModel.objects.all(),
            "dealers": restapis.get_dealers_from_cf(url),
        }
        return render(request, 'djangoapp/add_review.html', context)
    
    if request.method == "POST":
        if request.user.is_authenticated:
            form = request.POST
            review = {
                "name": f"{request.user.first_name} {request.user.last_name}",
                "dealership": dealer_id,
                "review": form["content"],
                "purchase": form.get("purchasecheck"),
            }
            if form.get("purchasecheck"):
                review["purchase_date"] = datetime.strptime(form.get("purchasedate"), "%m/%d/%Y").isoformat()
                car = models.CarModel.objects.get(pk=form["car"])
                review["car_make"] = car.carmake.name
                review["car_model"] = car.name
                review["car_year"] = car.year.strftime("%Y")
            json_payload = {"review": review}
            print(json_payload)
            url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/e81514e9-de36-4069-8e3b-01724008e3b0/dealership-package/post-review"
            restapis.post_request(url, json_payload, dealerId=dealer_id)
            return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
        else:
            return redirect("/djangoapp/login")
