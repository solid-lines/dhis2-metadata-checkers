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
    #read args
    credentials_parser = argparse.ArgumentParser(description='Metadata validator')
    credentials_parser.add_argument('-c', '--credentials', action="store", dest="credentials_name", type=str, help='credentials name')
    args = credentials_parser.parse_args()
    
    if not args.credentials_name:
        args.credentials_name = "credentials_clone"
    
    ##### Obtain credentials ####
    credentials = {}
    parser = ConfigParser()
    parser.read("credentials.ini")
    params = parser.items(args.credentials_name) # CHANGE select here your credentials
    
    for param in params:
        credentials[param[0]] = param[1]
    return credentials


def get_logger(credentials, check_name):
    
    server_name = credentials["server_name"]

    ##### Logging setup ####
    today = date.today().strftime("%Y-%m-%d")
    FILENAME_LOG = today + "-"+server_name+"-"+check_name+".log"
    
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    # create file handler which logs error messages
    fh = logging.FileHandler(FILENAME_LOG, encoding='utf-8')
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
    
    SERVER_URL = credentials["server"]
    USERNAME = credentials["user"]
    PASSWORD = credentials["password"]
    PAGESIZE = credentials["page_size"]
        
    page = 0
    resources = { resource_type : [] }
    data_to_query = True
    while data_to_query:
        page += 1
        url_resource = f"{SERVER_URL}{resource_type}.json?fields={fields}&pageSize={PAGESIZE}&format=json&order=created:ASC&skipMeta=true&page={page}"
        if param_filter:
            url_resource = url_resource + "&" + param_filter
        logging.debug(url_resource)
        response = requests.get(url_resource, auth=HTTPBasicAuth(USERNAME, PASSWORD))

        if response.ok:
            resources[resource_type].extend(response.json()[resource_type])
            if ("nextPage" not in response.json()["pager"]):
                data_to_query = False
        else:
            # If response code is not ok (200), print the resulting http error code with description
            response.raise_for_status()

    return resources

def get_resource_fields(credentials, resource, resourceUID, fields):
    SERVER_URL = credentials["server"]
    USERNAME = credentials["user"]
    PASSWORD = credentials["password"]
        
    urlSource = SERVER_URL+resource+"/"+resourceUID+".json?fields="+(",".join(fields))
    logging.debug(urlSource)
    response = requests.get(urlSource, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    return response.json()