import requests
import json
import os
# import related models here
from .models import DealerReview
from .models import CarDealer
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1 
from ibm_cloud_sdk_core.api_exception import ApiException

from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions

# Create a `get_request` to make HTTP GET requests

def get_request(url, **kwargs):
    
    # If argument contain API KEY
    api_key = kwargs.get("api_key")
    print("GET from {} ".format(url))
    try:
        if api_key:
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', api_key))
        else:
            # Call get method of requests library with URL and parameters
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")

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
        print("Response status:", response.status_code)
        print("Response body:", response.text)
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
    json_result = get_request(url)
    print("JSON RESULT",json_result)
    if json_result:
       
        for dealer_review in json_result['docs']:
            review_obj = DealerReview(dealership=dealer_review["dealership"],
                                   name=dealer_review["name"],
                                   purchase=dealer_review["purchase"],
                                   review=dealer_review["review"])
            if "id" in dealer_review:
                review_obj.id = dealer_review["id"]
            if "purchase_date" in dealer_review:
                review_obj.purchase_date = dealer_review["purchase_date"]
            if "car_make" in dealer_review:
                review_obj.car_make = dealer_review["car_make"]
            if "car_model" in dealer_review:
                review_obj.car_model = dealer_review["car_model"]
            if "car_year" in dealer_review:
                review_obj.car_year = dealer_review["car_year"]
            
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            print(review_obj.sentiment)
            results.append(review_obj)

    return results

def analyze_review_sentiments(text):
    api_key = "zZWqbYDNjfBNoZbBai3lNJ6ABB8N9nMBVm5hPC6s4gdn"
    url = "https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/33ac8d6e-2c2f-4f8b-b9e8-3d16696c857b"
    text_to_analyze = text
    version = '2020-08-01'
    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version=version,
        authenticator=authenticator
    )
    natural_language_understanding.set_service_url(url)

    if not text_to_analyze:
        return "No text for sentiment analysis"

    try:
        response = natural_language_understanding.analyze(
            text=text_to_analyze,
            features=Features(sentiment=SentimentOptions())
        ).get_result()

        sentiment_score = str(response["sentiment"]["document"]["score"])
        sentiment_label = response["sentiment"]["document"]["label"]
        sentiment_result = sentiment_label
        return sentiment_result

    except ApiException as e:
        if e.code == 422:
            return "Unable to analyze sentiment for the given text"
        else:
            return "Error analyzing sentiment: " + str(e)