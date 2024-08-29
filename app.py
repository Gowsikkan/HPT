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

import pandas as pd

def calculate_class_percentages(df, class_column, count_column):
    # Initialize dictionaries to store counts and percentages
    counts = {'single': 0, 'double': 0, 'triple': 0}

    # Calculate counts of single, double, and triple classes
    total_count = 0
    for _, row in df.iterrows():
        class_count = len(row[class_column])
        total_count += row[count_column]
        if class_count == 1:
            counts['single'] += row[count_column]
        elif class_count == 2:
            counts['double'] += row[count_column]
        elif class_count == 3:
            counts['triple'] += row[count_column]

    # Calculate percentages
    percentages = {key: (value / total_count) * 100 for key, value in counts.items()}

    return percentages

# Create DataFrame
data = {'class': [['cs'], ['cs', 'pq'], ['cs', 'pq', 'at'], ['cs', 'pq', 'dd']],
        'count': [100, 23, 10, 7]}
df = pd.DataFrame(data)

# Call the function
result = calculate_class_percentages(df, 'class', 'count')

# Print percentages
for key, value in result.items():
    print("Percentage of {} classes: {:.2f}%".format(key, value))


CM Analysis : 
         Initially CM graded samples were selected from the golden data
         Got the count of  SME provided keyword for both CM and DD on all the samples .
         Get the keywords of the sentence from keybert and created a similarity matrix score for each sample.

Selectction strategy:
              Select samples if one or more CM keyword is present or
               select samples if 2 or more DD kyowrd is present or 
               select sample if similarity score is grater than 0.68 (from violin plot)

PQ Analysis : 
         Initially PQ graded samples were selected from the golden data
         Got the count of  SME provided keyword for all the graded samples .
         Got the count of SME provides keyword in entire golden data
         
Selection strategy:
              Samples are selected if more than 2 PQ keyword is present


import pandas as pd

# Create the initial DataFrame
import pandas as pd

# Sample data
data = {
    'Filename': ['pdf1', 'pdf1', 'pdf1', 'pdf1', 'pdf1', 'pdf1', 'pdf2', 'pdf2','pdf3','pdf3'],
    'page': [
        [1, 2, 3],
        [6, 8, 10, 11],
        [12, 13, 14],
        [15, 17, 19, 21, 22],
        [26, 27, 28, 29, 30],
        [7, 16, 18, 23, 24, 25],
        [1, 2, 3, 4, 6, 7, 9],
        [5],
        [1,2,3,5,7],
        [4,6,8]
    ],
    'class': ['A', 'B', 'C', 'D', 'E', 'X', 'A', 'X','C','X']
}

# Create the dataframe
df = pd.DataFrame(data)

# Function to process the dataframe
def process_dataframe(df):
    for filename in df['Filename'].unique():
        # Filter by the current filename
        sub_df = df[df['Filename'] == filename]
        pages_dict = {row['class']: row['page'] for _, row in sub_df.iterrows()}
        
        if 'X' in pages_dict:
            x_pages = pages_dict['X']
            new_x_pages = []
            for page in x_pages:
                prev_class = next_class = None
                for cls, pages in pages_dict.items():
                    if cls != 'X':
                        if page - 1 in pages:
                            prev_class = cls
                        if page + 1 in pages:
                            next_class = cls
                # If both previous and next pages belong to the same class, reassign the page
                if prev_class and prev_class == next_class:
                    pages_dict[prev_class].append(page)
                else:
                    new_x_pages.append(page)
            # Update the pages for class X
            pages_dict['X'] = new_x_pages
            # Update the dataframe
            for cls, pages in pages_dict.items():
                df.loc[(df['Filename'] == filename) & (df['class'] == cls), 'page'] = [pages]
    
    # Remove empty class X rows
    # df = df[~((df['class'] == 'X') & (df['page'].apply(len) == 0))]
    return df

# Process the dataframe
updated_df = process_dataframe(df)
print(updated_df)

import pandas as pd
import json
import os

def json_to_dataframe(json_data):
    data = []
    for filename, details in json_data.items():
        for class_name, class_details in details['Result'].items():
            pages = class_details['classification_pages']
            data.append([filename, class_name, pages])
    
    df = pd.DataFrame(data, columns=['file_name', 'class', 'page'])
    return df

def load_and_merge_json_files(directory_path):
    merged_data = {}
    
    for file_name in os.listdir(directory_path):
        if file_name.endswith('.json'):
            file_path = os.path.join(directory_path, file_name)
            with open(file_path, 'r') as f:
                json_data = json.load(f)
                merged_data.update(json_data)
    
    return merged_data

# Directory containing JSON files (replace with your directory path)
directory_path = 'path/to/your/json/files'

# Load and merge JSON data from files in the directory
merged_json_data = load_and_merge_json_files(directory_path)

# Convert merged JSON to DataFrame
df = json_to_dataframe(merged_json_data)

print(df)

import pandas as pd
import json
import os

class JSONProcessor:
    def __init__(self, directory_path, all_classes):
        self.directory_path = directory_path
        self.all_classes = all_classes

    def json_to_dataframe(self, json_data):
        data = []
        cls = []

        for class_name, class_details in json_data['Result'].items():
            cls.append(class_name)
            pages = class_details['classification_pages']
            data.append([json_data['Filename'], class_name, pages])

        for class_name in self.all_classes:
            if class_name not in cls:
                data.append([json_data['Filename'], class_name, []])

        df = pd.DataFrame(data, columns=['file_name', 'class', 'page'])
        return df

    def load_and_process_json_files(self):
        res = pd.DataFrame()

        for file_name in os.listdir(self.directory_path):
            if file_name.endswith(".json"):
                file_path = os.path.join(self.directory_path, file_name)
                with open(file_path, 'r') as f:
                    json_data = json.load(f)
                    df = self.json_to_dataframe(json_data)
                    res = pd.concat([res, df]).reset_index(drop=True)

        return res

# Directory containing JSON files (replace with your directory path)
directory_path = 'outputs/1719517846/'

# List of all possible classes (update this list based on your classes)
all_classes = ['A', 'B', 'C']  # Add more classes if needed

# Create an instance of JSONProcessor
processor = JSONProcessor(directory_path, all_classes)

# Load, process JSON data from files in the directory, and convert to DataFrame
result_df = processor.load_and_process_json_files()

print(result_df)

import pandas as pd

# Sample data
data = {
    'filename': ['file1', 'file1', 'file2', 'file2'],
    'page': [1, 2, 1, 2],
    'text': ["some text with keyword", "some other text", "keyword present here", "another keyword"],
    'pred_class': [['ao', 'hp'], ['ed', 'cp'], ['ao'], ['ar']],
    'ar_proba': [0.04, 0.6, 0.8, 0.3]
}

df = pd.DataFrame(data)

# Keyword to search for
keyword = "keyword"

# Process each file
for filename, file_df in df.groupby('filename'):
    # Initialize a counter for added 'ar' classes
    ar_added_count = 0

    # Check pages with 'ao', 'ed', 'hp' classes
    for class_to_check in ['ao', 'ed', 'hp']:
        for idx, row in file_df.iterrows():
            if class_to_check in row['pred_class'] and keyword in row['text']:
                df.at[idx, 'pred_class'].append('ar')
                ar_added_count += 1
                if ar_added_count == 3:
                    break
        if ar_added_count == 3:
            break

    # If no 'ar' class added, check individually predicted 'ar' pages
    if ar_added_count < 3:
        for idx, row in file_df.iterrows():
            if row['pred_class'] == ['ar'] and keyword in row['text']:
                if 'ar' not in df.at[idx, 'pred_class']:
                    df.at[idx, 'pred_class'].append('ar')
                    ar_added_count += 1
                if ar_added_count == 3:
                    break

    # Remove 'ar' class from all other pages not updated
    for idx, row in file_df.iterrows():
        if 'ar' in row['pred_class'] and ar_added_count < 3:
            row['pred_class'].remove('ar')

# Ensure that each file has a maximum of 3 pages with 'ar' class
for filename, file_df in df.groupby('filename'):
    ar_pages = file_df[file_df['pred_class'].apply(lambda x: 'ar' in x)]
    if len(ar_pages) > 3:
        excess_ar_pages = ar_pages.iloc[3:]
        for idx in excess_ar_pages.index:
            df.at[idx, 'pred_class'].remove('ar')

print(df)

def group_pages_and_cnfx(pages, cnfx):
    grouped_pages = []
    grouped_cnfx = []
    temp_pages = [pages[0]]
    temp_cnfx = [cnfx[0]]
    
    for i in range(1, len(pages)):
        if pages[i] == pages[i-1] + 1:
            temp_pages.append(pages[i])
            temp_cnfx.append(cnfx[i])
        else:
            grouped_pages.append(temp_pages)
            grouped_cnfx.append(temp_cnfx)
            temp_pages = [pages[i]]
            temp_cnfx = [cnfx[i]]
    
    # Append the last group
    grouped_pages.append(temp_pages)
    grouped_cnfx.append(temp_cnfx)
    
    return grouped_pages, grouped_cnfx

# Apply the function to the DataFrame
df[['page', 'cnfx']] = df.apply(lambda row: group_pages_and_cnfx(row['page'], row['cnfx']), axis=1, result_type='expand')

print(df)



import pandas as pd

# Sample DataFrame
data = {
    'file': [1, 1, 1, 1, 1, 2, 2, 2],
    'page': [1, 2, 3, 4, 5, 6, 7, 8],
    'class': [['ds', 'cm'], ['ds', 'cm'], ['ds', 'cm'], ['cm'], ['ds', 'cm'], ['ds', 'cm'], ['cm'], ['ds', 'cm']]
}

df = pd.DataFrame(data)

def retain_max_continuous_ds(df):
    segments = []
    current_segment = []

    # Identify all continuous 'ds' segments
    for _, row in df.iterrows():
        if 'ds' in row['class']:
            current_segment.append(row['page'])
        else:
            if current_segment:
                segments.append(current_segment)
            current_segment = []

    # Final check in case the last segment is the longest
    if current_segment:
        segments.append(current_segment)

    # Determine the maximum segment length
    max_length = max(len(segment) for segment in segments) if segments else 0

    # Retain 'ds' only in segments with the maximum length
    max_segments = [segment for segment in segments if len(segment) == max_length]

    # Update the DataFrame to remove 'ds' from pages not in the max segments
    if max_segments:
        pages_with_max_ds = [page for segment in max_segments for page in segment]
        df['class'] = df.apply(lambda row: [cls for cls in row['class'] if cls != 'ds'] 
                               if row['page'] not in pages_with_max_ds else row['class'], axis=1)
    
    return df

# Apply the function to each file group
df = df.groupby('file').apply(retain_max_continuous_ds).reset_index(drop=True)

print(df)


def combine_pages(input_list):
    if not input_list:
        return []
    
    output_list = []
    offset = 0
    previous_value = None
    
    for current_value in input_list:
        if previous_value is not None and current_value <= previous_value:
            # Adjust offset whenever the sequence starts repeating
            offset += previous_value
        
        output_list.append(current_value + offset)
        previous_value = current_value
    
    return output_list

# Test cases
input1 = [1, 2, 3, 4, 1, 2, 3]
output1 = combine_pages(input1)
print(output1)  # Expected: [1, 2, 3, 4, 5, 6, 7]

input2 = [1, 2, 3, 4, 5, 6, 8, 2, 3, 4, 2, 3]
output2 = combine_pages(input2)
print(output2)  # Expected: [1, 2, 3, 4, 5, 6, 8, 10, 11, 12, 14, 15]


