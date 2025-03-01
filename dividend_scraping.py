import time
import requests
from datetime import date
from bs4 import BeautifulSoup
from selenium import webdriver
'''from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions #as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--disable-webgl")
options.add_experimental_option("excludeSwitches", ["enable-logging"])
service = Service("C:\\Users\\toby\\.vscode\\chromedriver.exe")
driver = webdriver.Chrome(service=service,options=options)
'''

# gets html of a website given the url as an argument
# returns html as a string
def get_html(url):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(5)
    html = driver.page_source
    driver.quit()

    return html


# returns the number of a company in a list - e.g. CBA = 1 etc
# returns -1 if an error occurs
def match_firm_price(name, name_list):
    for i in range(200):
        if name == name_list[i]:
            return i
    return -1

# enter two strings which contain price and dividend
# form $0.00
def calculate_yield(curr_price, dividend):
    temp_price = float(curr_price[1:])
    temp_dividend = float(dividend[1:])
    return temp_dividend / temp_price * 100


'''options = webdriver.ChromeOptions() 
options.add_argument("start-maximized")
# to supress the error messages/logs
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver_one = webdriver.Chrome(options=options, executable_path=r'C:\\WebDrivers\\chromedriver.exe')
'''

html = get_html("https://www.marketindex.com.au/asx-listed-companies")
'''
table = driver.find_elements(By.TAG_NAME, "tr")
# table is a list of web elements
# mi-table mt-6

print(table[1].get_attribute("outerHTML"))

for row in table:
    continue
    #name = row.find_element(By.TAG_NAME, "a")
    #price = row.find_element(By.CLASS_NAME, "text-right")
    #print(f"{name}\n")
'''

soup_one = BeautifulSoup(html, 'html.parser')

locator = 'div table tbody tr td.sticky-column a'
item_links = soup_one.select(locator)

top200_names = [item.text for item in item_links]
top200_names = top200_names[:200]

locator = 'div table tbody tr td.text-right'
item_links = soup_one.select(locator)
top200_prices = []

for i in range(len(item_links)):
    if i % 5 == 0:
        top200_prices.append(item_links[i].text)

html = get_html("https://www.marketindex.com.au/upcoming-dividends")

soup_two = BeautifulSoup(html, 'html.parser')

# first find the name of the dividend giver
locator = '#sticky-table table.mi-table tbody td.sticky-column a'
item_links = soup_two.select(locator)

dividend_names = [item.text for item in item_links]
#print(dividend_names)

locator = '#sticky-table table.mi-table tbody td.text-right.font-tabular'
item_links = soup_two.select(locator)
raw_data = [item.text for item in item_links]
#print(raw_data)

# now get rid of days, interimness, pay date, yield, price

filtered_data = []
for i in range(len(raw_data)):
    if i % 8 == 0 or i % 8 >= 4:
        continue
    else:
        filtered_data.append(raw_data[i])

result_data = []

index = 0
for name in dividend_names:
    if name not in top200_names:
        index += 3
        continue
    else:
        temp_list = []
        temp_list.append(name)
        curr_price = top200_prices[match_firm_price(name, top200_names)]
        temp_list.append(curr_price)
        for _ in range(3):
            temp_list.append(filtered_data[index])
            index += 1
        
        temp_list.append(f"{calculate_yield(curr_price, temp_list[3])}%")
        temp_list = tuple(temp_list)
        result_data.append(temp_list)


if len(result_data) == 0:
    print("No results to show at the moment.\n")
else:
    print("Company\tPrice\tEx date\tDiv\tFrank%\tYield")
    for result in result_data:
        print('\t'.join(result))
print(date.today())