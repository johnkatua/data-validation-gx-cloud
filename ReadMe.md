# Install SQL Alchemy
  -> SQL Alchemy = 2.0.20
  -> pandas=2.0.3
  -> pyodbc=4.0.39

# Docs
  - Setup a GX Environment
    - Install GX (Great expectations)
      - pip install great_expectations
    - Install any additional dependencies
      - pip install 'great_expectations[mssql]'
    - Create a Data Context
      - Defines the storage location for metadata, such as your conf for Data Sources, Expectation Suites, Checkpoints and Data Docs
      Types of Data Context:-
        1. File Data Context
        2. Ephemeral Data Context
        3. GX Cloud Data Context
        ```
          import great_expectations as gx

          context = gx.get_context()
        ```

  - Connect to Data
    => Connect to SQL Data
    => Connect to Filesystem data
    => Connect to data in Dataframes

    To connect to your SQL data, you first create a Data Source which tells GX where your database resides and how to connect to it.  You then configure Data Assets for your Data Source to tell GX which sets of records you want to be able to access from your Data Source. Finally, you will define Batch Definitions which allow you to request all the records retrieved from a Data Asset or further partition the returned records based on the contents of a date and time field

    - Create a Data Asset
      - Data assets are collections of records within a Data Source. With SQL Data sources, a data asset can consist of the records from a specific table or the records from a specified query.

      1. Table Data Asset
        - A table Data Asset consists of the records in a single table. It takes two required parameters.
          a. table_name: The name of the SQL table that the Table Data Asset will retrieve records from.
          b. name: The name used to reference the Table Data Asset with GX, You may assign this arbitrarily, but all Data Assets within the same Data Source must have unique names

      2. Query Data Asset
        - A Query Data Asset consists of the records returned by a SQL query. It takes 2 required parameters:
          a. query: The SQL query that the Data Asset will retrieve records from.
          b. name: The name used to reference the Query Data Asset within GX.

    - Create a Batch Definition
      - Request records from the Data Asset
      1. Full Table - Returns all of the records in your Data Asset as a single Batch. Therefore, to define a full table batch definition you only need to provide a name for the batch definition to be referenced by.
      2. Partition - A partitioned Batch Definition subdivides the records in a Data Asset based on the values in a specified field. GX Core currently supports partitioning Data Assets based on date fields. The records can be grouped by year, month or day.

  - Define Expectations
    An Expectation is a verifiable assertion about your data, and an Expectation Suite is a collection of Expectations that describe the ideal state of a set of data.
      1. Create an Expectation - An instance of an expectation
      2. Test an Expectation - Test an expectation against a batch of data.
      3. Organize Expectations into Expectation Suite - Modify the params for an existing expecation.

      a. Create an Expectation
        Expectations make implicit assumptions about your data explicit, and they provide a flexible, declarative language for describing expected behaviour. They can help you better understand your data and help you improve data quality.
      b. Test an Expectation
      c. Organize expectation into a suite
        An Expectation suite contains a grp of Expectations that describe the same data. This allows you to validate the given set of data as a grp rather than individually

  - Run Validations
    Associate a batch definition with an Expectation Suite, set a format for results, and run a Validation Definition using default parameters or runtime parameter
    a. Create a Validation Definition
      A validation definition is a fixed reference that links a Batch of data to an Expectation Suite. It can be used to validate the referenced data against the associated Expectations. You can also have a Checkpoint with multiple validation definitions and are used to validate results based of on the validation definition.
    b. Run a Validation Definition
      Run the definition using predefined defaults or parameters defined at runtime

    - Trigger actions
      Automations of responses to validation results such as sending alerts and updating Data Docs
      a. Create a Checkpoint that triggers actions based on Validation Results
        Creates a checkpoint that triggers actions based on the validation results
      b. Select the result format
        When you validate data with GX Core you can set the level of detail returned in your validation results by specifying a value for the optional result_format parameter. The level accepted include:
          1. BOOLEAN_ONLY
          2. BASIC
          3. SUMMARY
          4. COMPLETE
      c. Run a checkpoint
        Validate all of the validation definitions and execute the action list based on the results. Some of the actions list include:-
          1. Update the results document
          2. Send Slack Notifications
          3. Send Teams Notifications


Yesterday
  I went through user story CPAP11-630 which is dealing with the creation financial field accounts. I also had a sync with Kevin Otieno on navigating through the agent console and viewing the existing financial account fields.

  Questions:
  1. The ticket requires the confirmation that all the financial fields are added to Financial 360 Data Agent, Is Financial 360 Data Agent a tool that I should have access to and if yes how can I access it.
  2. Not in UAT, added in CPAP

CPAP
Salesforce -> Reference Docs -> Technical Mapping Specifications
Loan Manager
Shaw file Source Table

# GX Cloud
  A fully managed SaaS platform that simplifies data quality management and monitoring. It helps collaborations of individuals within an organization to define and maintain data.

## GX Cloud Concepts
  1. Data Source - GX rep of a database or data store
  2. Data Asset - A collection of records within a Data Source.
  3. Expectation - A declarative, verifiable assumption about your data. They serve as unit tests for your data.
  4. Validation - An action that runs selected expectations against a Data Asset to validate the data.
  5. Validation Result - An outcome of a validation and related metadata that describes passing and failing data.


## GX Cloud workflow
  1. Connect to your data.
  2. Create a Data Asset.
  3. Define Expectations.
  4. Validate your data.
  5. Review and share your validation results with your organization.

## Additional workflow features
  1. GX Cloud user management -> Users can be invited to the GX Cloud organization and assigned a role that governs their ability to view and edit components and workflows in GX Cloud.
  2. Data Asset profiling -> 