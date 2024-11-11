import great_expectations as gx
import great_expectations.expectations as gxe
import logging as log

# Get the context of Great Expectations
def get_gx_context():
    return gx.get_context()


# validation.py
def validate_data(df, data_name, expectations):
    context = get_gx_context()
    
    # Create or load the data source and the asset
    try:
        data_source = context.data_sources.get("pandas")
    except KeyError:
        data_source = context.data_sources.add_pandas("pandas")
    
    # Create or load the data asset
    try:
        data_asset = data_source.get_asset(name=data_name)
    except LookupError:
        data_asset = data_source.add_dataframe_asset(name=data_name)
    
    # Define the batch definition and retrieve the batch
    batch_definition = data_asset.add_batch_definition_whole_dataframe(f"batch_{data_name}")
    batch = batch_definition.get_batch(batch_parameters={"dataframe": df})
    
    # Create or load the Expectation Suite
    suite_name = f"{data_name}_expectations"
    try:
        expectation_suite = context.suites.get(suite_name)
    except gx.exceptions.DataContextError:
        expectation_suite = context.suites.add(gx.ExpectationSuite(name=suite_name))
    
    # Add expectations to the suite
    for expectation in expectations:
        expectation_suite.add_expectation(expectation)
    
    # Validate and capture the result
    validation_result = batch.validate(expectation_suite)
    if not validation_result["success"]:
        log.error(f"Validation failed for {data_name}")
        log.error("Detalles de la validación fallida:")
        for result in validation_result["results"]:
            log.error(result)
        raise Exception(f"GX validation failed for {data_name}")
    
    return validation_result




# Specify the expectations for each dataset
def validate_cardio_data(df):
    cardio_expectations = [
        gxe.ExpectTableColumnsToMatchOrderedList(
            column_list=[
                "id", "age", "gender", "height", "weight", "ap_hi", "ap_lo",
                "cholesterol", "gluc", "smoke", "alco", "active", "cardio"
            ]
        ),
        gxe.ExpectColumnValuesToBeBetween(column="age", min_value=10798, max_value=23713),
        gxe.ExpectColumnValuesToBeBetween(column="height", min_value=55, max_value=250),
        gxe.ExpectColumnValuesToBeBetween(column="weight", min_value=10, max_value=200),
        gxe.ExpectColumnValuesToBeOfType(column="id", type_="int"),
        gxe.ExpectColumnValuesToBeOfType(column="gender", type_="int"),
    ]
    return validate_data(df, "cardio_data", cardio_expectations)

def validate_deaths_data(df):
    deaths_expectations = [
        gxe.ExpectTableColumnsToMatchOrderedList(
            column_list=["id", "Country", "Code", "Year", "Cardiovascular", "TotalDeaths"]
        ),
        gxe.ExpectColumnValuesToBeBetween(column="Year", min_value=1990, max_value=2019),
        gxe.ExpectColumnValuesToBeBetween(column="Cardiovascular", min_value=4 * 0.95, max_value=4584273 * 1.05),
        gxe.ExpectColumnValuesToBeBetween(column="TotalDeaths", min_value=7 * 0.95, max_value=10442560 * 1.05),
    ]
    return validate_data(df, "deaths_data", deaths_expectations)

def validate_api_data(df):
    owid_expectations = [
        gxe.ExpectTableColumnsToMatchOrderedList(
            column_list=[
                "Country", "Code", "Year", "CardiovascularDeaths", 
                "nitrogen_oxide(NOx)", "sulphur_dioxide(SO2)", 
                "carbon_monoxide(CO)", "black_carbon(BC)", "ammonia(NH3)", 
                "non_methane_volatile_organic_compounds", "gdp_per_capita", 
                "obesity_prevalence_percentage", "diabetes_prevalence_percentage", 
                "population", "TotalDeaths"
            ]
        ),
        gxe.ExpectColumnValuesToBeBetween(column="Year", min_value=1990, max_value=2019),
        gxe.ExpectColumnValuesToBeBetween(column="CardiovascularDeaths", min_value=3.8, max_value=4813486.65),
        gxe.ExpectColumnValuesToBeBetween(column="gdp_per_capita", min_value=234.4, max_value=177660.3),
        gxe.ExpectColumnValuesToBeBetween(column="obesity_prevalence_percentage", min_value=0.3, max_value=64.05),
        gxe.ExpectColumnValuesToBeBetween(column="diabetes_prevalence_percentage", min_value=1.8, max_value=31.3),
    ]
    
    # Perform the validation
    validation_result = validate_data(df, "owid_data", owid_expectations)

    # Log the result instead of using XCom
    if not validation_result["success"]:
        log.error(f"Validation failed for owid_data")
        log.error("Detalles de la validación fallida:")
        for result in validation_result["results"]:
            log.error(result)
    else:
        log.info("Validation for owid_data passed successfully.")
        
    
    return validation_result["success"]

