
# while loading the dataset i experienced some problems so upon research on how to identify where in the 
# dataset i have issues i went and implemented a log feature that allows us know what line in the 
#data has issues. and when a problem comes up it logs it into a text file
def load_data_from_csv(file_path):
    nested_dict = {}
    headers = [
        "age", "workclass", "fnlwgt", "education", "education-num",
        "marital-status", "occupation", "relationship", "race", "sex",
        "capital-gain", "capital-loss", "hours-per-week", "native-country", "income"
    ]
    malformed_lines = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            if not lines:
                print("Error: The file is empty.")
                return {}

            for index, line in enumerate(lines):
                if line.strip() == '':  # Skip blank lines
                    continue
                values = line.strip().split(',')
                if len(values) != len(headers):
                    malformed_lines.append((index + 1, line))  # Log malformed line
                    continue  # Skip this line
                nested_dict[index] = {headers[i]: values[i] for i in range(len(headers))}

    except FileNotFoundError:
        print("The file was not found. Please check the file path.")
        return {}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {}

    if malformed_lines:
        print(f"Warning: Some lines were malformed and skipped. Check 'malformed_lines.log'.")
        with open("malformed_lines.log", "w") as log_file:
            for line_info in malformed_lines:
                log_file.write(f"Line {line_info[0]}: {line_info[1]}")

    return nested_dict
