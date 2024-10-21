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

# Sample DataFrame for multiple files
data = {
    'file': ['file 1', 'file 1', 'file 1', 'file 1', 'file 1', 'file 1', 'file 1',
             'file 2', 'file 2', 'file 2', 'file 2', 'file 2'],
    'page': [1, 2, 3, 4, 15, 16, 17, 1, 2, 12, 22, 32],
    'flag': [1, 0, 0, 0, -1, 0, 0, 1, 0, -1, 0, 1],
    'class': ['a', 'b', 'a', 'c', 'c', 'b', 'b', 'x', 'y', 'x', 'z', 'w']
}
df = pd.DataFrame(data)

# Function to update the 'new_class' column based on the flag logic
def update_class_for_file(group):
    group = group.reset_index(drop=True)
    
    n = len(group)
    new_classes = group['class'].tolist()  # Store classes in a list for efficiency
    current_mode = None  # Initialize the current mode
    
    # Iterate through each row
    for idx in range(n):
        flag = group.at[idx, 'flag']
        current_page = group.at[idx, 'page']
        
        if flag == 1:
            # Start using 'x' when flag is 1
            current_mode = 'x'
            
            # Step 1: Check the next 30 pages for flag 1 or -1
            max_check_page = current_page + 30
            next_30_pages_flags = group[(group['page'] > current_page) & (group['page'] <= max_check_page)]['flag'].values
            
            # Step 2: If no 1 or -1 in the next 30 pages, update only the next 7 pages
            if not any(flag in next_30_pages_flags for flag in [1, -1]):
                for j in range(1, 8):
                    if idx + j < n:
                        new_classes[idx + j] = 'x'
                current_mode = None  # Reset mode after updating 7 pages
        
        elif flag == -1:
            # Start using 'y' when flag is -1
            current_mode = 'y'
            
            # Step 1: Check the next 30 pages for flag 1 or -1
            max_check_page = current_page + 30
            next_30_pages_flags = group[(group['page'] > current_page) & (group['page'] <= max_check_page)]['flag'].values
            
            # Step 2: If no 1 or -1 in the next 30 pages, update only the next 7 pages
            if not any(flag in next_30_pages_flags for flag in [1, -1]):
                for j in range(1, 8):
                    if idx + j < n:
                        new_classes[idx + j] = 'y'
                current_mode = None  # Reset mode after updating 7 pages
        
        # Apply the current mode to the new_class column if it's set
        if current_mode:
            new_classes[idx] = current_mode
    
    # Assign the new class values back to the DataFrame column
    group['new_class'] = new_classes
    
    return group

# Apply the function to each group (each file)
df = df.groupby('file', group_keys=False).apply(update_class_for_file).reset_index(drop=True)

# Output the resulting DataFrame
print(df)

