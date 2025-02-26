import time
import zipfile
import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
PATH ="C:/Users/HP/Downloads/EXL_Capstone/chromedriver.exe"
search="allowed-amounts"


def download_zip(url):
    driver.get(url)
    time.sleep(20)
    
    email=driver.find_element(By.CLASS_NAME,"ant-input")
    email.send_keys(search)
    time.sleep(10)
    email.send_keys(Keys.RETURN)


    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    lists = soup.find_all('li', class_='ant-list-item')

    for lst in lists:
        link_element = lst.find('a')
        if link_element:
            link_url = link_element.get('href')
            print("Downloading:", link_url)
            response = requests.get(link_url)
            filename = link_url.split('/')[-1]
            full_path = os.path.join("C:/Users/HP/Downloads/EXL_Capstone/zips", filename)

            with open(full_path, 'wb') as file:
                file.write(response.content)

            with zipfile.ZipFile(full_path, 'r') as zip_ref:
                zip_ref.extractall("C:/Users/HP/Downloads/EXL_Capstone/extracts")
            
            print("Extracted:", filename)
            break
        else:
            
            print("No <a> tag found in list item.")




import psycopg2
import pandas as pd
from psycopg2 import pool
from psycopg2.extras import execute_batch

class PostgresPool:
    _instance = None  # Singleton instance

    def __new__(cls, minconn=1, maxconn=5, dsn=""):
        if cls._instance is None:
            cls._instance = super(PostgresPool, cls).__new__(cls)
            cls._instance.pool = pool.SimpleConnectionPool(
                minconn, maxconn, dsn=dsn
            )
        return cls._instance

    def get_connection(self):
        return self.pool.getconn()

    def release_connection(self, conn):
        self.pool.putconn(conn)

    def close_all_connections(self):
        self.pool.closeall()

# Function to update table using execute_batch()
def update_table_execute_batch(df, table_name, update_columns, condition_column):
    DATABASE_URL = "dbname=mydb user=myuser password=mypass host=localhost port=5432"
    db_pool = PostgresPool(dsn=DATABASE_URL)  # Get the singleton pool

    conn = db_pool.get_connection()  # Get a connection from the pool
    cursor = conn.cursor()

    try:
        # Build dynamic SQL update query
        set_clause = ", ".join([f"{col} = %s" for col in update_columns])
        sql_query = f"UPDATE {table_name} SET {set_clause} WHERE {condition_column} = %s"

        # Convert DataFrame to list of tuples for execute_batch
        data_tuples = [
            tuple(row[col] for col in update_columns) + (row[condition_column],)
            for _, row in df.iterrows()
        ]

        # Execute batch update in chunks
        execute_batch(cursor, sql_query, data_tuples, page_size=1000)

        conn.commit()  # Commit transaction after batch update
        print(f"Updated {len(df)} rows in {table_name}.")

    except Exception as e:
        conn.rollback()  # Rollback transaction in case of error
        print(f"Error updating {table_name}: {e}")

    finally:
        cursor.close()
        db_pool.release_connection(conn)  # Return connection to pool

# Example usage
if __name__ == "__main__":
    # Creating a sample DataFrame with 50,000 rows
    data = {
        "id": range(1, 50001),
        "column1": ["new_value"] * 50000,
        "column2": ["updated_value"] * 50000
    }
    df = pd.DataFrame(data)

    # Updating table1 with new values from DataFr


import psycopg2
import pandas as pd
from psycopg2 import pool
from psycopg2.extras import execute_batch

# Singleton Connection Pool
class PostgresPool:
    _instance = None  # Singleton instance

    def __new__(cls, minconn=1, maxconn=5, dsn=""):
        if cls._instance is None:
            cls._instance = super(PostgresPool, cls).__new__(cls)
            cls._instance.pool = pool.SimpleConnectionPool(
                minconn, maxconn, dsn=dsn
            )
        return cls._instance

    def get_connection(self):
        return self.pool.getconn()

    def release_connection(self, conn):
        self.pool.putconn(conn)

    def close_all_connections(self):
        self.pool.closeall()

# Function to create and return a database connection
def create_connection():
    DATABASE_URL = "dbname=mydb user=myuser password=mypass host=localhost port=5432"
    db_pool = PostgresPool(dsn=DATABASE_URL)  # Get the singleton pool
    return db_pool.get_connection(), db_pool

# Function to fetch data from two tables and merge into a DataFrame
def fetch_and_prepare_df():
    conn, db_pool = create_connection()  # Get a connection
    cursor = conn.cursor()

    try:
        # Fetch data from table1
        cursor.execute("SELECT id, column1 FROM table1;")
        table1_data = cursor.fetchall()

        # Fetch data from table2
        cursor.execute("SELECT id, column2 FROM table2;")
        table2_data = cursor.fetchall()

        # Convert to DataFrames
        df1 = pd.DataFrame(table1_data, columns=["id", "column1"])
        df2 = pd.DataFrame(table2_data, columns=["id", "column2"])

        # Merge DataFrames on 'id'
        merged_df = pd.merge(df1, df2, on="id", how="inner")

        return merged_df

    except Exception as e:
        print(f"Error fetching data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error

    finally:
        cursor.close()
        db_pool.release_connection(conn)  # Return connection to pool

# Function to update a table using execute_batch()
def update_table_execute_batch(df, table_name, update_columns, condition_column):
    conn, db_pool = create_connection()  # Get a connection
    cursor = conn.cursor()

    try:
        if df.empty:
            print("No data to update.")
            return

        # Build dynamic SQL update query
        set_clause = ", ".join([f"{col} = %s" for col in update_columns])
        sql_query = f"UPDATE {table_name} SET {set_clause} WHERE {condition_column} = %s"

        # Convert DataFrame to list of tuples for execute_batch
        data_tuples = [
            tuple(row[col] for col in update_columns) + (row[condition_column],)
            for _, row in df.iterrows()
        ]

        # Execute batch update in chunks
        execute_batch(cursor, sql_query, data_tuples, page_size=1000)

        conn.commit()  # Commit transaction after batch update
        print(f"Updated {len(df)} rows in {table_name}.")

    except Exception as e:
        conn.rollback()  # Rollback on failure
        print(f"Error updating {table_name}: {e}")

    finally:
        cursor.close()
        db_pool.release_connection(conn)  # Return connection to pool

# Main function to fetch data and update table3
if __name__ == "__main__":
    df = fetch_and_prepare_df()  # Fetch and prepare DataFrame

    if not df.empty:
        update_table_execute_batch(df, "table3", ["column1", "column2"], "id")
    else:
        print("No updates were performed.")


Here’s a detailed few-shot prompt you can use with the Mistral 24B model to classify whether a word is PHI (Protected Health Information) or not. The output should be in JSON format.


---

Prompt:

You are an expert classifier that determines whether a given word is PHI (Protected Health Information) or not.
Follow these rules:

General terms (like "hospital", "sex", "dob") are not PHI.

Specific entities (like "Lotus Hospital", actual names, specific dates) are PHI.

Gender identifiers ("male", "female") are PHI, but the word "sex" alone is not PHI.

Any specific information that can personally identify someone is PHI.


Return the classification as JSON with "word" and "is_phi" fields.

Examples:

[
  {"word": "hospital", "is_phi": false},
  {"word": "Lotus Hospital", "is_phi": true},
  {"word": "sex", "is_phi": false},
  {"word": "male", "is_phi": true},
  {"word": "female", "is_phi": true},
  {"word": "dob", "is_phi": false},
  {"word": "12-05-1992", "is_phi": true},
  {"word": "John Doe", "is_phi": true},
  {"word": "address", "is_phi": false},
  {"word": "123 Main Street", "is_phi": true}
]

Task:

Now, classify the following words:
{{your_word_list_here}}


---

How to Use It?

Replace {{your_word_list_here}} with your actual list of words.

The model will output a JSON array where each word is classified.

Ensure the model understands that specific identifiers are PHI while general terms are not.


Would you like to refine the criteria further or add more edge cases?


