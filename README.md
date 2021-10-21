# dhis2-metadata-checkers

## Requirements
1. Python 3 (maybe 3.6+)


## Steps for all scripts

1. RENAME credentials-template.ini to credentials.ini and FILL IN with your information
2. Watch out!!! the server url MUST follow the pattern "http://SERVER_DOMAIN/api/" (including the trailing slash)
3. In the python file, select the credentials that you want to use
4. Run the script
5. Check the log file

# check_de_aggregate_without_dataset.py
This script checks if a data element is NOT associated with any dataSet (i.e. search for dataElements).

# check_de_ps_pss.py
This script checks if the data elements associated to a program stage are used in the program stage instance.

# check_error_500.py
This script checks if resource_types the resource "reportTables", "eventReports", "eventCharts", "dashboards", "maps" and "visualizations" (> 2.33) returns a HTTP code 500.

# check_expressions.py
This scripts check if different expressions are well-formed. The expressions are: Indicator (numerator and denominator), Program Indicator (expression and filter), Program Rule (condition -since 2.35-), Program Rule Actions (data expression -since 2.37-) and Predictors (generator data and sampleSkipTest).

# check_link_programRuleAction_de.py
This script checks if the data element associated to a program rule action belongs to the program that the program rule is associated to.

# check_link_programRuleAction_tea.py
This script checks if the tracked entity attribute associated to a program rule action belongs to the program (or the tracked entity type) that the program rule is associated to.

# check_link_programRuleVariable_de.py
This script checks if the data element associated to a program rule variable exists and belongs to the program that the program rule is associated to.

# check_link_programRuleVariable_de.py
This script checks if the tracked entity attribute associated to a program rule variable exists and belongs to the program (or the tracked entity type) that the program rule is associated to.

# check_options_in_filters.py
This script checks if the options present in the filter of eventCharts and eventReports are valid (comparing them with the current options of the optionSets related to the dataelements referenced in the filter).

# check_options_without_optionSet.py
This script checks if an option is NOT associated with an optionSet (i.e. search for orphan options).

# check_optionSets_options_and_order.py
This script checks if each optionSet has at least 2 options associated AND checks if the sortOrder of the options is valid (i.e. starts at 1  and the latest sortOrder value is the size of the list of options)

# check_organisationUnitOpeningDateAndClosedDate.py
This script checks if an organization unit has coherent opening and closed dates (i.e. search for closedDate in the future or openingDate later than closedDate)

# check_programIndicators_without_expression.py
This script checks if a program indicator has a expression.

# check_programRules_boolean.py
This script checks if the program rule variable that appears in '!#{prv}' has boolean/true_only type. 

# check_programRules_evaluation_texts.py
This script checks that in program rule actions (ASSIGN, DISPLAY TEXT, DISPLAY KEY/VALUE PAIR, SHOW WARNING, SHOW ERROR, WARNING ON COMPLETE, ERROR ON COMPLETE), if the expression to evaluate and assign/display is a text, it has to be in single quotes.

# check_programRules_without_condition.py
This script checks if a program rule has a condition.

# check_programRules_without_programRuleActions.py
This script checks if a program rule has at least one program rule action.

# check_programRuleVariable_name.py
This script checks if a program rule variable has not "and", "or" or "not" in its name 

# check_programs_without_programStages.py
This script checks if a program (event/tracker) has at least one programStage (i.e. search for programs without programStages).

# check_programStages_without_program.py
This script checks if a programStage is NOT associated with a program (i.e. search for orphan programStage).

# check_programStageSections_without_programStage.py
This script checks if a programStageSection is NOT associated with a programStage (i.e. search for orphan programStageSections).

# check_programsWithoutRegistration_with_TE_type.py
This script checks if a program without registration (event program) is associated (unexpectedly) to a Tracked Entity Type.

# check_size_groups_and_sets.py
This script checks the number of elements that are part of a group or a set, raising an error if the number is unexpected (like groups conformed by one element).

# check_uniqueness_name.py
This script checks if more than one resource of a particular type has the same name (configurable as name, shortname, formname) for the same locale.  

# check_uniqueness_options_in_optionSet.py
This script checks that all names and codes of the options that belongs to an optionSet are unique.

# check_uniqueness_orgUnit_orgUnitGroupSet.py
This script checks that an organisation unit can be member of exactly one of the groups in a group set.


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
