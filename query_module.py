def find_missing_workclass(data):
# Retrieve records where the 'workclass' feature is missing (indicated by '?').
    missing_workclass_records = []
    for index, record in data.items():
        if record.get('workclass', '').strip() == '?': 
            missing_workclass_records.append(record)
    
    return missing_workclass_records

def compute_std_deviation(data):
    capital_gains = []
    capital_losses = []

    # Collecting all capital gains and losses
    for record in data.values():
        capital_gains.append(float(record.get('capital-gain', 0)))
        capital_losses.append(float(record.get('capital-loss', 0)))

    # function to calculate standard deviation
    def std_dev(values):
        if not values:
            return 0
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return sqrt(variance)  # Using custom sqrt function

    # square root function
    def sqrt(value):
        if value == 0:
            return 0
        x, y = value, None
        while y != x:
            y = x
            x = (x + value / x) / 2 
        return x

    # Calculating standard deviation for gains and losses
    std_dev_gains = std_dev(capital_gains)
    std_dev_losses = std_dev(capital_losses)

    return std_dev_gains, std_dev_losses

def get_native_country(data, index):
    try:
        # Retrieve the record for the given index
        record = data[index]
        # Return the 'native-country' attribute
        return record.get('native-country', 'No country data available')
    except KeyError:
        return "No individual found at the provided index."

def count_people_by_country(data, country_name):
    count = 0
    for record in data.values():
        if record.get('native-country', '').strip() == country_name:
            count += 1
    return count

def count_people_with_doctorate(data):
    count = 0
    for record in data.values():
        if record.get('education', '').strip() == 'Doctorate':
            count += 1
    return count

def get_occupation(data, index):
    try:
        # Retrieve the record for the given index
        record = data[index]
        # Return the 'occupation'
        return record.get('occupation', 'No occupation data available')
    except KeyError:
        return "No individual found at the provided index."

def marital_status_statistics(data):
    status_counts = {}
    for record in data.values():
        status = record.get('marital-status', 'Unknown').strip()
        if status in status_counts:
            status_counts[status] += 1
        else:
            status_counts[status] = 1

    return status_counts

def average_age_above_50k(data):
    total_age = 0
    count = 0

    for record in data.values():
        if record.get('income', '').strip() == '>50K':
            total_age += int(record.get('age', 0))
            count += 1

    if count == 0:
        return "No individuals with income above $50K found."
    else:
        return total_age / count

def occupations_below_50k(data):
    occupations = []
    for record in data.values():
        if record.get('income', '').strip() == '<=50K':
            occupation = record.get('occupation', 'Unknown').strip()
            occupations.append(occupation)

    return occupations

def income_percentage_by_gender(data):
    # as prep we initialize counters
    gender_income = {
        'Male': {'>50K': 0, '<=50K': 0, 'total': 0},
        'Female': {'>50K': 0, '<=50K': 0, 'total': 0}
    }

    # then we count occurrences
    for record in data.values():
        gender = record.get('sex', 'Unknown').strip()
        income = record.get('income', '').strip()
        if gender in ['Male', 'Female']:
            gender_income[gender]['total'] += 1
            if income == '>50K':
                gender_income[gender]['>50K'] += 1
            elif income == '<=50K':
                gender_income[gender]['<=50K'] += 1

    # Calculate percentages
    results = {}
    for gender, counts in gender_income.items():
        if counts['total'] > 0:
            results[gender] = {
                '>50K': (counts['>50K'] / counts['total']) * 100,
                '<=50K': (counts['<=50K'] / counts['total']) * 100
            }
        else:
            results[gender] = {'>50K': 0, '<=50K': 0}

    return results

def income_stats_by_marital_status(data):
    # first we collect income data per marital status using a dictionary
    marital_incomes = {}
    for record in data.values():
        status = record.get('marital-status', 'Unknown').strip()
        if record.get('income').isdigit():
            income = int(record.get('income'))
            if status in marital_incomes:
                marital_incomes[status].append(income)
            else:
                marital_incomes[status] = [income]

    # then we define some functions to calculate mode and median
    def calculate_mode(incomes):
        income_count = {}
        for income in incomes:
            if income in income_count:
                income_count[income] += 1
            else:
                income_count[income] = 1
        max_count = max(income_count.values())
        modes = [income for income, count in income_count.items() if count == max_count]
        return modes

    def calculate_median(incomes):
        n = len(incomes)
        sorted_incomes = sorted(incomes)
        mid = n // 2
        if n % 2 == 0:
            return (sorted_incomes[mid - 1] + sorted_incomes[mid]) / 2
        else:
            return sorted_incomes[mid]

    # then we calculate statistics for each marital status
    stats = {}
    for status, incomes in marital_incomes.items():
        if incomes:
            mean_income = sum(incomes) / len(incomes)
            mode_income = calculate_mode(incomes)
            median_income = calculate_median(incomes)
            stats[status] = {'mean': mean_income, 'mode': mode_income, 'median': median_income}
        else:
            stats[status] = {'mean': 0, 'mode': [], 'median': None}

    return stats

def attributes_of_high_earners(data):
    high_earners = []
    for record in data.values():
        if record.get('income', '').strip() == '>50K':
            # now we Collect the required attributes
            attributes = {
                'age': record.get('age'),
                'race': record.get('race'),
                'gender': record.get('sex')
            }
            high_earners.append(attributes)

    return high_earners

def attributes_of_lower_earners(data):
    lower_earners = []
    for record in data.values():
        if record.get('income', '').strip() == '<=50K':
            # Collect the required attributes
            attributes = {
                'age': record.get('age'),
                'race': record.get('race'),
                'gender': record.get('sex')
            }
            lower_earners.append(attributes)

    return lower_earners

def attributes_of_doctorates(data):
    doctorates = []
    for record in data.values():
        if record.get('education', '').strip() == 'Doctorate':
            # Collecting the required attributes
            attributes = {
                'income': record.get('income'),
                'gender': record.get('sex'),
                'race': record.get('race')
            }
            doctorates.append(attributes)

    return doctorates

def persist_query_results_to_csv(data, query_name, file_path):

    # we normalize data to a list of dictionaries if it's a single dictionary
    if isinstance(data, dict):
        data = [data]

    print(f"Data to write: {data}")  # Debugging output

    # Open the file in append mode
    with open(file_path, mode='a', encoding='utf-8') as file:
        if data:
            # Check if file is empty to decide on writing headers
            file.seek(0, 2)  # Move to the end of file
            if file.tell() == 0:  # File is empty
                file.write('Query Name,Data\n')
            # Write data
            for record in data:
                formatted_record = str(record).replace(',', ';')  # Handle commas in data
                file.write(f"{query_name},{formatted_record}\n")
        else:
            print("No data received to write.")  # Debugging output


