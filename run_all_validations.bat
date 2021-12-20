@echo off 
set credentials=credentials_who_tracker_dev

python3 check_de_aggregate_without_dataset.py --credentials=%credentials%
python3 check_de_ps_pss.py --credentials=%credentials%
python3 check_error_500.py --credentials=%credentials%
python3 check_expressions.py --credentials=%credentials%
python3 check_link_programRuleAction_de.py --credentials=%credentials%
python3 check_link_programRuleAction_tea.py --credentials=%credentials%
python3 check_link_programRuleVariable_de.py --credentials=%credentials%
python3 check_link_programRuleVariable_tea.py --credentials=%credentials%
python3 check_naming_convention.py --credentials=%credentials%
python3 check_option_code.py --credentials=%credentials%
python3 check_options_in_filters.py --credentials=%credentials%
python3 check_options_without_optionSet.py --credentials=%credentials%
python3 check_optionSets_options_and_order.py --credentials=%credentials%
python3 check_organisationUnitOpeningDateAndClosedDate.py --credentials=%credentials%
python3 check_PR_PI_program_stage_name.py --credentials=%credentials%
python3 check_programIndicators_without_expression.py --credentials=%credentials%
python3 check_programRule_expression.py --credentials=%credentials%
python3 check_programRules_boolean.py --credentials=%credentials%
python3 check_programRules_evaluation_texts.py --credentials=%credentials%
python3 check_programRules_without_condition.py --credentials=%credentials%
python3 check_programRules_without_programRuleActions.py --credentials=%credentials%
python3 check_programRuleVariable_name.py --credentials=%credentials%
python3 check_programs_without_programStages.py --credentials=%credentials%
python3 check_programStages_without_program.py --credentials=%credentials%
python3 check_programStageSections_without_programStage.py --credentials=%credentials%
python3 check_programsWithoutRegistration_with_TE_type.py --credentials=%credentials%
python3 check_size_groups_and_sets.py --credentials=%credentials%
python3 check_uniqueness_de_in_deg.py --credentials=%credentials%
python3 check_uniqueness_name.py --credentials=%credentials%
python3 check_uniqueness_options_in_optionSet.py --credentials=%credentials%
python3 check_uniqueness_orgUnit_orgUnitGroupSet.py --credentials=%credentials%
python3 check_uniqueness_pig_program.py --credentials=%credentials%
