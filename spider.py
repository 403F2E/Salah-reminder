from requests import get
from urllib3 import disable_warnings, exceptions
from bs4 import BeautifulSoup 
from pandas import DataFrame
from datetime import datetime
from time import strftime
from json import load, dump
from subprocess import run


today, current_time = datetime.today().day, strftime("%H:%M")

time_pile: dict = {}

try:
    with open('pile.json', 'r') as f:
        time_pile = load(f) # type: ignore
except Exception as e:
    print(f'Error loading the file "pile.json"! {e}')
    exit()


time_pile["status"] = "disallowed"
time_pile['current'].append(time_pile["waiting"][0])
time_pile['waiting'].pop(0)

# if it is not the cronjob that calls this file scrape the website again
if today != time_pile["today"] or current_time != time_pile["waiting"][0] or True:
    disable_warnings(exceptions.InsecureRequestWarning)

    # Fetch the needed table for the current month
    url: str = 'https://habous.gov.ma/prieres/horaire_hijri_2.php?ville=104'
    response = get(url, verify=False)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')  
    else:
        print('Failed to retrieve the webpage')
        exit()

    html_table = soup.find('table')  
    rows: list = html_table.find_all('tr') # type: ignore

    data: list = []
    for row in rows:
        columns: list = row.find_all(['td'])
        data.append([col.text.strip() for col in columns])

    table = DataFrame(data)

    todays_times = table[1:31][table[1:31][2].astype(int) == today]
    hour = todays_times.loc[:, 3:9][todays_times.loc[:, 3:9] >= current_time].stack().values # type: ignore

    time_pile["today"] = today
    time_pile["waiting"] = list(hour)

time_pile["status"] = "allow"

try:
    with open('pile.json', 'w') as f:
        dump(time_pile, f)
except Exception as e:
    print(f'Error writing to the file "pile.json"! {e}')
    exit()

## uncomment the line below if your system is windows and comment the other
run(["powershell", "-command", "Here the path to your cronjob.py file"])

## uncomment the line below if your system is linux and comment the other
# run(["python3", "Here the path to your cronjob.py file"])
