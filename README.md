# dhis2-metadata-checkers

## Requirements
1. Python 3 (maybe 3.6+)


## Steps for all scripts

1. RENAME credentials-template.ini to credentials.ini and FILL IN with your information
2. Watch out!!! the server url MUST follow the pattern "http://SERVER_DOMAIN/api/" (including the trailing slash)
3. In the python file, select the credentials that you want to use
4. Run the script
5. Check the log file


# check-options-without-optionSet.py
This script checks if an option is NOT associated with an optionSet (i.e. search for orphan options).

# check-programs-without-programStages.py
This script checks if a program (event/tracker) has at least one programStage (i.e. search for programs without programStages).