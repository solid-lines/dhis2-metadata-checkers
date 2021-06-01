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

# check-uniqueness-options-in-optionSet.py
This script checks that all names and codes of the options that belongs to an optionSet are unique.

# check-uniqueness-orgUnit-orgUnitGroupSet.py
This script checks that an organisation unit can be member of exactly one of the groups in a group set.

# check-programsWithoutRegistration-with-TE-type.py
This script checks if a program without registration (event program) is associated (unexpectedly) to a Tracked Entity Type.

# check-size-groups-and-sets.py
This script checks the number of elements that are part of a group or a set, raising an error if the number is unexpected (like groups conformed by one element).

Groups and Sets that they are expected to be conformed by more than one element:

* programIndicatorGroups: programIndicators
* dataElementGroups: dataElements
* programTrackedEntityAttributeGroups: programTrackedEntityAttributes
* indicatorGroups: indicators
* validationRuleGroups: validationRules
* predictorGroups: predictors
* categoryOptionGroups: categoryOptions
* organisationUnitGroups: organisationUnits
* userGroups: users
* optionGroups: options
* categories: categoryOptions
* indicatorGroupSets: indicatorGroups
* organisationUnitGroupSets: organisationUnitGroups
* optionSets: options
* legendSets: legends
* dataElementGroupSets: dataElementGroups
* categoryOptionGroupSets: categoryOptionGroups
* dataSets: dataSetElements
* colorSets: colors
* optionGroupSets: optionGroups


Resources that are expected to be linked with only one 'otherResource':

* dataElements: dataSetElements
