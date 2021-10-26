#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import utils


if __name__ == "__main__":

    credentials = utils.get_credentials()    
    check_name = os.path.basename(__file__).replace(".py", "")
    logger = utils.get_logger(credentials, check_name)
    server_url = credentials["server"]
    
################################################################################
     
    # since 2.29
        
    RESOURCE_TYPE = "indicators"
       
    
    logger.info(f"Processing resource type: {RESOURCE_TYPE}")
    try:
        response = utils.get_resources_from_online(credentials=credentials, resource_type=RESOURCE_TYPE, fields='id,name,numerator,denominator', param_filter=None)
    except Exception as e: 
        logger.error(f"Error while processing resource type: {RESOURCE_TYPE}")
        logger.error(e)
        response[RESOURCE_TYPE] = {}
              
    for resource in response[RESOURCE_TYPE]:       
        logger.debug(f"Check I={resource['id']}")
        url_ui = utils.get_url_maintenance(server_url, RESOURCE_TYPE, resource['id'])

        EXPRESSION_NAME = "numerator"
        validation_numerator = utils.validate_expression(credentials, RESOURCE_TYPE, "expression", expression=resource[EXPRESSION_NAME])
        if validation_numerator:
            logger.error(f"Expression problem. Double check the numerator of the I '{resource['name']}' ({resource['id']}). Response {validation_numerator.json()}. See {url_ui}" )
 
        EXPRESSION_NAME = "denominator"
        validation_denominator = utils.validate_expression(credentials, RESOURCE_TYPE, "expression", expression=resource[EXPRESSION_NAME])
        if validation_denominator:
            logger.error(f"Expression problem. Double check the denominator of the I '{resource['name']}' ({resource['id']}). Response {validation_denominator.json()}. See {url_ui}" )

      
################################################################################
     
    # since 2.29
            
    RESOURCE_TYPE = "programIndicators"
    
    logger.info(f"Processing resource type: {RESOURCE_TYPE}")
    try:
        response = utils.get_resources_from_online(credentials=credentials, resource_type=RESOURCE_TYPE, fields='id,name,expression,filter,program[id,name]', param_filter=None)
    except Exception as e: 
        logger.error(f"Error while processing resource type: {RESOURCE_TYPE}")
        logger.error(e)
        response[RESOURCE_TYPE] = {}


    for resource in response[RESOURCE_TYPE]:
            
        EXPRESSION_NAME = "expression"
        if EXPRESSION_NAME in resource: 
            validation_expression = utils.validate_expression(credentials, RESOURCE_TYPE, EXPRESSION_NAME, expression=resource[EXPRESSION_NAME])
            if validation_expression:
                logger.error(f"Expression problem. Double check the expression of the PI '{resource['name']}' ({resource['id']}) from Program '{resource['program']['name']}' ({resource['program']['id']}). Response {validation_expression.json()}" )
        else:
            logger.error(f"PI '{resource['name']}' ({resource['id']}) from Program '{resource['program']['name']}' ({resource['program']['id']}) without expression" )
    
    
        EXPRESSION_NAME = "filter"
        if EXPRESSION_NAME in resource: 
            validation_filter = utils.validate_expression(credentials, RESOURCE_TYPE, EXPRESSION_NAME, expression=resource[EXPRESSION_NAME])
            if validation_filter:
                logger.error(f"Expression problem. Double check the filter of the PI '{resource['name']}' ({resource['id']}) from Program '{resource['program']['name']}' ({resource['program']['id']}). Response {validation_filter.json()}" )
   
   
################################################################################
    
    # since 2.35
   
    dhis2_version = utils.get_dhis2_version(credentials)
    dhis2_version_detail = int(dhis2_version.split(".")[1])

    
    if dhis2_version_detail >= 35:
        
        RESOURCE_TYPE = "programRules"
        EXPRESSION_NAME = "condition"        
       
        logger.info(f"Processing resource type: {RESOURCE_TYPE}")
        try:
            response = utils.get_resources_from_online(credentials=credentials, resource_type=RESOURCE_TYPE, fields='id,name,program[id,name],condition,data', param_filter=None)
        except Exception as e: 
            logger.error(f"Error while processing resource type: {RESOURCE_TYPE}")
            logger.error(e)
            response[RESOURCE_TYPE] = {}


        for resource in response[RESOURCE_TYPE]:
            validation_condition = utils.validate_pr_expression(credentials, RESOURCE_TYPE, EXPRESSION_NAME, program_id=resource['program']['id'], expression=resource[EXPRESSION_NAME])
            if validation_condition:
                logger.error(f"Expression problem. Double check the {EXPRESSION_NAME} of the PR '{resource['name']}' ({resource['id']}) from Program '{resource['program']['name']}' ({resource['program']['id']}). Response {validation_condition.json()}" )
    else:
        logger.info(f"Skip Program Rules validation because the dhis2 version instance is lower than 2.35 ({dhis2_version})" )   
            

    # since 2.37
    
    if dhis2_version_detail >= 37:
        
        RESOURCE_TYPE = "programRuleActions"
        EXPRESSION_NAME = "data"
       
        logger.info(f"Processing resource type: {RESOURCE_TYPE}")
        try:
            response = utils.get_resources_from_online(credentials=credentials, resource_type=RESOURCE_TYPE, fields='id,name,programRule[id,name,program[id,name]],data', param_filter=None)
        except Exception as e: 
            logger.error(f"Error while processing resource type: {RESOURCE_TYPE}")
            logger.error(e)
            response[RESOURCE_TYPE] = {}

        for resource in response[RESOURCE_TYPE]:
            if EXPRESSION_NAME in resource:
                validation_rule_action = utils.validate_pra_expression(credentials, RESOURCE_TYPE, EXPRESSION_NAME, program_id=resource['programRule']['program']['id'], expression=resource[EXPRESSION_NAME])
                if validation_rule_action is not None:
                    logger.error(f"Expression problem. Double check the PRA ({resource['id']}) of PR '{resource['programRule']['name']}' ({resource['programRule']['id']}) from Program '{resource['programRule']['program']['name']}' ({resource['programRule']['program']['id']}). Response {validation_rule_action.json()}" )
      
    else:
        logger.info(f"Skip Program Rules Actions validation because the dhis2 version instance is lower than 2.37 ({dhis2_version})" )   


################################################################################
 
 
    # since 2.29
     
    RESOURCE_TYPE = "predictors"
    EXPRESSION_NAME = "expression" # from generator
  
    logger.info(f"Processing resource type: {RESOURCE_TYPE}")
    try:
        response = utils.get_resources_from_online(credentials=credentials, resource_type=RESOURCE_TYPE, fields='id,name,generator[expression],sampleSkipTest[expression]', param_filter=None)
    except Exception as e: 
        logger.error(f"Error while processing resource type: {RESOURCE_TYPE}")
        logger.error(e)
        response[RESOURCE_TYPE] = {}
           
    for resource in response[RESOURCE_TYPE]:
        logger.debug(f"Check PREDICTOR={resource['id']}")
        validation_expression_generator = utils.validate_expression(credentials, RESOURCE_TYPE, "expression", expression=resource["generator"][EXPRESSION_NAME])
        if validation_expression_generator:
            logger.error(f"Expression problem. Double check the generator {EXPRESSION_NAME} of the Predictor '{resource['name']}' ({resource['id']}). Response {validation_expression_generator.json()}" )
          
        if "sampleSkipTest" in resource:
            validation_expression_sampleSkipTest = utils.validate_expression(credentials, RESOURCE_TYPE, "expression", expression=resource["sampleSkipTest"][EXPRESSION_NAME])
            if validation_expression_sampleSkipTest:
                logger.error(f"Expression problem. Double check the sampleSkipTest {EXPRESSION_NAME} of the Predictor '{resource['name']}' ({resource['id']}). Response {validation_expression_sampleSkipTest.json()}" )
 
################################################################################
     
    # since 2.29
            
    RESOURCE_TYPE = "validationRules"
    
    logger.info(f"Processing resource type: {RESOURCE_TYPE}")
    try:
        response = utils.get_resources_from_online(credentials=credentials, resource_type=RESOURCE_TYPE, fields='id,name,leftSide[expression],rightSide[expression]', param_filter=None)
    except Exception as e: 
        logger.error(f"Error while processing resource type: {RESOURCE_TYPE}")
        logger.error(e)
        response[RESOURCE_TYPE] = {}


    for resource in response[RESOURCE_TYPE]:
        logger.debug(f"Check VR={resource['id']}")
        EXPRESSION_NAME = "leftSide"
        if EXPRESSION_NAME in resource: 
            validation_expression = utils.validate_expression(credentials, RESOURCE_TYPE, "expression", expression=resource[EXPRESSION_NAME]['expression'])
            if validation_expression:
                logger.error(f"Expression problem. Double check the leftSide expression of the VR '{resource['name']}' ({resource['id']}). Response {validation_expression.json()}" )
        else:
            logger.error(f"VR '{resource['name']}' ({resource['id']}) without leftSide expression" )
    
    
        EXPRESSION_NAME = "rightSide"
        if EXPRESSION_NAME in resource: 
            validation_filter = utils.validate_expression(credentials, RESOURCE_TYPE, "expression", expression=resource[EXPRESSION_NAME]['expression'])
            if validation_filter:
                logger.error(f"Expression problem. Double check the rightSide expression of the VR '{resource['name']}' ({resource['id']}). Response {validation_expression.json()}" )
        else:
            logger.error(f"VR '{resource['name']}' ({resource['id']}) without rightSide expression" )
