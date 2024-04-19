import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from query_module import QueryModule
from data_loader import DataLoader

class GUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Data Query System")
        
        self.loader = DataLoader()
        try:
            self.data = self.loader.load_data('people.data')
            self.clean_data()
        except FileNotFoundError:
            messagebox.showerror("Error", "Data file 'people.data' not found.")
            self.master.destroy()
            return
        self.query_module = QueryModule(self.data)
        
        self.create_widgets()

    def create_widgets(self):
        self.query_label = tk.Label(self.master, text="Select Query:")
        self.query_label.grid(row=0, column=0, padx=10, pady=10)

        self.query_options = tk.Listbox(self.master, height=13, width=55)
        self.query_options.grid(row=0, column=1, padx=10, pady=10)

        queries = [
            "Find records with missing work class",
            "Compute standard deviation of capital gains and losses",
            "Retrieve native country of an individual",
            "Total people from given native country",
            "Total people with doctorate degrees",
            "Retrieve occupation of an individual",
            "Basic statistics of marital status",
            "Average age of people with incomes higher than 50k",
            "Occupations of people with incomes less than 50k",
            "Percentage of income by gender",
            "Exit"
        ]
        for query in queries:
            self.query_options.insert(tk.END, query)
        
        #execute button
        self.execute_button = tk.Button(self.master, text="Execute", command=self.execute_query)
        self.execute_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
        
    def clean_data(self):
        for record in self.data.values():
            record['native_country'] = record['native_country'].strip().title()

    def execute_query(self):
        selected_index = self.query_options.curselection()
        if not selected_index:
            messagebox.showwarning("Warning", "Please select a query.")
            return
        
        selected_query = self.query_options.get(selected_index[0])

        try:
            if selected_query == "Find records with missing work class":
                result = self.query_module.get_records_with_missing_work_class()
            elif selected_query == "Compute standard deviation of capital gains and losses":
                result = self.query_module.compute_std_capital_gains_losses()
            elif selected_query == "Retrieve native country of an individual":
                age = self.prompt_for_age()
                if age is not None:
                    result = self.query_module.retrieve_native_country(int(age))
                else:
                    return  # canceled input
            elif selected_query == "Total people from given native country":
                self.show_country_selection_dialog()
                return
            elif selected_query == "Total people with doctorate degrees":
                result = self.query_module.total_people_with_doctorate()
            elif selected_query == "Retrieve occupation of an individual":
                age = self.prompt_for_age()
                if age is not None:
                    result = self.query_module.retrieve_occupation(int(age))
                else:
                    return  # if user canceled input
            elif selected_query == "Basic statistics of marital status":
                result = self.query_module.basic_statistics_marital_status()
            elif selected_query == "Average age of people with incomes higher than 50k":
                result = self.query_module.average_age_higher_than_50k()
            elif selected_query == "Occupations of people with incomes less than 50k":
                result = self.query_module.occupations_income_less_than_50k()
            elif selected_query == "Percentage of income by gender":
                result = self.query_module.percentage_income_by_gender()
            elif selected_query == "Exit":
                self.master.destroy()
                return
            else:
                messagebox.showerror("Error", "Invalid query.")
                return

            messagebox.showinfo("Query Result", str(result))

            self.query_module.write_to_csv('results.csv')
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def prompt_for_age(self):
        age_input = simpledialog.askinteger("Enter Age", "Enter the age of the individual:")
        if age_input is None:  # User canceled input
            return None
        else:
            return age_input
    
    def show_country_selection_dialog(self):
        country_dialog = tk.Toplevel(self.master)
        country_dialog.title("Select Country")

        country_label = tk.Label(country_dialog, text="Select Country:")
        country_label.pack()

        unique_countries = sorted(set(record['native_country'] for record in self.data.values()))
        selected_country = tk.StringVar()
        country_combobox = ttk.Combobox(country_dialog, textvariable=selected_country, values=unique_countries)
        country_combobox.pack()

        select_button = tk.Button(country_dialog, text="Select", command=lambda: self.handle_country_selection(selected_country.get(), country_dialog))
        select_button.pack()

    def handle_country_selection(self, country, dialog):
        dialog.destroy()
        if country:
            result = self.query_module.total_people_from_native_country(country)
            messagebox.showinfo("Query Result", f"Total people from {country}: {result}")
        else:
            messagebox.showwarning("Warning", "Please select a country.")


def main():
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
