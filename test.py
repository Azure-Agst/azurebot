import json
import requests
from bs4 import BeautifulSoup


# Get Release Notes Page
page = requests.get('https://macadmins.software/latest.xml').content
pagedata = BeautifulSoup(page, "xml")
id_arr = pagedata.find_all('id')
version_arr = pagedata.find_all('version')
for i in range(len(id_arr)):
    if id_arr[i].get_text() == "com.microsoft.office.suite.2016":
        version = version_arr[i].get_text()

print(f"Version: {version}")