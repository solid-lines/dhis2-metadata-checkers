import utils
import os

if __name__ == "__main__":
    credentials = utils.get_credentials()
    check_name = os.path.basename(__file__).replace(".py", "")
    logger = utils.get_logger(credentials, check_name)

    server_url = credentials["server"]

    ############################################################################

    de_types = "[DATAELEMENT_NEWEST_EVENT_PROGRAM_STAGE,DATAELEMENT_NEWEST_EVENT_PROGRAM,DATAELEMENT_CURRENT_EVENT,DATAELEMENT_PREVIOUS_EVENT]"

    # Retrieving programRuleVariables filtered by programRuleVariableSourceType DATALEMENT_ or TEI_ATTRIBUTE
    prv_de = utils.get_resources_from_online(credentials=credentials, resource_type="programRuleVariables",
                                             fields="id,name,program[id,name]programRuleVariableSourceType,dataElement",
                                             param_filter="filter=dataElement:null&filter=programRuleVariableSourceType:in:" + de_types)

    prv_tei = utils.get_resources_from_online(credentials=credentials, resource_type="programRuleVariables",
                                              fields="id,name,program[id,name]programRuleVariableSourceType,trackedEntityAttributes",
                                              param_filter="filter=trackedEntityAttribute:null&filter=programRuleVariableSourceType:eq:TEI_ATTRIBUTE")

    # printing the log with the results
    for variable in prv_de["programRuleVariables"]:
        message = f"The Program Rule Variable '{variable['name']}' ({variable['id']}), present in the program '{variable['program']['name']}' ({variable['program']['id']}) with program Rule variable Source Type '{variable['programRuleVariableSourceType']}' has no dataElement associated."
        logger.error(message)

    for variable in prv_tei["programRuleVariables"]:
        message = f"The Program Rule Variable '{variable['name']}' ({variable['id']}), present in the program '{variable['program']['name']}' ({variable['program']['id']}) with program Rule variable Source Type '{variable['programRuleVariableSourceType']}' has no trackedEntityAttribute associated."
        logger.error(message)
