'''This module is responsible for handling enviorement variables and validating they are set'''

import os
import sys
from tokenize import String

PAM_API_TOKEN_ENV = "PAM_API_TOKEN"
PAM_API_ENDPOINT_ENV = "PAM_SCAN_ENDPOINT"
PAM_DB_ENDPOINT_ENV = "PAM_DB_ENDPOINT"
RUNS_IN_DOCKER_ENV = "PYTHON_RUNS_IN_DOCKER"

def check_env_vars() -> None:
    '''Checking if the required env variables are set'''
    error_message = ""

    api_token_err =  validate_env_var(PAM_API_TOKEN_ENV)

    if api_token_err is not None:
        error_message += api_token_err

    api_endpoint_err = validate_env_var(PAM_API_ENDPOINT_ENV)

    if api_endpoint_err is not None:
        error_message += api_endpoint_err

    db_endpoint_err = validate_env_var(PAM_DB_ENDPOINT_ENV)

    if db_endpoint_err is not None:
        error_message += db_endpoint_err

    if error_message.strip() is not "":
        print(error_message)
        sys.exit(1)

def validate_env_var(env_name) -> None:
    '''Attempts to validate a enviorement variable and returns an error message if it cannot set it'''

    if env_name is None or env_name == "":
        raise ValueError("The parameter env_name cannot be empty")
    
    env_value = os.environ.get(env_name)

    if env_value == "" or env_value is None:

        if not runs_in_docker():
            print(env_name, " is not set. Do you want to set the environment variable now (Y/n)?")
            answer = input()

            if answer.strip() == "" or answer.strip().upper() == "Y":
                try_setting_env(env_name)
                return None

        return env_name + " is not set, which is required to start the application. Please set it before attempting to start again."

    return None

def try_setting_env(env_name) -> bool:
    '''Try setting the enviorement variable for application if it hasn't been set yet directly'''

    if env_name is None or env_name is "":
        raise ValueError("The parameter env_name cannot be empty")

    while True:
        print("Please enter the value for", env_name, ":")
        answer = input()

        if answer.strip() is "" or (env_name is PAM_API_TOKEN_ENV and not answer.__contains__("PamToken")):
            print("Entered invalid or empty value. Do you want to try again? (Y/n)")
            answer = input()

            if answer.strip.upper() == "N":
                return False

        os.environ[env_name] = answer
        return True

def runs_in_docker() -> bool:
    '''Check if the service is running in docker'''
    return os.environ.get(RUNS_IN_DOCKER_ENV) == "True" or os.environ.get('PYTHON_RUNS_IN_DOCKER') == "1"

def get_api_token() -> String:
    '''Getting the API token via the env variable'''
    return os.environ.get(PAM_API_TOKEN_ENV)

def get_db_endpoint() -> String:
    '''Getting the API token via the env variable'''
    return os.environ.get(PAM_DB_ENDPOINT_ENV)

def get_scan_endpoint() -> String:
    '''Getting the API token via the env variable'''
    return os.environ.get(PAM_API_ENDPOINT_ENV)
