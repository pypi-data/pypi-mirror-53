# -*- coding: utf-8 -*-

PROJECT_HELP_COMMENT = """
# Welcome to great expectations. 
# This project configuration file allows you to define datasources, 
# generators, integrations, and other configuration artifacts that
# make it easier to use Great Expectations.

# For more help configuring great expectations, 
# see the documentation at: https://docs.greatexpectations.io/en/latest/core_concepts/data_context.html#configuration

# NOTE: GE uses the names of configured datasources and generators to manage
# how expectations and other configuration artifacts are stored in the 
# expectations/ and datasources/ folders. If you need to rename an existing
# datasource or generator, be sure to also update the paths for related artifacts.

ge_config_version: 1

"""

CONFIG_VARIABLES_INTRO = """
# Great Expectations config file supports variable substitution.

# Variable substitution enables these two use cases:
# 1. do not store sensitive credentials in a committed file (since the credentials file should be in 
#    the uncommitted directory  
# 2. allow a config parameter to take different values, depending on the environment (e.g., dev/staging/prod)
#
# When GE encounters the following syntax in the config file:
#
# my_key: ${my_value} (or $my_value)
#
# GE will attempt to replace the value of “my_key” with the value of env variable “my_value” or with the value of the key “my_value” read from credentials file (env variable takes precedence).
#
# If the replacing value comes from the config variables file, it can be a simple value or a dictionary. If it comes from an environment variable, it must be a simple value.
"""

PROJECT_OPTIONAL_CONFIG_COMMENT = CONFIG_VARIABLES_INTRO + """
config_variables_file_path: uncommitted/config_variables.yml

# The plugins_directory is where the data_context will look for custom_data_assets.py
# and any configured evaluation parameter store

plugins_directory: plugins/

expectations_store:
  class_name: ExpectationStore
  store_backend:
    class_name: FixedLengthTupleFilesystemStoreBackend
    base_directory: expectations/

profiling_store_name: local_validation_result_store

evaluation_parameter_store_name: evaluation_parameter_store

# Configure additional data context options here.

# Uncomment the lines below to enable s3 as a result store. If a result store is enabled,
# validation results will be saved in the store according to run id.

# For S3, ensure that appropriate credentials or assume_role permissions are set where
# validation happens.

stores:

  local_validation_result_store:
    class_name: ValidationResultStore
    store_backend:
      class_name: FixedLengthTupleFilesystemStoreBackend
      base_directory: uncommitted/validations/
      filepath_template: '{4}/{0}/{1}/{2}/{3}.json'

  # s3_validation_result_store:
  #   class_name: ValidationStore
  #   store_backend:
  #     class_name: FixedLengthTupleS3StoreBackend
  #     bucket: ???
  #     prefix: ???
  #     file_extension: json
  #     filepath_template: '{4}/{0}/{1}/{2}/{3}.{file_extension}'

  # FIXME: These configs are temporarily commented out to facititate refactoring Stores.

  # local_profiling_store:
  #   module_name: great_expectations.data_context.store
  #   class_name: FilesystemStore
  #   store_config:
  #     base_directory: uncommitted/profiling/
  #     serialization_type: json
  #     file_extension: .json

  # local_workbench_site_store:
  #   module_name: great_expectations.data_context.store
  #   class_name: FilesystemStore
  #   store_config:
  #     base_directory: uncommitted/documentation/local_site
  #     file_extension: .html

  # shared_team_site_store:
  #   module_name: great_expectations.data_context.store
  #   class_name: FilesystemStore
  #   store_config:
  #     base_directory: uncommitted/documentation/team_site
  #     file_extension: .html

  # fixture_validation_results_store:
  #   module_name: great_expectations.data_context.store
  #   class_name: FilesystemStore
  #   store_config:
  #     base_directory: fixtures/validations
  #     file_extension: .zzz

  fixture_validation_results_store:
    class_name: ValidationResultStore
    store_backend:
      class_name: FixedLengthTupleFilesystemStoreBackend
      base_directory: fixtures/validations
      filepath_template: '{4}/{0}/{1}/{2}/{3}.json'

#  data_asset_snapshot_store:
#    module_name: great_expectations.data_context.store
#    class_name: S3Store
#    store_config:
#      bucket:
#      key_prefix:

  evaluation_parameter_store:
    module_name: great_expectations.data_context.store
    class_name: EvaluationParameterStore

  local_site_html_store:
    module_name: great_expectations.data_context.store
    class_name: HtmlSiteStore
    base_directory: uncommitted/documentation/local_site/

  team_site_html_store:
    module_name: great_expectations.data_context.store
    class_name: HtmlSiteStore
    base_directory: uncommitted/documentation/team_site/


validation_operators:
  # Read about validation operators at: https://docs.greatexpectations.io/en/latest/guides/validation_operators.html
  perform_action_list_operator:
    class_name: PerformActionListValidationOperator
    action_list:
      - name: store_validation_result
        action:
          class_name: StoreAction
          target_store_name: local_validation_result_store
      - name: store_evaluation_params
        action:
          class_name: ExtractAndStoreEvaluationParamsAction
          target_store_name: evaluation_parameter_store
      - name: store_evaluation_params
        action:
          class_name: SlackNotificationAction
          slack_webhook: ${validation_notification_slack_webhook}
#          notify_on: all
          renderer:
            module_name: great_expectations.render.renderer.slack_renderer
            class_name: SlackRenderer
    
# Uncomment the lines below to enable a result callback.

# result_callback:
#   slack: ${slack_callback_url}

# TODO : Remove the extra layer of yml nesting in v0.8:
data_docs:
  sites:
    local_site: # site name
    # “local_site” renders documentation for all the datasources in the project from GE artifacts in the local repo. 
    # The site includes expectation suites and profiling and validation results from uncommitted directory. 
    # Local site provides the convenience of visualizing all the entities stored in JSON files as HTML.

      # specify a whitelist here if you would like to restrict the datasources to document
      datasource_whitelist: '*'

      module_name: great_expectations.render.renderer.site_builder
      class_name: SiteBuilder
      target_store_name: local_site_html_store
      
      site_index_builder:
        class_name: DefaultSiteIndexBuilder
      
      site_section_builders:
          
        expectations:
          class_name: DefaultSiteSectionBuilder
          source_store_name: expectations_store
          renderer:
            module_name: great_expectations.render.renderer
            class_name: ExpectationSuitePageRenderer

        validations:
          class_name: DefaultSiteSectionBuilder
          source_store_name: local_validation_result_store
          run_id_filter:
            ne: profiling
          renderer:
            module_name: great_expectations.render.renderer
            class_name: ValidationResultsPageRenderer

        profiling:
          class_name: DefaultSiteSectionBuilder
          source_store_name: local_validation_result_store
          run_id_filter:
            eq: profiling
          renderer:
            module_name: great_expectations.render.renderer
            class_name: ProfilingResultsPageRenderer

    team_site:
    # "team_site" is meant to support the "shared source of truth for a team" use case. 
    # By default only the expectations section is enabled.
    #  Users have to configure the profiling and the validations sections (and the corresponding validations_store and profiling_store attributes based on the team's decisions where these are stored (a local filesystem or S3). 
    # Reach out on Slack (https://greatexpectations.io/slack>) if you would like to discuss the best way to configure a team site.

      # specify a whitelist here if you would like to restrict the datasources to document
      datasource_whitelist: '*'
      
      module_name: great_expectations.render.renderer.site_builder
      class_name: SiteBuilder
      target_store_name: team_site_html_store
      
      site_index_builder:
        class_name: DefaultSiteIndexBuilder
      
      site_section_builders:
          
        expectations:
          class_name: DefaultSiteSectionBuilder
          source_store_name: expectations_store
          renderer:
            module_name: great_expectations.render.renderer
            class_name: ExpectationSuitePageRenderer

"""

PROJECT_TEMPLATE = PROJECT_HELP_COMMENT + "datasources: {}\n" + PROJECT_OPTIONAL_CONFIG_COMMENT

CONFIG_VARIABLES_COMMENT = CONFIG_VARIABLES_INTRO

CONFIG_VARIABLES_FILE_TEMPLATE = CONFIG_VARIABLES_INTRO