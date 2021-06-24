#!/usr/bin/python
# -*- coding: UTF-8 -*-

from configparser import ConfigParser
import requests
from requests.auth import HTTPBasicAuth
from datetime import date
import logging
import os
from collections import Counter

PARENT_RESOURCE = "optionSets"

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
        url_resource = SERVER_URL + parent_resource + ".json?fields=id,name,options[name,code]&pageSize=" + str(PAGESIZE) + "&format=json&order=created:ASC&skipMeta=true&page=" + str(page)
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
    #retrieve all metadata_resources
    metadata_resources = get_resources_from_online(parent_resource=PARENT_RESOURCE)


    for optionSet in metadata_resources[PARENT_RESOURCE]:
        metadata_url = SERVER_URL+PARENT_RESOURCE+"/"+optionSet["id"]+"?fields=*,options[*]"

        #check condition
        # all option's names that belong to a optionSet MUST be unique
        names = [o["name"]for o in optionSet["options"]]
        if len(names) != len(set(names)):
            d =  Counter(names)
            res = ["'"+k+"'" for k, v in d.items() if v > 1]
            message = "There are options in the optionSet "+ str(optionSet["name"]) + "' (" + str(optionSet["id"]) + ") with the same name. The duplicated names are ("+', '.join(res)+"). See "+metadata_url
            logging.error(message)
            
        # all option's codes that belong to a optionSet MUST be unique
        codes = [o["code"]for o in optionSet["options"]]
        if len(codes) != len(set(codes)):
            d =  Counter(codes)
            res = ["'"+k+"'" for k, v in d.items() if v > 1]
            message = "There are options in the optionSet "+ str(optionSet["name"]) + "' (" + str(optionSet["id"]) + ") with the same code. The duplicated codes are: ("+', '.join(res)+"). See "+metadata_url
            logging.error(message)