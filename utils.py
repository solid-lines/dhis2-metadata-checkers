import json
from configparser import ConfigParser
import argparse
from datetime import date
import logging
import requests
from requests.auth import HTTPBasicAuth


def get_resources_from_file(resource, filename):
    with open(filename, 'r') as f:
        metadata = json.load(f)
        if resource in metadata:
            return {resource: metadata[resource]}
        else:
            return{resource: []}


def get_credentials():
    # Read args
    credentials_parser = argparse.ArgumentParser(description='Metadata validator')
    credentials_parser.add_argument('-c', '--credentials', action="store", dest="credentials_name", type=str, help='credentials name')
    args = credentials_parser.parse_args()

    if not args.credentials_name:
        args.credentials_name = "credentials_clone"
    
    # Obtain credentials
    credentials = {}
    parser = ConfigParser()
    parser.read("credentials.ini")
    params = parser.items(args.credentials_name)  # CHANGE select here your credentials
    
    for param in params:
        credentials[param[0]] = param[1]
    return credentials


def get_logger(credentials, check_name):
    
    server_name = credentials["server_name"]

    # Logging setup
    today = date.today().strftime("%Y-%m-%d")
    filename_log = today + "-"+server_name+"-"+check_name+".log"
    
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    # create file handler which logs error messages
    fh = logging.FileHandler(filename_log, encoding='utf-8')
    fh.setLevel(logging.WARN)
    # create console handler which logs even debug messages
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    # add the handlers to logger
    logger.addHandler(ch)
    logger.addHandler(fh)
    return logger


def get_resources_from_online(credentials, resource_type, fields='*', param_filter=None):
    
    server_url = credentials["server"]
    username = credentials["user"]
    password = credentials["password"]
    pagesize = credentials["page_size"]
        
    page = 0
    resources = {resource_type: []}
    data_to_query = True
    while data_to_query:
        page += 1
        url_resource = f"{server_url}{resource_type}.json?fields={fields}&pageSize={pagesize}&format=json&order=created:ASC&skipMeta=true&page={page}"
        if param_filter:
            url_resource = url_resource + "&" + param_filter
        logging.debug(url_resource)
        response = requests.get(url_resource, auth=HTTPBasicAuth(username, password))

        if response.ok:
            resources[resource_type].extend(response.json()[resource_type])
            if "pager" not in response.json():
                logging.warning(f"{resource_type} does not return a pager")
                data_to_query = False
            elif "nextPage" not in response.json()["pager"]:
                data_to_query = False
        else:
            # If response code is not ok (200), print the resulting http error code with description
            response.raise_for_status()

    return resources


def get_resource_from_online(credentials, resource_type, resource_uid, fields='*'):
    server_url = credentials["server"]
    username = credentials["user"]
    password = credentials["password"]
        
    url_resource = server_url+resource_type+"/"+resource_uid+".json?fields="+fields
    logging.debug(url_resource)
    response = requests.get(url_resource, auth=HTTPBasicAuth(username, password))
    return response.json()


def check_OK(credentials, url_resource_uid):
    logging.debug(url_resource_uid) 
    username = credentials["user"]
    password = credentials["password"]

    response = requests.get(url_resource_uid, auth=HTTPBasicAuth(username, password))

    if response.ok:
        return {"valid": True}
    else:
        # If response code is not ok (200), print the resulting http error code with description
        #response.raise_for_status()
        return {"valid": False, "response": response}
