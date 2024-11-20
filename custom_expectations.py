def validate_status_purchase_amount(gx, suite):
  """
  Checks if the status is either ["Active", "Pending"] if purchase amount > 0

  Args:
    gx: Great Expectations instance
    suite: Expectations suite file
  """
  expectation_exists = any(
    exp.expectation_type == "expect_column_values_to_be_in_set"
    for exp in suite.expectations
  )

  if not expectation_exists:
    expectation = gx.expectations.ExpectColumnValuesToBeInSet(
      column="Status",
      value_set=["Active", "Pending"],
      condition_parser="pandas",
      row_condition='PurchaseAmount>0'
    )
    suite.add_expectation(expectation)