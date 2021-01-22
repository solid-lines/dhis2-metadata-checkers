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

# check-programIndicators-without-expression.py
This script checks if a program indicator has a expression.

# check-organisationUnitOpeningDateAndClosedDate.py
This script checks if an organization unit has coherent opening and closed dates (i.e. search for closedDate in the future or openingDate later than closedDate)

# check-programStageSections-without-programStage.py
This script checks if a programStageSection is NOT associated with a programStage (i.e. search for orphan programStageSections).

# check-optionSets-options-and-order.py
This script checks if each optionSet has at least 2 options associated AND checks if the sortOrder of the options is valid (i.e. starts at 1  and the latest sortOrder value is the size of the list of options)