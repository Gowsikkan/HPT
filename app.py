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
            4
            import pandas as pd

# Your JSON data
json_data = {
    "reporting_entity_name": "UBH TPA CLAIMS",
    "reporting_entity_type": "Third-Party Administrator",
    "plan_name": "BH-EAP-BLUE-BELL-TRUST-PPO",
    "plan_id_type": "EIN",
    "plan_id": "00000013",
    "plan_market_type": "group",
    "out_of_network": [{
        "name": "SUBSEQUENT HOSPITAL CARE",
        "billing_code_type": "CPT",
        "billing_code_type_version": "2023",
        "billing_code": "99232",
        "description": "SUBSEQUENT HOSPITAL CARE",
        "allowed_amounts": [{
            "tin": {"type": "ein", "value": "030417452"},
            "service_code": ["51"],
            "billing_class": "professional",
            "payments": [{"allowed_amount": 140.00,
                           "providers": [{"billed_charge": 140.00,
                                          "npi": [1528532728]}]}]
        }]
    }, {
        "name": "SUBSEQUENT HOSPITAL CARE",
        "billing_code_type": "CPT",
        "billing_code_type_version": "2023",
        "billing_code": "99233",
        "description": "SUBSEQUENT HOSPITAL CARE",
        "allowed_amounts": [{
            "tin": {"type": "ein", "value": "030417452"},
            "service_code": ["51"],
            "billing_class": "professional", 
            "payments": [{"allowed_amount": 202.00,
                           "providers": [{"billed_charge": 202.00,
                                          "npi": [1528532728, 1356462972]}]}]
        }]
    },
                       {
        "name": "SUBSEQUENT HOSPITAL CARE",
        "billing_code_type": "CPT",
        "billing_code_type_version": "2023",
        "billing_code": "99233",
        "description": "SUBSEQUENT HOSPITAL CARE",
        "allowed_amounts": [{
            "tin": {"type": "ein", "value": "030417452"},
            "service_code": ["51"],
            "billing_class": "professional",
            "payments": [{"allowed_amount": 202.00,
                           "providers": [{"billed_charge": 202.00,
                                          "npi": [15]}]}]
        }]
    }],
    "last_updated_on": "2023-12-01",
    "version": "1.0.0"
}

# Create a DataFrame for allowed amounts
allowed_amounts_data = []

for item in json_data["out_of_network"]:
    for amount in item["allowed_amounts"]:
        for payment in amount["payments"]:
            for provider in payment["providers"]:
                allowed_amounts_data.append({
                    "Name": item["name"],
                    "Billing Code": item["billing_code"],
                    "Description": item["description"],
                    "TIN Type": amount["tin"]["type"],
                    "TIN Value": amount["tin"]["value"],
                    "Service Code": ",".join(amount["service_code"]),
                    "Billing Class": amount["billing_class"],
                    "Allowed Amount": payment["allowed_amount"],
                    "Billed Charge": provider["billed_charge"],
                    "NPI": ",".join(map(str, provider["npi"]))
                })

# Create a DataFrame
df = pd.DataFrame(allowed_amounts_data)
df
# Save to Excel
# df.to_excel("allowed_amounts_data.xlsx", index=False)


if __name__=="__main__":
    url = "https://transparency-in-coverage.optum.com/"
    response = requests.get(url)

    if response.status_code == 200:
            urls=download_zip(url)
    else:
        print(f"Error accessing page:")
    
