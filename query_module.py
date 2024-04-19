# QueryModule

class QueryModule:
    def __init__(self, data):
        self.data = data

    def compute_std_capital_gains_losses(self):
        capital_gains = [record['capital_gain'] for record in self.data.values()]
        capital_losses = [record['capital_loss'] for record in self.data.values()]
        return {'capital_gains_std': self.calculate_std(capital_gains), 'capital_losses_std': self.calculate_std(capital_losses)}

    def calculate_std(self, values):
        if len(values) <= 1:
            return 0
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return variance ** 0.5

    def retrieve_native_country(self, age):
        return self.data[age]['native_country']

    def total_people_from_native_country(self, country):
        return sum(1 for record in self.data.values() if record['native_country'] == country)

    def total_people_with_doctorate(self):
        return sum(1 for record in self.data.values() if record['education'] == 'Doctorate')

    def retrieve_occupation(self, age):
        return self.data[age]['occupation']

    def basic_statistics_marital_status(self):
        marital_status_counts = {}
        for record in self.data.values():
            marital_status = record['marital_status']
            if marital_status in marital_status_counts:
                marital_status_counts[marital_status] += 1
            else:
                marital_status_counts[marital_status] = 1
        
        return marital_status_counts

    def average_age_higher_than_50k(self):
        total_age = 0
        count = 0
        for record in self.data.values():
            if record['income'] == '>50k':
                total_age += record['age']
                count += 1
        if count == 0:
            return 0
        return total_age / count

    def occupations_income_less_than_50k(self):
        occupations = set()
        for record in self.data.values():
            if record['income'] == '<=50k':
                occupations.add(record['occupation'])
        return list(occupations)

    def percentage_income_by_gender(self):
        total_count = len(self.data)
        income_by_gender = {'>50k': {}, '<=50k': {}}
        for record in self.data.values():
            income_category = record['income']
            gender = record['gender']
            if gender not in income_by_gender[income_category]:
                income_by_gender[income_category][gender] = 0
            income_by_gender[income_category][gender] += 1

        for income_category in income_by_gender:
            for gender in income_by_gender[income_category]:
                income_by_gender[income_category][gender] /= total_count
                income_by_gender[income_category][gender] *= 100

        return income_by_gender
    
    def get_records_with_missing_work_class(self):
        records_with_missing_work_class = []
        for age, record in self.data.items():
            if 'workclass' not in record or not record['workclass']:
                records_with_missing_work_class.append(record)
        return records_with_missing_work_class
    
    # Write the data to a CSV file
    def write_to_csv(self, file_path):
        try:
            with open(file_path, 'w') as csvfile:
                for record in self.data.values():
                    row_str = ','.join(map(str, record.values())) + '\n'
                    csvfile.write(row_str)
            print(f"Data written to {file_path} successfully.")
        except Exception as e:
            print(f"An error occurred while writing to CSV: {e}")

