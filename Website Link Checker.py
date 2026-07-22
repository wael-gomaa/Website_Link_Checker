import requests
from bs4 import BeautifulSoup
import csv  
import json
from openpyxl import Workbook
from urllib.parse import urljoin

CSV_FILE = "Website_Link_Checker/report.csv"
JSON_FILE = "Website_Link_Checker/report.json"
EXCEL_FILE = "Website_Link_Checker/report.xlsx"



def save_csv(broken_or_working_list):

    with open(CSV_FILE , "w" , newline="" , encoding="utf-8") as file:

        writer = csv.writer(file)

        writer.writerow(["Broken or not"])

        for link in broken_or_working_list:
            writer.writerow([link])
    

def save_json(broken_or_working_list):

    with open(JSON_FILE , "w" , encoding="utf-8") as file:

        json.dump(broken_or_working_list , file , indent=4)


def save_excel(broken_or_working_list):

    workbook = Workbook()

    sheet = workbook.active

    sheet.append(["Broken or not"])

    for link in broken_or_working_list:

        sheet.append([link])

    workbook.save(EXCEL_FILE)


Broken_or_working = []


url = input("enter the full website url: ")

try:
    response = requests.get(url)
except Exception:
    print("Failed to load the page")
    exit()


if response.status_code != 200:
    print("Failed to load the page")
    exit()

soup = BeautifulSoup(response.text , "html.parser")


urls = soup.select("a[href]")

if not urls:
    print("The websites does not have links")
    exit()

for web_url in urls:

    
    
    web_url = urljoin(url , web_url["href"])

    try:
        link_response = requests.get(web_url)
    except Exception:
        continue

    if link_response.status_code != 200:
        Broken_or_working.append(f"this link is Broken {web_url}")
    
    else:
        Broken_or_working.append(f"this link is Working {web_url}")

save_csv(Broken_or_working)
save_json(Broken_or_working)
save_excel(Broken_or_working)

