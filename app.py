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

# Creating the dataframe
data = {'filename': ['file1']*12,
        'page': list(range(1, 13)),
        'class': [[] for _ in range(12)],
        'flag': [1, 0, 0, 0, 0, -1, 0, 0, 1, -1, 1, 0]}

df = pd.DataFrame(data)

def process_flags(df):
    i = 0
    n = len(df)
    
    while i < n:
        if df.loc[i, 'flag'] == 1:
            # Search for the next +1 or -1 within 30 rows
            found = False
            for j in range(i + 1, min(i + 31, n)):
                if df.loc[j, 'flag'] in [-1, 1]:
                    # Append 'pn' to the rows up to the found +1 or -1
                    df.loc[i+1:j, 'class'] = df.loc[i+1:j, 'class'].apply(lambda x: x + ['pn'])
                    i = j  # Move to the found row
                    found = True
                    break
            if not found:
                # If no -1 or +1 found, append 'pn' to the next 5 rows
                df.loc[i+1:min(i+6, n), 'class'] = df.loc[i+1:min(i+6, n), 'class'].apply(lambda x: x + ['pn'])
                i += 6  # Skip the next 6 rows
        elif df.loc[i, 'flag'] == -1:
            # Remove 'pn' from rows until the next +1
            for j in range(i + 1, n):
                if df.loc[j, 'flag'] == 1:
                    i = j  # Move to the found +1
                    break
                df.loc[j, 'class'] = []
        else:
            i += 1  # Continue to the next row if flag is 0 or any other value
    
    return df

# Process the dataframe
df_processed = process_flags(df)
df_processed
