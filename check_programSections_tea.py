#!/usr/bin/python
# -*- coding: UTF-8 -*-

import utils
import os


if __name__ == "__main__":

    credentials = utils.get_credentials()    
    check_name = os.path.basename(__file__).replace(".py", "")
    logger = utils.get_logger(credentials, check_name)
    
    server_url = credentials["server"]
    
    ############################################################################
    
    PARENT_RESOURCE = "programs"

    # Retrieve all metadata_resources
    metadata_resources = utils.get_resources_from_online(credentials=credentials, resource_type=PARENT_RESOURCE, fields="id,name,programSections[id,name,trackedEntityAttributes[id,name]],programTrackedEntityAttributes[trackedEntityAttribute]", param_filter="filter=programSections:ne:0")
       
    # Check condition (all TEAs in the program sections are part of the program)    
    for program in metadata_resources[PARENT_RESOURCE]:        
        program_teas = [t['trackedEntityAttribute']['id'] for t in program['programTrackedEntityAttributes']]
        for program_section in program["programSections"]:
            program_section_teas = {t['id']:t['name'] for t in program_section['trackedEntityAttributes']}
            
            # Get TEAs that are in the program Section but there are not part of program's TEAs
            offensive_teas = list(set(program_section_teas.keys())-set(program_teas))
            for t in offensive_teas:
                message = f"In program '{program['name']}' ({program['id']}), the program section '{program_section['name']}' ({program_section['id']}) includes an unexpected TEA '{program_section_teas[t]}' ({t})."
                logger.error(message)
