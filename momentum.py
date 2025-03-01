import time
import csv
from datetime import date
from bs4 import BeautifulSoup
from selenium import webdriver

# obtains a list of the ASX 200
# user can then search for a company code (e.g. CBA) and obtain the 210 moving average
# prices taken at close of market
# the information is printed to the terminal and a csv file is also produced
# the user should take note of what day the program was executed

# had a small issue 24/02/2025 where VAS, CBA and BHP were loading but VGS didn't

# gets html of a website given the url as an argument
# returns html as a string
def get_html(url):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(4)
    html = driver.page_source
    driver.quit()

    return html

# takes a string, returns true if string contains numbers only, false otherwise
def numbers_only(string):
    for letter in string:
        if letter.isnumeric() or letter == '.':
            continue
        else:
            return False
        
    return True



# takes html of yahoo website and obtains the closing prices, returned as a list
# div.table-container.yf-1jecxey
def fetch_closes(html):
    locator = 'table.table.yf-1jecxey.noDl tbody td.yf-1jecxey'
    soup = BeautifulSoup(html, 'html.parser')
    item_links = soup.select(locator)
    items = [item.text for item in item_links if numbers_only(item.text)]
    result = []

    i = 0
    days = 0
    for item in items:
        if days > 210:
            break
        if i % 6 == 4:
            result.append(float(item))
            days += 1
        i += 1
    
    return result

# checks whether a search_term (already formatted) has been previously entered
# into the final array
# returns true if already searched, false otherwise
def already_searched(final, search_term):
    for entry in final:
        if search_term == entry[0]:
            return True
        
    return False

# returns true if a given company code is in the top 200, else false
def is_top200(target, top200_names):
    for name in top200_names:
        if target.strip().upper() == name.strip().upper():
            return True
        
    return False


html = get_html("https://www.marketindex.com.au/asx-listed-companies")
soup_one = BeautifulSoup(html, 'html.parser')

locator = 'div table tbody tr td.sticky-column a'
item_links = soup_one.select(locator)

top200_names = [item.text for item in item_links]
top200_names = top200_names[:200]

# create a list of the top 200's 210 day moving averages
final = []

target_comp = ''
while (target_comp := input('Enter an ASX200 company code, or enter QUIT to exit: ').strip().upper()) != None:
    if target_comp == 'QUIT':
        break
    elif already_searched(final, target_comp) == True:
        print('Already searched!\n')
        continue
    elif is_top200(target_comp, top200_names) == False:
        print('Not in the ASX 200.\n')
        continue
    
    target_site = 'https://au.finance.yahoo.com/quote/' + target_comp + '.AX/history/'
    html = get_html(target_site)
    past_prices = fetch_closes(html)
    if (len(past_prices) == 0):
        ten_month_ave = 0
    else:
        ten_month_ave = sum(past_prices) / len(past_prices)
    
    final.append((target_comp, ten_month_ave))

    
print("Ten month moving averages")
for company in final:
    name, average = company
    print(f"{name}\t{average}")

# now write everything to a csv file
with open("ten_month_averages.csv", "w") as csv_file:
    for company in final:
        name, average = company
        csv_file.write(f'{name}, {average}\n')