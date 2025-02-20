from requests import get
from bs4 import BeautifulSoup 
from pandas import DataFrame
from urllib3 import disable_warnings, exceptions
from datetime import datetime


disable_warnings(exceptions.InsecureRequestWarning)

# Fetch the needed table of the cuurent month
url = 'https://habous.gov.ma/prieres/horaire_hijri_2.php?ville=104'
response = get(url, verify=False)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')  
else:
    print('Failed to retrieve the webpage')
    exit()

html_table = soup.find('table')  
rows = html_table.find_all('tr') # type: ignore

data = []
for row in rows:
    columns = row.find_all(['td'])
    data.append([col.text.strip() for col in columns])

table = DataFrame(data)
'''
print(table)
           0                   1               2      3       4      5      6       7
0     الأيام               شعبان  يناير / فبراير  الصبح  الشروق  الظهر  العصر  المغرب
1     الجمعة                   1              31  06:57   08:20  13:51  16:45   19:12
2      السبت                   2               1  06:56   08:20  13:51  16:46   19:13
3      الأحد                   3               2  06:56   08:19  13:51  16:46   19:14
4    الإثنين                   4               3  06:55   08:18  13:51  16:47   19:14
5   الثلاثاء                   5               4  06:55   08:18  13:51  16:48   19:15
6   الأربعاء                   6               5  06:54   08:17  13:51  16:48   19:16
7     الخميس                   7               6  06:53   08:16  13:51  16:49   19:17
8     الجمعة                   8               7  06:53   08:16  13:51  16:50   19:18
9      السبت                   9               8  06:52   08:15  13:51  16:50   19:19
10     الأحد                  10               9  06:51   08:14  13:51  16:51   19:20
11   الإثنين                  11              10  06:51   08:13  13:51  16:52   19:21
12  الثلاثاء                  12              11  06:50   08:12  13:51  16:52   19:21
13  الأربعاء                  13              12  06:49   08:11  13:51  16:53   19:22
14    الخميس                  14              13  06:48   08:11  13:51  16:54   19:23
15    الجمعة                  15              14  06:48   08:10  13:51  16:54   19:24
16     السبت                  16              15  06:47   08:09  13:51  16:55   19:25
17     الأحد                  17              16  06:46   08:08  13:51  16:55   19:26
18   الإثنين                  18              17  06:45   08:07  13:51  16:56   19:26
19  الثلاثاء                  19              18  06:44   08:06  13:51  16:57   19:27
20  الأربعاء                  20              19  06:43   08:05  13:51  16:57   19:28
21    الخميس                  21              20  06:42   08:04  13:51  16:58   19:29
22    الجمعة                  22              21  06:41   08:03  13:51  16:58   19:30
23     السبت                  23              22  06:40   08:02  13:51  16:59   19:31
24     الأحد                  24              23  06:39   08:01  13:50  16:59   19:31
25   الإثنين                  25              24  06:38   08:00  13:50  17:00   19:32
26  الثلاثاء                  26              25  06:37   07:59  13:50  17:00   19:33
27  الأربعاء                  27              26  06:36   07:57  13:50  17:01   19:34
28    الخميس                  28              27  06:35   07:56  13:50  17:01   19:34
29    الجمعة                  29              28  06:34   07:55  13:50  17:01   19:35
30     السبت  حسب نتيجة المراقبة               1  06:33   07:54  13:49  17:02   19:36
'''

today = datetime.today().month
print(table[1:30][table[1:30][2].astype(int) == today])
