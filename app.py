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
import pandas as pd

def append_to_excel(df, excel_file_path):
    try:
        # Read existing data from Excel
        existing_df = pd.read_excel(excel_file_path)

        # Identify the common 'plan_name' values between df and existing_df
        common_plan_names = df[df['plan_name'].isin(existing_df['plan_name'])]['plan_name']

        # Change 'flag' to 0 for common 'plan_name' in existing_df
        existing_df.loc[existing_df['plan_name'].isin(common_plan_names), 'flag'] = 0

        # Append df to existing_df
        result_df = pd.concat([existing_df, df], ignore_index=True)

        # Save the result back to Excel
        result_df.to_excel(excel_file_path, index=False)
        print("Data appended to Excel with updated flags.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
# Replace these with your actual DataFrame and Excel file path
df_to_append = pd.DataFrame({'plan_name': ['a', 'b'], 'flag': [1, 1]})
excel_file_path = 'your_excel_file.xlsx'

append_to_excel(df_to_append, excel_file_path)
