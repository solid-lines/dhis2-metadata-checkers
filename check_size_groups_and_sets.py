#!/usr/bin/python
# -*- coding: UTF-8 -*-

from configparser import ConfigParser
import requests
from requests.auth import HTTPBasicAuth
from datetime import date
import logging
import os

PARENT_RESOURCE = "programs"
CHILD_RESOURCE = "trackedEntityType" # Watch out singular and plural.

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


def get_resources_from_online(parent_resource, child_resource, country_prefix=None):
    page = 0
    resources = { parent_resource : [] }
    data_to_query = True
    while data_to_query:
        page += 1
        url_resource = SERVER_URL + parent_resource + "?fields=id,name,"+child_resource+"::size&pageSize=" + str(PAGESIZE) + "&format=json&order=created:ASC&skipMeta=true&page=" + str(page)
        if country_prefix is not None:
            url_resource = url_resource + "&filter=name:like:"+country_prefix
        logging.debug(url_resource) 
        response = requests.get(url_resource, auth=HTTPBasicAuth(USERNAME, PASSWORD))

        if response.ok:
            resources[parent_resource].extend(response.json()[parent_resource])
            if ("nextPage" not in response.json()["pager"]):
                data_to_query = False
        else:
            # If response code is not ok (200), print the resulting http error code with description
            response.raise_for_status()

    return resources


################################################################################

if __name__ == "__main__":

    groups = {
        "programIndicatorGroups": "programIndicators",
        "dataElementGroups" : "dataElements",
        "programTrackedEntityAttributeGroups": "programTrackedEntityAttributes",
        "indicatorGroups" : "indicators",
        "validationRuleGroups" : "validationRules",
        "predictorGroups": "predictors",
        "categoryOptionGroups": "categoryOptions",
        "organisationUnitGroups": "organisationUnits",
        "userGroups": "users",
        "optionGroups": "options",
    
        "categories": "categoryOptions",
        
        "indicatorGroupSets": "indicatorGroups",
        "organisationUnitGroupSets": "organisationUnitGroups",
        "optionSets": "options",
        "legendSets": "legends",
        "dataElementGroupSets": "dataElementGroups",
        "categoryOptionGroupSets": "categoryOptionGroups",
        "dataSets": "dataSetElements",
        "colorSets": "colors",
        "optionGroupSets": "optionGroups"
        }
    
    
    for k,v in groups.items():
        #retrieve all metadata_resources
        response = get_resources_from_online(parent_resource=k, child_resource=v)
        for group in response[k]:
            #check condition
            if (group[v] <= 1):
                metadata_url = SERVER_URL+k+"/"+group["id"]
                message = "The "+ k +" "+ str(group["name"]) + "' (" + str(group["id"]) + ") has not the expected number of "+v + " (size obtained="+str(group[v])+"). See "+metadata_url
                logging.error(message)
     
    
    expected_one = {
        "dataElements" : "dataSetElements",
    }
    
    for k,v in expected_one.items():
        #retrieve all metadata_resources
        response = get_resources_from_online(parent_resource=k, child_resource=v)
        for group in response[k]:
            #check condition
            if (group[v] > 1):
                metadata_url = SERVER_URL+k+"/"+group["id"]
                message = "The "+ k +" "+ str(group["name"]) + "' (" + str(group["id"]) + ") has not the expected number of "+v + " (size obtained="+str(group[v])+"). See "+metadata_url
                logging.error(message)
