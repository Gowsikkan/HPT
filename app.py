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


import os
import pandas as pd
import PyPDF2
from PIL import Image

def extract_class(pdf_name, df):
    """
    Extracts the class for all pages of a particular PDF.
    
    Args:
    - pdf_name (str): Name of the PDF file.
    - df (DataFrame): DataFrame containing PDF names, classes, and page numbers.
    
    Returns:
    - dict: Dictionary containing page numbers as keys and corresponding classes as values.
    """
    pdf_classes = {}
    pdf_df = df[df['pdf_name'] == pdf_name]
    for index, row in pdf_df.iterrows():
        pdf_classes[row['pg_no']] = row['class']
    return pdf_classes

def take_screenshot(pdf_path, output_folder, pdf_classes):
    """
    Takes screenshots of pages in the PDF and saves them in the specified folder structure.
    
    Args:
    - pdf_path (str): Path to the PDF file.
    - output_folder (str): Path to the output folder.
    - pdf_classes (dict): Dictionary containing page numbers and their corresponding classes.
    """
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfFileReader(file)
        for page_num in range(pdf_reader.numPages):
            page = pdf_reader.getPage(page_num)
            image = Image.frombytes('RGB', page.mediaBox.dimensions, page.extractText())
            class_folder = os.path.join(output_folder, pdf_classes.get(page_num + 1, 'Unknown'))
            os.makedirs(class_folder, exist_ok=True)
            image_path = os.path.join(class_folder, f'page_{page_num + 1}.png')
            image.save(image_path)

def main(pdf_name, df, folder_location):
    """
    Main function to extract class information, take screenshots, and store them.
    
    Args:
    - pdf_name (str): Name of the PDF file.
    - df (DataFrame): DataFrame containing PDF names, classes, and page numbers.
    - folder_location (str): Location of the folder containing PDF files.
    """
    pdf_path = os.path.join(folder_location, pdf_name)
    pdf_classes = extract_class(pdf_name, df)
    take_screenshot(pdf_path, folder_location, pdf_classes)

# Example usage:
if __name__ == "__main__":
    # Assuming df is a DataFrame containing columns: 'pdf_name', 'class', 'pg_no'
    df = pd.DataFrame({
        'pdf_name': ['example.pdf', 'example.pdf', 'example.pdf'],
        'class': ['ClassA', 'ClassA', 'ClassB'],
        'pg_no': [1, 2, 3]
    })
    pdf_name = 'example.pdf'
    folder_location = '/path/to/folder'
    main(pdf_name, df, folder_location)

