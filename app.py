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

# Assuming df1 and df2 are your DataFrames
# Replace this with your actual DataFrames

# Sample data for demonstration
data1 = {'name': ['Alice', 'Bob', 'Charlie'],
         'age': [25, 30, 35],
         'plan_name': ['Basic', 'Standard', 'Premium'],
         'flag': [0, 0, 0]}

data2 = {'name': ['Bob', 'Charlie', 'David'],
         'age': [30, 35, 28],
         'plan_name': ['Standard', 'Premium', 'Basic'],
         'flag': [0, 0, 0]}

df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)

# Iterate through rows in df2
for index, row in df2.iterrows():
    plan_name = row['plan_name']
    
    # Check if plan_name exists in df1
    if plan_name in df1['plan_name'].values:
        # Check if all other columns are equal
        matching_rows = df1[df1['plan_name'] == plan_name]
        matching_rows = matching_rows[(matching_rows[['name', 'age']] == row[['name', 'age']]).all(axis=1)]

        if not matching_rows.empty:
            # Update flag to 1 for the matched rows in df1
            df1.loc[matching_rows.index, 'flag'] = 1
        else:
            # If no matching rows found, append the row from df2 to df1
            df1 = df1.append(row, ignore_index=True)
            # Update flag to 1 for the newly appended row
            df1.loc[df1.index[-1], 'flag'] = 1

# Display the updated df1
print(df1)
