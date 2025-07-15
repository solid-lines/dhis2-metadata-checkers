# dhis2-metadata-checkers

## Requirements
1. Python 3 (maybe 3.6+)


## Steps for all scripts

1. RENAME credentials-template.ini to credentials.ini and FILL IN with your information
2. Watch out!!! the server url MUST follow the pattern "http://SERVER_DOMAIN/api/" (including the trailing slash)
3. Select the credentials that you want to use. There are 2 options:
    1. Use the command line argument `-c` OR `--credentials` to be able to pass the credentials you want to use.
    2. Edit `utils.py` and change the fixed value of `args.credentials_name` from `"credentials_myserver"` to the desired one.
4. Run the script
5. Check the log file


# check_authorities_and_userRoles.py
(2.37 or above) This script checks the userRoles without any authority associated, the authorities that are declared but there are not used by any userRole, and the authorities used by a userRole that are not declared.

# check_customForm_existence.py
This script checks if custom form is present in a program, a program stage or a dataset (there shouldn't be custom forms in packages and there must not be empty custom forms in packages)

# check_de_aggregate_without_dataset.py
This script checks if a data element is NOT associated with any dataSet (i.e. search for dataElements).

# check_de_domain_type.py
This script checks if there is a dataset that it is linked to a data element with domain type different than AGGREGATE.
Also, this script checks if there is a program (in fact, program stage) that it is linked to a data element with domain type different than TRACKER.

# check_de_ps_pss.py
This script checks if the data elements associated to a program stage are used in the program stage section AND if data elements that are NOT associated to the program stage are present in a program stage section.

# check_de_valuetype_aggregationtype.py
This script checks if the aggregation type of the data elements are inline with the expected values.

# check_error_500.py
This script checks if resource_types the resource "reportTables", "eventReports", "eventCharts", "dashboards", "maps" and "visualizations" (> 2.33) returns a HTTP code 500.

# check_existence_description.py
This script checks the existence of a description for a particular subset of resource types: programs, dataSets, dataElements, trackedEntityAttributes, trackedEntityTypes, indicators, programIndicators, validationRules, predictors, programRules, visualizations (event chart, event report, map, data visualizer), dashboards

# check_expressions.py
This scripts check if different expressions are well-formed. The expressions are: Indicator (numerator and denominator), Program Indicator (expression and filter), Program Rule (condition -since 2.35-), Program Rule Actions (data expression -since 2.37-) and Predictors (generator data and sampleSkipTest).

# check_link_programRuleAction_de.py
This script checks if the data element associated to a program rule action belongs to the program that the program rule is associated to.

# check_link_programRuleAction_hideoption.py
This script checks if the option to be hidden belongs to the optionSet of DE/TEA selected in the program rule. Also, it checks if an unexpected extra field "optionGroup" appears in the PRA.

# check_link_programRuleAction_hideoptiongroup.py
This script checks if the optionSet of the optiongroup to be hidden is the same than the optionSet of DE/TEA selected in the program rule. Also, it checks if an unexpected extra field "option" appears in the PRA.

# check_link_programRuleAction_tea.py
This script checks if the tracked entity attribute associated to a program rule action belongs to the program (or the tracked entity type) that the program rule is associated to.

# check_link_programRuleVariable_de.py
This script checks if the data element associated to a program rule variable exists and belongs to the program that the program rule is associated to.

# check_link_programRuleVariable_tea.py
This script checks if the tracked entity attribute associated to a program rule variable exists and belongs to the program (or the tracked entity type) that the program rule is associated to.

# check_naming_convention.py
This script checks if the resources follow the best practices of naming convention.

# check_option_code.py
This script checks if the option codes follows the best practice for codes (compoused by letters (upper/lower case), digits and special characters ('-', '_', '|' and '.').

# check_options_in_filters.py
This script checks if the options present in the filter of eventCharts and eventReports are valid (comparing them with the current options of the optionSets related to the dataelements referenced in the filter).

# check_options_without_optionSet.py
This script checks if an option is NOT associated with an optionSet (i.e. search for orphan options).

# check_optionSets_options_and_datatype.py
This script checks if the datatype of a DE associated to a optionSet is the same than the datatype of the optionSet. Also, it check that the codes of the options in the respective optionSet match the value type of the DE.

# check_optionSets_options_and_order.py
This script checks if each optionSet has at least 2 options associated AND checks if the sortOrder of the options is valid (i.e. starts at 0 or 1 (in a dhis2 instance, optionSets with different start sort order value can coexist), the latest sortOrder value is the size of the list of options)

# check_organisationUnitOpeningDateAndClosedDate.py
This script checks if an organization unit has coherent opening and closed dates (i.e. search for closedDate in the future or openingDate later than closedDate)

# check_orphan_optionSets.py
This script looks for optionSets that are not used in the system (neither in DE or TEA).

# check_PR_PI_program_stage_name.py
This script checks the use of "program_stage_name" (due to issues if the stage name is translated) in PR expression, PRA exression, PI expression, PI filter. 

# check_programIndicators_aggregateExchange.py
This script checks if a program indicator is correctly linked to the DE and COC used for the Tracker2Aggregate approach (See dhis2 documentation about "Integrating tracker and aggregate data").
This script is using the custom attribute `vudyDP7jUy5` for linking the PI and the DE.

# check_programIndicators_without_expression.py
This script checks if a program indicator has a expression.

# check_programRuleActions_duplicate.py
This script checks if in a program rule variable there are progrm rule actions duplicated.

# check_programRules_boolean.py
This script checks if the program rule variable that appears in '!#{prv}' has boolean/true_only type. 

# check_programRules_evaluation_texts.py
This script checks that in program rule actions (ASSIGN, DISPLAY TEXT, DISPLAY KEY/VALUE PAIR, SHOW WARNING, SHOW ERROR, WARNING ON COMPLETE, ERROR ON COMPLETE), if the expression to evaluate and assign/display is a text, it has to be in single quotes.

# check_programRules_without_condition.py
This script checks if a program rule has a condition.

# check_programRules_without_programRuleActions.py
This script checks if a program rule has at least one program rule action.

# check_programRuleVariable_name.py
This script checks if a program rule variable has not "and", "or" or "not" in its name. Also checks if the PRV name contains unexecpted characters. And also checks if there are PRV names duplicated for the same program

# check_programRuleVariable_unlink.py
This script checks if program rule variables (with source type DATAELEMENT_ or TEI_ATTRIBUTE) are linked to a DE or a TEA.

# check_programRuleVariable_unused.py
This script checks if program rule variables (PRVs) in a DHIS2 instance that are not being used by any program rule (condition) or program rule action.

# check_programs_without_programStages.py
This script checks if a program (event/tracker) has at least one programStage (i.e. search for programs without programStages).

# check_programSections_tea.py
This script checks if all TEAs that belongs to a programSection are linked to the program that the programSection belongs to.

# check_programStages_without_program.py
This script checks if a programStage is NOT associated with a program (i.e. search for orphan programStage).

# check_programStageSections_without_programStage.py
This script checks if a programStageSection is NOT associated with a programStage (i.e. search for orphan programStageSections).

# check_programsWithoutRegistration_with_TE_type.py
This script checks if a program without registration (event program) is associated (unexpectedly) to a Tracked Entity Type.

# check_sharesettings_no_public_no_usergroups.py
This script checks if a set of resources (DE, TEA, datasets and programs) is not public shared and it does not have any userGroup associated.

# check_size_groups_and_sets.py
This script checks the number of elements that are part of a group or a set, raising an error if the number is unexpected (like groups conformed by one element).

# check_translations.py
This script checks if translations are valid. For instance, it checks if there is one only translation per property and locale (e.g. a DE has only one translation for 'description' property in 'es' locale).

# check_uniqueness_name.py
This script checks if more than one resource of a particular type has the same name (configurable as name, shortname, formname) for the same locale.  

# check_uniqueness_options_in_optionSet.py
This script checks that all names and codes of the options that belongs to an optionSet are unique.

# check_uniqueness_orgUnit_orgUnitGroupSet.py
This script checks that an organisation unit can be member of exactly one of the groups in a group set.

# check_visualizations_with_empty_dataDimensionItems.py
This script checks if a visualization has empty data dimension items (that shouldn't be).


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
