'''This module is responsible for containing interaction logic with our scanning api'''
from tokenize import String
import requests
import json
import env
import sys
import os

def test_connection() -> bool:
    '''Test if the API is available for requests'''
    print("Checking if our service is currently available...")

    try:
        request_url = env.get_scan_endpoint() + "scan/v1/status"

        print("Requesting server availability from: " + request_url)
        response = requests.get(request_url)
        if response.status_code == 200:
            print("Response on servers being up was:")
            print(response.text)
            payload = json.loads(response.text)

            if payload is not None and payload.get("SCAN_STATUS") == "Ok" and payload.get("DB_STATUS") == "Ok":
                print("Scanning API is available and database is available.")
                return True

        print("Some of our API endpoints are not available. Please try again later or check your internet connection and authentication token.")
        return False
    except requests.exceptions.ConnectionError:
        print("There was a failure attempting to connect to our servers. Please check your internet connection.")
        return False

def get_jwt_token(auth_token) -> String:
    '''Get the authentication token from the api'''

    if auth_token is None or auth_token == "":
        raise ValueError("The parameter auth_token cannot be empty")

    try:
        request_url = env.get_db_endpoint() + "db/v1/scan/login"
        response = requests.get(request_url, headers={"Authorization": "Token " + auth_token})

        if response.status_code == 200:
            print("Retrieved response while attempting to refresh JWT Token.")

            payload = json.loads(response.text)

            if payload is not None and payload.get("Token") != "":
                payload = json.loads(response.text)
                token_payload = payload.get("Token")

                if token_payload.get("Token") != "":
                    return token_payload.get("Token")

        print("Unknown status code while attempting to retrieve JWT Token. Response code was: " + str(response.status_code))
        return None
    except requests.exceptions.ConnectionError:
        print("Ran into connection error while attempting to connect with our API")
        return None

def post_result(jwt_token, work_result) -> bool:
    '''Get work from the API, returns status code and Image Data'''

    if work_result is None or work_result == "":
        raise ValueError("The parameter work_result cannot be empty")

    if jwt_token is None or jwt_token == "":
        raise ValueError("The parameter work_result cannot be empty")

    try:
        request_url = env.get_scan_endpoint() + "scan/v1/worker/post_result"
        response = requests.post(request_url, headers={"Authorization": "Bearer " + jwt_token}, data=work_result)

        if response.status_code == 200:
            return True

        print("Failed sending the result back to the scan api. Recieved error code: " + str(response.status_code))
        return False
    except requests.exceptions.ConnectionError:
        return False

def get_work(jwt_token):
    '''Get work from the API, returns status code and Image Data'''

    if jwt_token is None or jwt_token == "":
        raise ValueError("The parameter jwt_token cannot be empty")

    try:
        request_url = env.get_scan_endpoint() + "scan/v1/worker/get_work"
        response = requests.get(request_url, headers={"Authorization": "Bearer " + jwt_token})

        if response.status_code == 200:
            return response.status_code, response.text

        return response.status_code, None
    except requests.exceptions.ConnectionError:
        return None

