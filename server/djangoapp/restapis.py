import requests
import json
import os
# import related models here
from .models import DealerReview
from .models import CarDealer
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1 
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions

# Create a `get_request` to make HTTP GET requests

def get_request(url, json_payload=None):
    print(json_payload)
    print("GET from {} ".format(url))
    response = None
    try:
        if json_payload:
            response = requests.get(url, headers={'Content-Type': 'application/json'}, params=json_payload)
        else:
            response = requests.get(url, headers={'Content-Type': 'application/json'})
        response.raise_for_status()  # Check for any HTTP errors
    except requests.exceptions.RequestException as e:
        print("Network exception occurred:", str(e))
        return {
            'statusCode': 500,
            'message': 'Network exception occurred'
        }
    
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    print(f"POST to {url}")
    try:
        response = requests.post(url, params=kwargs, json=json_payload)
    except:
        print("Error")
    status_code = response.status_code
    print(f"With status {status_code}")

    return response

# Create a get_dealers_from_cf method to get dealers from a cloud function
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result if isinstance(json_result, list) else []
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            #dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(
                address=dealer["address"],
                city=dealer["city"],
                full_name=dealer["full_name"],
                id=dealer["id"],
                lat=dealer["lat"],
                long=dealer["long"],
                short_name=dealer["short_name"],
                st=dealer["st"],
                zip=dealer["zip"]
            )
            results.append(dealer_obj)
    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list

def get_dealer_reviews_from_cf(url, dealer_id):
    results = []
    # Make a POST request to the cloud function URL with the dealer ID
    json_payload = {
        "id": dealer_id
    }
    json_result = get_request(url,json_payload)
    if json_result:
        # Get the row list in JSON as reviews
        reviews = json_result if isinstance(json_result, list) else []
        # For each review object
        for review in reviews:
            # Create a DealerReview object with values from the JSON
            review_obj = DealerReview(
                id=review["id"],
                name=review["name"],
                dealership=review["dealership"],
                review=review["review"],
                purchase=review["purchase"],
                purchase_date=review["purchase_date"],
                car_make=review["car_make"],
                car_model=review["car_model"],
                car_year=review["car_year"]
            )
            results.append(review_obj)
    return results
