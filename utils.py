import json
from configparser import ConfigParser
import argparse
from datetime import date
import logging
import requests
from requests.auth import HTTPBasicAuth
import collections


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
    fh.setLevel(logging.INFO)
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

def get_dhis2_version(credentials):
    server_url = credentials["server"]
    username = credentials["user"]
    password = credentials["password"]
        
    url_resource = f"{server_url}system/info"
    logging.debug(url_resource)
    response = requests.get(url_resource, auth=HTTPBasicAuth(username, password))
    if response.ok:
        return response.json()["version"]
    else:
        # If response code is not ok (200), print the resulting http error code with description
        logging.error(f"Please, double check this call: {url_resource}")
        response.raise_for_status()



def validate_generic_expression(credentials, expression):
    '''
    Uses the generic /api/expressions/description?expression=<expression-string> for validation
    '''
    server_url = credentials["server"]
    username = credentials["user"]
    password = credentials["password"]
        
    url_resource = f"{server_url}expressions/description?expression={requests.utils.quote(expression)}"
    logging.debug(url_resource)
    response = requests.get(url_resource, auth=HTTPBasicAuth(username, password))
    if response.ok:
        if response.json()["status"] == "ERROR":
            return response
        else:
            return None
    else:
        # If response code is not ok (200), print the resulting http error code with description
        logging.error(f"Please, double check this call: {url_resource}")
        response.raise_for_status()

    
def validate_expression(credentials, resource_type, type_expression, expression):
    server_url = credentials["server"]
    username = credentials["user"]
    password = credentials["password"]
        
    url_resource = f"{server_url}{resource_type}/{type_expression}/description"
    logging.debug(url_resource)
    response = requests.post(url_resource, data=expression, auth=HTTPBasicAuth(username, password))
    if response.ok:
        if response.json()["status"] == "ERROR":
            return response
        else:
            return None
    else:
        # If response code is not ok (200), print the resulting http error code with description
        logging.error(f"Please, double check this call: {url_resource}")
        response.raise_for_status()
    

def validate_pr_expression(credentials, resource_type, type_expression, program_id, expression):
    server_url = credentials["server"]
    username = credentials["user"]
    password = credentials["password"]
    logging.debug(expression)
        
    url_resource = f"{server_url}{resource_type}/{type_expression}/description?programId={program_id}"
    logging.debug(url_resource)
    response = requests.post(url_resource, data=expression, auth=HTTPBasicAuth(username, password))
    if response.ok:
        if response.json()["status"] == "ERROR":
            return response
        else:
            return None
    else:
        # If response code is not ok (200), print the resulting http error code with description
        logging.error(f"Please, double check this call: {url_resource} {expression}")
        #response.raise_for_status()


def validate_pra_expression(credentials, resource_type, type_expression, program_id, expression):
    server_url = credentials["server"]
    username = credentials["user"]
    password = credentials["password"]
        
    url_resource = f"{server_url}{resource_type}/{type_expression}/expression/description?programId={program_id}"
    logging.debug(url_resource)
    response = requests.post(url_resource, data=expression, auth=HTTPBasicAuth(username, password))
    if response.ok:
        if response.json()["status"] == "ERROR":
            return response
        else:
            return None
    elif response.status_code == 409:
        return response
    else:
        # If response code is not ok (200), print the resulting http error code with description
        logging.error(f"Please, double check this call: {url_resource}")
        response.raise_for_status()

def checkIfDuplicates(listOfElems):
    ''' Check if given list contains any duplicates '''
    if len(listOfElems) == len(set(listOfElems)):
        return False
    else:
        return True

def get_resources_from_online(credentials, resource_type, fields='*', param_filter=None):
    
    server_url = credentials["server"]
    username = credentials["user"]
    password = credentials["password"]
    pagesize = credentials["page_size"]
        
    page = 0
    resources = {resource_type: []}
    resources_id = []
    
    data_to_query = True
    while data_to_query:
        page += 1
        url_resource = f"{server_url}{resource_type}?fields={fields}&pageSize={pagesize}&format=json&order=created:ASC&skipMeta=true&format=json&page={page}"
        if param_filter:
            url_resource = url_resource + "&" + param_filter

        logging.debug(url_resource)
        response = requests.get(url_resource, auth=HTTPBasicAuth(username, password))

        if response.ok:
            resources[resource_type].extend(response.json()[resource_type])
            if resource_type not in["resources"]:
                resources_id.extend([x['id'] for x in response.json()[resource_type] if "id" in x])
                if checkIfDuplicates(resources_id):
                    logging.error(f"Duplicates in pagination ({resource_type}) = {[item for item, count in collections.Counter(resources_id).items() if count > 1]}")
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
        
    url_resource = server_url+resource_type+"/"+resource_uid+"?format=json&fields="+fields
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


def has_trailing_space(input_text):
    if len(input_text) != len(input_text.strip()):
        return True


def has_double_space(input_text):
    if "  " in input_text:
        return True


def has_parenthesis_extra_space(input_text):
    if "( " in input_text or " )" in input_text:
        return True


def has_parenthesis_extra_space_double(input_text):
    if " ( " in input_text or " ) " in input_text:
        return True


import re
def has_parenthesis_without_space(input_text):
    if re.search("[a-zA-Z]\([^sSd]", input_text):
        return True


def has_colon_at_end(input_text):
    if input_text and (len(input_text.strip()) > 0) and input_text.strip()[-1] == ':':
        return True


def empty_after_strip(input_text):
    if input_text and (len(input_text.strip()) == 0):
        return True


# server url includes /api/
def get_url_maintenance(server_url, resource_type, resource_id):
    if resource_type == "dataSets-dataEntryForms":
        return f"{server_url.replace('/api/','')}/dhis-web-maintenance/index.html#/edit/dataSetSection/dataSet/{resource_id}/dataEntryForm"
    if resource_type == "dataSets":
        return f"{server_url.replace('/api/','')}/dhis-web-maintenance/index.html#/edit/dataSetSection/dataSet/{resource_id}"
    if resource_type == "dataElements":
        return f"{server_url.replace('/api/','')}/dhis-web-maintenance/index.html#/edit/dataElementSection/dataElement/{resource_id}"
    if resource_type == "programs" or resource_type == "programStages":
        return f"{server_url.replace('/api/','')}/dhis-web-maintenance/index.html#/edit/programSection/program/{resource_id}"
    if resource_type == "indicators":
        return f"{server_url.replace('/api/','')}/dhis-web-maintenance/index.html#/edit/indicatorSection/indicator/{resource_id}"
    if resource_type == "programIndicators":
        return f"{server_url.replace('/api/','')}/dhis-web-maintenance/index.html#/edit/indicatorSection/programIndicator/{resource_id}"
    if resource_type == "programRules":
        return f"{server_url.replace('/api/','')}/dhis-web-maintenance/index.html#/edit/programSection/programRule/{resource_id}"


# server url includes /api/
def get_url_api(server_url, resource_type, resource_id):
    return server_url+resource_type+"/"+resource_id
