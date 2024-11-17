import json
import pandas as pd
import great_expectations as gx
from dotenv import load_dotenv
from sqlalchemy import create_engine
from great_expectations.exceptions import DatasourceError, ExpectationSuiteNotFoundError

# Load environment variables from .env file
load_dotenv()

def load_config(config_file="config.json"):
  """Load configuration from a JSON file."""
  try:
    with open(config_file, "r") as file:
      return json.load(file)
  except (FileNotFoundError, json.JSONDecodeError) as e:
    raise RuntimeError(f"Failed to load configuration: {e}")


def initialize_context(mode="cloud"):
  """Initialize and return the GE DataContext."""
  return gx.get_context(mode=mode)

def get_column_mapping():
  """
  Define the mapping of CSV columns to database table columns

  Returns:
    dict: A dictionary mapping CSV columns to database table columns.
  """
  return {
    "CustomerID_CSV": "CustomerID"
  }

def load_data_from_db(conn_str, query):
  """
  Connect to an MSSQL database and load data into a DataFrame

  Args:
    conn_str (str): The connection string to MSSQL database
    query (str): The SQL query to execute

  Returns:
    pd.DataFrame: The data loaded into a Pandas DataFrame
  """
  try:
    engine = create_engine(conn_str)
    df = pd.read_sql_query(query, engine)
    return df
  except Exception as e:
    raise RuntimeError(f"Failed to connect to MSSQL database or execute query: {e}")

def add_data_source(context, data_source_name):
  """
  Check if a data source with the specified name exists.
  Adds the data source if it is not already present.
  """
  try:
    if not any(ds["name"] == data_source_name for ds in context.list_datasources()):
      context.add_datasource(
        name=data_source_name,
        class_name="PandasDatasource"
      )
      print(f"Data source '{data_source_name}' added successfully")
    else:
      print(f"Data source '{data_source_name}' already exists.")
  except DatasourceError as e:
    raise RuntimeError(f"Error adding data source '{data_source_name}': {e}")

def add_data_asset(context, data_source_name, data_asset_name):
  """
  Add a data asset to the specified data source in the GE Context
  """
  try:
    # Retrieve the data source
    data_source = context.data_sources.get(data_source_name)

    if data_source.get_asset(data_asset_name):
      print(f"Data asset '{data_asset_name}' already exists in data source '{data_source_name}'.")
      return
    # Add the data asset to the data source
    data_source.add_dataframe_asset(data_asset_name)
    print(f"Data asset '{data_asset_name}' successfully added to data source '{data_source_name}'.")
  except KeyError:
    raise RuntimeError(f"Data source '{data_source_name}' not found in the context.")
  except Exception as e:
    raise RuntimeError(f"Unexpected error while adding data asset '{data_asset_name}': {e}")

def add_batch_definition(context, data_source_name, data_asset_name, batch_name):
  """
  Add a batch definition to GE context

  Args:
    context: GE context
    data_source_name: Name of the data source
    data_asset_name: Name of the data asset
    batch_name: 
  """

def load_data(file_path="customers.csv"):
  """Load data into a DataFrame from a CSV file."""
  try:
    return pd.read_csv(file_path)
  except FileNotFoundError as e:
    raise RuntimeError(f"Data file not found: {e}")
  
def validate_config(config, required_keys):
  """
  Validate the configuration to ensure all required keys are present.

  Args:
    config (dict): The configuration dictionary
    required_keys (list): List of keys that must be present in the config.

  Raises:
    ValueError: If any required key is missing from the configuration.
  """
  missing_keys = [key for key in required_keys if key not in config or not config[key]]
  if missing_keys:
    raise ValueError(f"Missing required configuration keys: {', '.join(missing_keys)}")

def update_expectation_suite(context, csv_data, db_data, mapping, expectation_suite_name):
  """
  Update or create an expectation suite for validating data.

  Args:
    context: GE DataContext object.
    csv_data: DataFrame loaded from the CSV.
    db_data: DataFrame loaded from the database.
    mapping: Dictionary mapping CSV columns to database table columns.
    expectation_suite_name: Name of the expectation suite name.
  """
  try:
    # Load the existing expectation suite if it exists
    suite = context.suites.get(name=expectation_suite_name)
    #get_expectation_suite(expectation_suite_name)
  except ExpectationSuiteNotFoundError:
    # Create a new expectation suite if does not exist
    suite = context.create_expectation_suite(expectation_suite_name)

  # Iterate through column mappings and add/update expectations
  for csv_col, db_col in mapping.items():
    if csv_col in csv_data.columns and db_col in db_data.columns:
      # Check if the expectation already exist
      expectation_exists = any(
        exp.expectation_type == "expect_column_pair_values_to_be_equal"
        for exp in suite.expectations
      )

      if not expectation_exists:
        # Add the new column pair expectation if it does not exist
        pair_expectation = gx.expectations.ExpectColumnPairValuesToBeEqual(
          column_A=csv_col,
          column_B=db_col
        )
        suite.add_expectation(
          pair_expectation
        )

  # Save the updated or new expectation suite
  suite.save()
  print(f"Expectation suite '{expectation_suite_name}' updated successfully.")

# def run_validation(context, df, suite_name):


def main():
  # Load configuration
  config = load_config()

  # Validate configuration
  validate_config(config, required_keys=["data_source_name", "data_asset_name"])

  # Extract configuration values
  data_source_name = config.get("data_source_name")
  data_asset_name = config.get("data_asset_name")
  connection_string = config.get("connection_string")
  db_query = config.get("db_query")
  suite_name = config.get("suite_name")

  # Columns mapping
  columns_mapping = get_column_mapping()

  # Initialize GE context
  context = initialize_context()

  # Add and validate data source
  add_data_source(context, data_source_name)

  # Add data asset to the data source
  add_data_asset(context, data_source_name, data_asset_name)

  # Load data for further validation
  df = load_data()

  # Load data from the local MSSQL database
  df_mssql = load_data_from_db(conn_str=connection_string, query=db_query)

  # print("Data preview:\n", df.head())

  # print("MSSQL Data preview:\n", df_mssql.head())

  print("Available data source:", context.list_datasources())

  update_expectation_suite(
    context=context,
    csv_data=df,
    db_data=df_mssql,
    mapping=columns_mapping,
    expectation_suite_name=suite_name
  )

if __name__ == "__main__":
  main()