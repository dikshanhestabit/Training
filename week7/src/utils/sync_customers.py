import pandas as pd
import sqlite3
import os

# loading customer csv into sqlite
def load_customers_csv_to_sql(csv_path: str, db_path: str):
    if not os.path.exists(csv_path):
        print(f"Error: CSV file not found at {csv_path}")
        return

    # reading data using pandas
    df = pd.read_csv(csv_path)
    
    # cleaning column names by removing spaces and dots
    df.columns = [c.strip().replace(' ', '_').replace('.', '') for c in df.columns]

    # connecting to sqlite db
    conn = sqlite3.connect(db_path)
    
    # saving data to customers table
    df.to_sql('Customers', conn, if_exists='replace', index=False)
    
    conn.close()
    print(f"Successfully loaded {len(df)} records from {csv_path} to {db_path} in 'Customers' table.")

if __name__ == "__main__":
    csv_file = "src/data/raw/customers-100.csv"
    db_file = "src/data/customers.db"
    # running loader
    load_customers_csv_to_sql(csv_file, db_file)
