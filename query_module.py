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
        return sqrt(variance)  

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
    occupations = set()  # i use a set here to handle uniqueness

    for record in data.values():
        if record.get('income', '').strip() == '<=50K':
            occupation = record.get('occupation', 'Unknown').strip()
            occupations.add(occupation)

    return list(occupations)

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

def proportion_income_never_married(data):
    income_counts = {'>50K': 0, '<=50K': 0}
    total_never_married = 0

    for record in data.values():
        if record.get('marital-status', '').strip() == 'Never-married':
            income_category = record.get('income', '').strip()
            if income_category in income_counts:
                income_counts[income_category] += 1
            total_never_married += 1

    if total_never_married > 0:
        # Convert counts to percentages
        proportions = {category: (count / total_never_married) * 100 for category, count in income_counts.items()}
        return proportions
    else:
        return None

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

def basic_statistics_of_race(data):
    race_stats = {}
    for record in data.values():
        race = record.get('race', 'Unknown').strip()
        if race in race_stats:
            race_stats[race] += 1
        else:
            race_stats[race] = 1
    return race_stats

def persist_query_results_to_csv(data, query_name, file_path):
    try:
        # Open the file in append mode
        with open(file_path, mode='a', encoding='utf-8') as file:
            # Check if file is empty to decide on writing headers
            file.seek(0, 2)  # Move to the end of file
            if file.tell() == 0:  # File is empty
                file.write('Query Name,Data\n')
            
            # Handle different types of data
            if isinstance(data, (list, tuple)) and all(isinstance(item, dict) for item in data):
                for record in data:
                    formatted_record = ', '.join(f"{key}: {value}" for key, value in record.items())
                    file.write(f"{query_name},{formatted_record}\n")
            elif isinstance(data, dict):
                formatted_record = ', '.join(f"{key}: {value}" for key, value in data.items())
                file.write(f"{query_name},{formatted_record}\n")
            else:
                # Handle single data point (int, str, etc.)
                file.write(f"{query_name},{data}\n")
    except IOError as e:
        # Handle file I/O errors e.g., file not found, or disk full
        print(f"Error writing to file {file_path}: {e}")