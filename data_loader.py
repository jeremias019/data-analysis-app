
class DataLoader:
    def load_data(self, file_path):
        data = {}
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue  # Skip empty lines
                    record = line.split(',')
                    if len(record) < 15:
                        print(f"Skipping record: {line}. Insufficient fields.")
                        continue

                    try:
                        age = int(record[0])
                        capital_gain = int(record[10])
                        capital_loss = int(record[11])
                    except ValueError:
                        print(f"Skipping record: {line}. Age, capital gain, or loss is not a valid integer.")
                        continue

                    nested_dict = {
                        'age': age,
                        'workclass': record[1].strip(),
                        'fnlwgt': record[2].strip(),
                        'education': record[3].strip(),
                        'education_num': record[4].strip(),
                        'marital_status': record[5].strip(),
                        'occupation': record[6].strip(),
                        'relationship': record[7].strip(),
                        'race': record[8].strip(),
                        'gender': record[9].strip(),
                        'capital_gain': capital_gain,
                        'capital_loss': capital_loss,
                        'hours-per-week': record[12].strip(),
                        'native_country': record[13].strip(),
                        'income': record[14].strip()
                    }
                    data[age] = nested_dict
        except FileNotFoundError:
            print("Error: File not found.")
            return {}
        except Exception as e:
            print(f"An error occurred while loading data: {e}")
            return {}
        return data
