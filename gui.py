import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog, Toplevel
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
    basic_statistics_of_race,
    persist_query_results_to_csv
)


class GUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Data Query System")

        # Initiate loading data at startup
        self.load_data()

        self.create_widgets()

    def load_data(self):
        filename = filedialog.askopenfilename(title="Open CSV File", filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")])
        if filename:
            try:
                self.data = load_data_from_csv(filename)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load data: {e}")
                self.master.destroy()  # Close the application if data fails to load
        else:
            self.master.destroy()  # Close the application if no file is selected

    def create_widgets(self):
        self.query_label = tk.Label(self.master, text="Select Query:")
        self.query_label.grid(row=0, column=0, padx=10, pady=10)

        self.query_options = tk.Listbox(self.master, height=15, width=55)
        self.query_options.grid(row=0, column=1, padx=10, pady=10, rowspan=2)

        queries = [
            "Find Records with Missing Work Class",
            "Compute Standard Deviation of Capital Gains and Losses",
            "Retrieve Native Country of an Individual",
            "Total People from a Given Native Country",
            "Total People with Doctorate Degrees",
            "Retrieve Occupation of an Individual",
            "Basic Statistics of Marital Status",
            "Average Age of People with Incomes Higher Than 50K",
            "Occupations of People with Incomes Less Than 50K",
            "Percentage of Income by Gender",
            "Proportion of Income of Never Married Individuals",
            "Basic Statistics of Race Feature",
            "Attributes of High Earners(>50k)",
            "Attributes of Lower Earners(<=50k)",
            "Attributes of People with Doctorates",
            "Exit"
        ]
        for query in queries:
            self.query_options.insert(tk.END, query)

        self.execute_button = tk.Button(self.master, text="Execute", command=self.execute_query)
        self.execute_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)


    def execute_query(self):
        selected_query = self.query_options.get(self.query_options.curselection())

        if not selected_query:
            messagebox.showwarning("Warning", "Please select a query before executing.")
            return

        try:
            if selected_query == "Find Records with Missing Work Class":
                result = find_missing_workclass(self.data)
                if result:
                    persist_query_results_to_csv(result, 'Missing Workclass', 'query_results.csv')
                else:
                    messagebox.showinfo("No Data", "No records found with missing work class.")

            elif selected_query == "Compute Standard Deviation of Capital Gains and Losses":
                std_dev_gains, std_dev_losses = compute_std_deviation(self.data)
                if std_dev_gains is not None and std_dev_losses is not None:
                    result = {'Gains': std_dev_gains, 'Losses': std_dev_losses}
                    persist_query_results_to_csv(result, 'Standard Deviation of Gains and Losses', 'query_results.csv')
                    messagebox.showinfo("Query Complete", "Check the CSV file for results.")
                else:
                    messagebox.showinfo("No Data", "Unable to compute standard deviations.")

            elif selected_query == "Retrieve Native Country of an Individual":
                index = self.prompt_for_index()
                if index is not None:
                    result = get_native_country(self.data, index)
                    if result:
                        persist_query_results_to_csv({'Native Country': result}, 'Native Country', 'query_results.csv')
                        messagebox.showinfo("Query Complete", "Check the CSV file for results.")
                    else:
                        messagebox.showinfo("No Data", "No data available for the specified index.")

            elif selected_query == "Total People from a Given Native Country":
                self.open_country_selection_window()
            
            elif selected_query == "Total People with Doctorate Degrees":
                result = count_people_with_doctorate(self.data)
                persist_query_results_to_csv({'Total Doctorates': result}, 'Total People with Doctorate Degrees', 'query_results.csv')
                messagebox.showinfo("Query Complete", "Check the CSV file for results.")

            elif selected_query =="Retrieve Occupation of an Individual":
                index = self.prompt_for_index()
                if index is not None:
                    result = get_occupation(self.data, index)
                    if result:
                        persist_query_results_to_csv({'Occupation': result}, 'Occupation of Individual', 'query_results.csv')
                        messagebox.showinfo("Query Complete", "Check the CSV file for results.")
                    else:
                        messagebox.showinfo("No Data", "No data available for the specified index.")
                else:
                    return  # User canceled or entered an invalid index
            
            elif selected_query == "Basic Statistics of Marital Status":
                result = marital_status_statistics(self.data)
                persist_query_results_to_csv(result, 'Marital Status Statistics', 'query_results.csv')
                messagebox.showinfo("Query Complete", "Check the CSV file for results.")

            elif selected_query == "Average Age of People with Incomes Higher Than 50K":
                result = average_age_above_50k(self.data)
                if result is not None:
                    persist_query_results_to_csv({'Average Age >50K': result}, 'Average Age Above 50K', 'query_results.csv')
                    messagebox.showinfo("Query Complete", "Check the CSV file for results.")
                else:
                    messagebox.showinfo("No Data", "No applicable data found.")

            elif selected_query == "Occupations of People with Incomes Less Than 50K":
                result = occupations_below_50k(self.data)
                persist_query_results_to_csv(result, 'Occupations Below 50K', 'query_results.csv')
                messagebox.showinfo("Query Complete", "Check the CSV file for results.")
            
            elif  selected_query == "Percentage of Income by Gender":
                result = income_percentage_by_gender(self.data)
                if result:
                    persist_query_results_to_csv(result, 'Income Percentage by Gender', 'query_results.csv')
                    messagebox.showinfo("Query Complete", "Check the CSV file for results.")
                else:
                    messagebox.showinfo("No Data", "No data available to calculate income percentage by gender.")

            elif selected_query == "Proportion of Income of Never Married Individuals":
                result = proportion_income_never_married(self.data)
                if result is not None:
                    persist_query_results_to_csv({'Proportion of Income of Never Married': result}, 'Proportion of Income of Never Married', 'query_results.csv')
                    messagebox.showinfo("Query Complete", "Check the CSV file for results.")
                else:
                    messagebox.showinfo("No Data", "No data available for never married individuals.")

            elif selected_query == "Attributes of High Earners(>50k)":
                result = attributes_of_high_earners(self.data)
                if result:
                    persist_query_results_to_csv(result, 'Attributes of High Earners', 'query_results.csv')
                    messagebox.showinfo("Query Complete", "Check the CSV file for results.")
                else:
                    messagebox.showinfo("No Data", "No data found for high earners.")

            elif selected_query == "Attributes of Lower Earners(<=50k)":
                result = attributes_of_lower_earners(self.data)
                if result:
                    persist_query_results_to_csv(result, 'Attributes of Lower Earners', 'query_results.csv')
                    messagebox.showinfo("Query Complete", "Check the CSV file for results.")
                else:
                    messagebox.showinfo("No Data", "No data found for lower earners.")

            elif selected_query == "Attributes of People with Doctorates":
                result = attributes_of_doctorates(self.data)
                if result:
                    persist_query_results_to_csv(result, 'Attributes of Doctorates', 'query_results.csv')
                    messagebox.showinfo("Query Complete", "Check the CSV file for results.")
                else:
                    messagebox.showinfo("No Data", "No data found for individuals with doctorates.")
                
            elif selected_query == "Basic Statistics of Race Feature":
                result = basic_statistics_of_race(self.data)
                persist_query_results_to_csv(result, 'Basic Statistics of Race', 'query_results.csv')
                messagebox.showinfo("Query Complete", "Check the CSV file for results.")

            elif selected_query == "Exit":
                self.master.destroy()
            
            messagebox.showinfo("Query Complete", "Check the CSV file for results.")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def prompt_for_index(self):
        index = simpledialog.askinteger("Enter Index", "Enter the index of the individual:")
        if index is None:  # User canceled input
            return None
        else:
            return index
        
    def open_country_selection_window(self):
        # Create a new Toplevel window
        self.new_window = Toplevel(self.master)
        self.new_window.title("Select Country")

        # Label
        tk.Label(self.new_window, text="Select a country:").pack(pady=10)

        # Country Dropdown
        self.country_var = tk.StringVar(self.new_window)
        countries = ["United-States", "Cambodia", "England", "Puerto-Rico", "Canada", "Germany", 
            "Outlying-US(Guam-USVI-etc)", "India", "Japan", "Greece", "South", "China", 
            "Cuba", "Iran", "Honduras", "Philippines", "Italy", "Poland", "Jamaica", "Vietnam",
            "Mexico", "Portugal", "Ireland", "France", "Dominican-Republic", "Laos", "Ecuador",
            "Taiwan", "Haiti", "Columbia", "Hungary", "Guatemala", "Nicaragua", "Scotland", 
            "Thailand", "Yugoslavia", "El-Salvador", "Trinadad&Tobago", "Peru", "Hong", 
            "Holand-Netherlands"]
        self.country_menu = tk.OptionMenu(self.new_window, self.country_var, *countries)
        self.country_menu.pack()

        # Submit Button
        tk.Button(self.new_window, text="Submit", command=self.submit_country).pack(pady=20)

    def submit_country(self):
        country = self.country_var.get()
        if country and country != 'Select a country':
            result = count_people_by_country(self.data, country)
            persist_query_results_to_csv(result, f'Total People from {country}', 'query_results.csv')
            messagebox.showinfo("Query Complete", "Check the CSV file for results.")
            self.new_window.destroy()
        else:
            messagebox.showwarning("Warning", "Please select a country.")

# To run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()
