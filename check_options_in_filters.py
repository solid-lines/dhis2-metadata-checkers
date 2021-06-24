#!/usr/bin/python
# -*- coding: UTF-8 -*-

from configparser import ConfigParser
import requests
from requests.auth import HTTPBasicAuth
from datetime import date
import logging
import os

PARENT_RESOURCES = ["eventReports", "eventCharts"]

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


def get_resources_from_online(parent_resource, country_prefix=None):
    page = 0
    resources = { parent_resource : [] }
    data_to_query = True
    while data_to_query:
        page += 1
        url_resource = SERVER_URL + parent_resource + ".json?fields=id,name,dataElementDimensions&pageSize=" + str(PAGESIZE) + "&format=json&order=created:ASC&skipMeta=true&page=" + str(page)
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


def get_resource_from_online(resource_type, resource_uid, fields='*'):
    url_resource = SERVER_URL + resource_type + "/" + resource_uid+".json?fields="+fields
    logging.debug(url_resource)
    response = requests.get(url_resource, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    if response.ok:
        return response.json()
    else:
        # If response code is not ok (200), print the resulting http error code with description
        response.raise_for_status()


################################################################################

if __name__ == "__main__":
    for PARENT_RESOURCE in PARENT_RESOURCES:
        #retrieve all metadata_resources
        metadata_resources = get_resources_from_online(parent_resource=PARENT_RESOURCE)
        
        logger.info(f'Retrieved {len(metadata_resources[PARENT_RESOURCE])} {PARENT_RESOURCE}')
        for eventReportChart in metadata_resources[PARENT_RESOURCE]:
            flag = False
            issues = []
            metadata_url = SERVER_URL+PARENT_RESOURCE+"/"+eventReportChart["id"]+"?fields=*,options[*]"
    
            if (len(eventReportChart["dataElementDimensions"]) > 0):
                for dataElementDimension in eventReportChart["dataElementDimensions"]:
                    if "filter" in dataElementDimension:
                        filter_dhis2 = dataElementDimension["filter"]
                        dataElementUid = dataElementDimension["dataElement"]["id"]
                        dataElement = get_resource_from_online("dataElements", dataElementUid, fields='valueType,optionSetValue,optionSet')
                        if dataElement["optionSetValue"]:
                            options_raw = get_resource_from_online("optionSets", dataElement["optionSet"]["id"], fields="options[code]")
                            options = [x["code"] for x in options_raw["options"]]
                            
                            #Check if the options present in the filter are valid options
                            options_in_filter = filter_dhis2[3:].split(";") # Removing 'IN:' and convert to array
                            for option_in_filter in options_in_filter:
                                if option_in_filter not in options:
                                    flag = True
                                    issues.append(f"The option '{option_in_filter}' is in the filter but not in the options of the optionSet ({dataElement['optionSet']['id']}): {options}")
            if flag:
                logger.error(f"Issue/s in filter of {PARENT_RESOURCE} '{eventReportChart['name']}' ({eventReportChart['id']}). See{metadata_url}")
                for issue in issues:
                    logger.error(issue)
                logger.error("------------------")

