#!/usr/bin/python
# -*- coding: UTF-8 -*-

from configparser import ConfigParser
import requests
from requests.auth import HTTPBasicAuth
from datetime import date, datetime
import logging
import os

PARENT_RESOURCE = "organisationUnits"
OPENING_DATE = "openingDate"
CLOSED_DATE = "closedDate"

##### Obtain credentials ####
credentials = {}
parser = ConfigParser()
parser.read("credentials.ini")
params = parser.items("credentials_clone") # CHANGE select here your credentials

for param in params:
    credentials[param[0]] = param[1]

SERVER_URL = credentials["server"]
SERVER_NAME = credentials["server_name"]
USERNAME = credentials["user"]
PASSWORD = credentials["password"]
PAGESIZE = credentials["page_size"]


##### Logging setup ####
today = date.today().strftime("%Y-%m-%d")
check_name = os.path.basename(__file__).replace(".py","")
FILENAME_LOG = today + "-"+SERVER_NAME+"-"+check_name+".log"

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
# create file handler which logs error messages
fh = logging.FileHandler(FILENAME_LOG, encoding='utf-8')
fh.setLevel(logging.ERROR)
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


################################################################################
    

def get_resources(resource_name, country_prefix=None):
    page = 0
    resources = { resource_name : [] }
    data_to_query = True
    while data_to_query:
        page += 1
        url_resource = SERVER_URL + resource_name + ".json?filter=closedDate:!null&fields=id,name,openingDate,closedDate&pageSize=" + str(PAGESIZE) + "&format=json&order=created:ASC&skipMeta=true&page=" + str(page)
        if country_prefix is not None:
            url_resource = url_resource + "&filter=name:like:"+country_prefix
        logging.debug(url_resource) 
        response = requests.get(url_resource, auth=HTTPBasicAuth(USERNAME, PASSWORD))

        if response.ok:
            resources[resource_name].extend(response.json()[resource_name])
            if ("nextPage" not in response.json()["pager"]):
                data_to_query = False
        else:
            # If response code is not ok (200), print the resulting http error code with description
            response.raise_for_status()

    return resources


################################################################################


if __name__ == "__main__":
    #retrieve all metadata_resources
    metadata_resources = get_resources(resource_name=PARENT_RESOURCE)
    
    #check condition
    #check if each organization unit has coherent dates    
    for orgUnit in metadata_resources[PARENT_RESOURCE]:
        closedDate = datetime.strptime(orgUnit[CLOSED_DATE],"%Y-%m-%dT%H:%M:%S.%f")
        openingDate = datetime.strptime(orgUnit[OPENING_DATE],"%Y-%m-%dT%H:%M:%S.%f")
        
        
        if closedDate > datetime.now():
            print("The organisationUnit "+ str(orgUnit["name"]) + "' (" + str(orgUnit["id"]) + ") has a closedDate in the future (later than today): "+str(closedDate))
            logging.error("The organisationUnit "+ str(orgUnit["name"]) + "' (" + str(orgUnit["id"]) + ") has a closedDate in the future (later than today): "+str(closedDate))

        if openingDate > closedDate:
            print("The organisationUnit "+ str(orgUnit["name"]) + "' (" + str(orgUnit["id"]) + ") has the opening date ("+str(openingDate)+") later than the closed date: ("+str(closedDate)+")")
            logging.error("The organisationUnit "+ str(orgUnit["name"]) + "' (" + str(orgUnit["id"]) + ") has the opening date ("+str(openingDate)+") later than the closed date: ("+str(closedDate)+")")