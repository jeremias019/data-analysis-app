# Main module

from data_loader import DataLoader
from query_module import QueryModule

def main():
    try:
        # Load data
        loader = DataLoader()
        data = loader.load_data('people.data')

        # Initialize QueryModule
        query_module = QueryModule(data)

        # Example usage of query functions
        # Add code here to interact with the user interface or execute queries programmatically
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
