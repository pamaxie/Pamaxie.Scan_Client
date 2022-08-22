'''Primary entry point for the application'''
from genericpath import isdir
import json
import time
from tokenize import String
import requests
import env
import sys
import os
import api_requests
from file_detection import image_detection

from tensorflow import keras
from keras.models import load_model

EXE_PATH = sys.path[0]

def login_api() -> String:
    '''Authenticates with our API and returns the JWT bearer Token()'''

    auth_token = env.get_api_token()
    api_requests.test_connection()
    return api_requests.get_jwt_token(auth_token)

def get_work_loop(jwt_token, safety_net_model, symbol_net_model):
    '''Start requesting work from our scanning api'''
    print("Entering primary work loop to check for scans. This will run indefinetly until we hit an error.")

    while True:
        time.sleep(0.2)
        work_result = api_requests.get_work(jwt_token)

        if work_result is None:
            continue

        if work_result[0] == 401:
            try:
                jwt_token = login_api()
            except ConnectionError:
                print("We could not connect to our database API. Please check that it's available.")
            finally:
                continue


        if work_result[0] == 408:
            continue

        if work_result[1] is None:
            continue

        print("Found some work and starting the detection for it.")

        payload = json.loads(work_result[1])

        if payload is None or payload == "":
            continue

        if payload.get("ImageHash") == "" or payload.get("ScanUrl") == "" or payload.get("DataType") == "" or payload.get("DataExtension") == "":
            continue

        image_hash = payload.get("ImageHash")
        scan_url = payload.get("ImageUrl")
        data_type = payload.get("DataType")
        data_extension = payload.get("DataExtension")

        if data_type == "image":
            print("Starting detection for image with hash: " + image_hash)
            scan_result = image_detection.detect_image(scan_url, data_extension, image_hash, safety_net_model, symbol_net_model)

            #Invalid or maleformed scan result means something went wrong during the process and we'll ignore this scan request for now
            if scan_result is None or scan_result == "":
                continue

            storage_result = api_requests.post_result(jwt_token, scan_result)

            if storage_result is None or storage_result == "":
                print("We encountered an error while attempting to store data. Please ensure the connection to the server is stable.")

        else:
            print("Recieved a data type that is unavailable to be scanned by this api. Please check for updates for this API endpoint.")

            #Exiting the system here to prevent wrongful polling of data that could cause harm.
            exit(-1)

print("Starting the validation of our required enviorement variables...")
env.check_env_vars()
print("Done validating environment variables.")
print("Loading ML Models")
ACTIVE_SAFETY_NET_MODEL_PATH = EXE_PATH + "/Models/SafetyNet"
ACTIVE_SYMBOL_NET_MODEL_PATH = EXE_PATH + "/Models/SymbolNet"

model = load_model(ACTIVE_SAFETY_NET_MODEL_PATH)
symbol_model = load_model(ACTIVE_SYMBOL_NET_MODEL_PATH)
print("Finished loading models")
print("Starting the application...")
jwt_token = login_api()

if jwt_token is None or jwt_token == "":
    print("Could not retrieve a valid jwt bearer token from our api. Please ensure your enviorement variables are correct. Exiting now...")
    exit(-1)

#Create our File Cache Folder if it doesn't exist
if not os.path.isdir(sys.path[0] + "/File_Cache"):
    os.makedirs(sys.path[0] + "/File_Cache")

get_work_loop(jwt_token, model, symbol_model)
