import json
from configparser import ConfigParser
import argparse
from datetime import date
import logging


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


def get_logger(server_name, check_name):
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