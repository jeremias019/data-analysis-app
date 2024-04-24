#this is a file used to test the functions in the query module file
#

from data_loader import load_data_from_csv
from query_module import (
    find_missing_workclass,
    compute_std_deviation,
    get_native_country,
    count_people_by_country,
    count_people_with_doctorate,
    get_occupation,
    marital_status_statistics,
    average_age_above_50k,
    occupations_below_50k,
    income_percentage_by_gender,
    proportion_income_never_married,
    attributes_of_high_earners,
    attributes_of_lower_earners,
    attributes_of_doctorates,
    persist_query_results_to_csv
)

# Load the sample dataset
data_path = 'people.data'  
data = load_data_from_csv(data_path)

missing_workclass = find_missing_workclass(data)
persist_query_results_to_csv(missing_workclass, 'Missing Workclass', 'query_results.csv')

std_dev_gains, std_dev_losses = compute_std_deviation(data)
persist_query_results_to_csv({'Gains': std_dev_gains, 'Losses': std_dev_losses}, 'Standard Deviation', 'query_results.csv')

# Test for Native Country and log the results
native_country = get_native_country(data, 0)  # Example index, adjust as necessary
persist_query_results_to_csv({'Native Country': native_country}, 'Native Country', 'query_results.csv')

# Test for Counting People by Country and log the results
count_usa = count_people_by_country(data, 'United-States')
persist_query_results_to_csv({'Count USA': count_usa}, 'Count People by Country', 'query_results.csv')

# Test for Counting People with Doctorate and log the results
count_doctorates = count_people_with_doctorate(data)
persist_query_results_to_csv({'Doctorates Count': count_doctorates}, 'Count People with Doctorate', 'query_results.csv')

# Test for Getting Occupation and log the results
occupation = get_occupation(data, 0)  # Example index, adjust as necessary
persist_query_results_to_csv({'Occupation': occupation}, 'Occupation', 'query_results.csv')

# Test for Marital Status Statistics and log the results
marital_stats = marital_status_statistics(data)
persist_query_results_to_csv(marital_stats, 'Marital Status Statistics', 'query_results.csv')

# Test for Average Age Above 50K and log the results
average_age = average_age_above_50k(data)
persist_query_results_to_csv({'Average Age >50K': average_age}, 'Average Age Above 50K', 'query_results.csv')

# Test for Occupations Below 50K and log the results
occupations = occupations_below_50k(data)
persist_query_results_to_csv(occupations, 'Occupations Below 50K', 'query_results.csv')

# Test for Income Percentage by Gender and log the results
gender_income_percentage = income_percentage_by_gender(data)
persist_query_results_to_csv(gender_income_percentage, 'Income Percentage by Gender', 'query_results.csv')

# Test for Income Statistics by Marital Status and log the results
income_stats_marital = proportion_income_never_married(data)
persist_query_results_to_csv(income_stats_marital, 'Income Stats for Never Married', 'query_results.csv')

# Test for Attributes of High Earners and log the results
high_earner_attributes = attributes_of_high_earners(data)
persist_query_results_to_csv(high_earner_attributes, 'Attributes of High Earners', 'query_results.csv')

# Test for Attributes of Lower Earners and log the results
lower_earner_attributes = attributes_of_lower_earners(data)
persist_query_results_to_csv(lower_earner_attributes, 'Attributes of Lower Earners', 'query_results.csv')

# Test for Attributes of Doctorates and log the results
doctorate_attributes = attributes_of_doctorates(data)
persist_query_results_to_csv(doctorate_attributes, 'Attributes of Doctorates', 'query_results.csv')

