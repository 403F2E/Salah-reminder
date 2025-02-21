from requests import get
from urllib3 import disable_warnings, exceptions
from bs4 import BeautifulSoup 
from pandas import DataFrame
from datetime import datetime
from time import strftime
from json import load

disable_warnings(exceptions.InsecureRequestWarning)

# Fetch the needed table of the current month
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

today, current_time = datetime.today().day, strftime("%H:%M")

todays_times = table[1:31][table[1:31][2].astype(int) == today]

time_pile: dict = {}

try:
    with open('pile.json', 'r') as f:
        time_pile = load(f) # type: ignore
except Exception as e:
    print(f'Error loading the file "pile.json"! {e}')
    exit()

time_pile["status"] = "disallowed"
time_pile['current'] = time_pile["waiting"]

if current_time == time_pile["waiting"]:
    time_pile["waiting"] = todays_times[todays_times[1] == time_pile["waiting"]] # type: ignore
else:
    ''' 

    need a fix: logic of the else clause needs to be rewritten using pandas logic 
        # hour = list(todays_times.loc[:, 3:9][todays_times.loc[:, 3:9] != current_time])
        # time_pile["waiting"] = hour if hour != Nan else current_time # type: ignore

    '''
    old_waiting = time_pile["waiting"]

    for index in range(3, 9):
        if todays_times.loc[:, index].item() >= current_time: # type: ignore
            time_pile["waiting"] = todays_times.loc[:, index].item() # type: ignore
            break
    if time_pile["waiting"] == old_waiting:
        print("cannot found the correct time execute the cronjob upon!!")
        exit()

print(time_pile)
time_pile["status"] = "allow"


# try:
#     with open('pile.json', 'w') as f:
#         dump(time_pile, f)
# except Exception as e:
#     print(f'Error writing to the file "pile.json"! {e}')
#     exit()
