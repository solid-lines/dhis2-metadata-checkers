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
            url_resource = url_resource +filter
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

    PROGRAM_STAGES = "programStages"
    metadata_resources = get_resources_from_online(parent_resource=PROGRAM_STAGES, fields=["name","id","program[id,name]","programStageDataElements[dataElement]","programStageSections[dataElements]"], filter="filter=formType:eq:SECTION&filter=program:!null")
    
    programs = {}
    for programStage in metadata_resources[PROGRAM_STAGES]:
        program_uid = programStage["program"]["id"]
        program_name = programStage["program"]["name"]
        programStage_uid = programStage["id"]
        programStage_name = programStage["name"]
        programStageDataElements = [x["dataElement"]["id"] for x in programStage["programStageDataElements"]]
        programStageSectionsDE = list()
        for pss in programStage["programStageSections"]:
            programStageSectionsDE = programStageSectionsDE + [x["id"] for x in pss["dataElements"]]
        

        a = set(programStageDataElements)
        b = set(programStageSectionsDE)
 
        if a != b:
            logging.warning(f"The DE assigned to this Program Stage are not included in the program Stage Section. Check the programStage '{programStage_name}' ({programStage_uid}) of the program '{program_name}' ({program_uid})")
