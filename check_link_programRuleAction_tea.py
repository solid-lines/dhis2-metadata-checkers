#!/usr/bin/python
# -*- coding: UTF-8 -*-

from configparser import ConfigParser
import requests
from requests.auth import HTTPBasicAuth
from datetime import date
import logging
import os

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


def get_resources_from_online(parent_resource, fields='*', filter=None):
    page = 0
    resources = { parent_resource : [] }
    data_to_query = True
    while data_to_query:
        page += 1
        url_resource = SERVER_URL + parent_resource + ".json?fields="+(','.join(fields))+"&pageSize=" + str(PAGESIZE) + "&format=json&order=created:ASC&skipMeta=true&page=" + str(page)
        if filter:
            url_resource = url_resource + "&filter="+filter
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

def get_resource_fields(resource, resourceUID, fields):
    urlSource = SERVER_URL+resource+"/"+resourceUID+".json?fields="+(",".join(fields))
    logging.debug(urlSource)
    response = requests.get(urlSource, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    return response.json()


################################################################################


if __name__ == "__main__":


    PROGRAMS = "programs"
    metadata_resources = get_resources_from_online(parent_resource=PROGRAMS, fields=["name","id","programTrackedEntityAttributes[trackedEntityAttribute[id,name]]", "trackedEntityType[id,name,trackedEntityTypeAttributes[trackedEntityAttribute[id,name]]]"], filter=None)
    
    programs = {}
    for program in metadata_resources[PROGRAMS]:
        program_uid = program["id"]
        programs[program_uid] = { "name": program["name"], "teas": []}
        teas = program["programTrackedEntityAttributes"]
        if "trackedEntityType" in program:
            teas = teas + program["trackedEntityType"]["trackedEntityTypeAttributes"]
        for tea in teas:
            programs[program_uid]["teas"].append(tea["trackedEntityAttribute"]["id"])
    
    
    PROGRAM_RULES = "programRules"
    program_rules = get_resources_from_online(parent_resource=PROGRAM_RULES, fields=["name","id","program[id,name]", "programRuleActions[trackedEntityAttribute[id,name]]"], filter=None)
    
    for program_rule in program_rules[PROGRAM_RULES]:
        program_uid = program_rule["program"]["id"]
        for pra in program_rule["programRuleActions"]:
            if "trackedEntityAttribute" in pra and pra["trackedEntityAttribute"]["id"] not in programs[program_uid]["teas"]:
                logging.error(f"Program Rule '{program_rule['name']}' ({program_rule['id']}) in the PR Action uses a TEA '{pra['trackedEntityAttribute']['name']}' ({pra['trackedEntityAttribute']['id']}) that does not belong to the associated program '{program_rule['program']['name']}' or the TET")
