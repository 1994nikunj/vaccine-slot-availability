import time
from datetime import datetime, timedelta

import bs4.element
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome, ChromeOptions

from tabularize import Tabularize

slot_available = False
date_time_today = datetime.today()
cols = ['Center Name', 'Address']

# Setup
URL = 'https://www.cowin.gov.in/home'
DRIVER = './Drivers/chromedriver.exe'
options = ChromeOptions()

# Starting Browser
browser = Chrome(executable_path=DRIVER, options=options)
browser.get(url=URL)
print('-- Page Title:', browser.title)

# Make selection on Switch element
browser.find_element_by_class_name(name='status-switch').click()

# Making "State" selection
time.sleep(0.3)
browser.find_element_by_class_name(name='mat-form-field-infix').click()
time.sleep(0.3)
browser.find_element_by_xpath(xpath='//*[@id="mat-option-20"]/span').click()

# Making "District" selection
time.sleep(0.3)
browser.find_element_by_class_name(name='mat-select-placeholder').click()
time.sleep(0.3)
browser.find_element_by_xpath(xpath='//*[@id="mat-option-58"]/span').click()

# Hit Search Button
time.sleep(0.3)
browser.find_element_by_class_name(name='pin-search-btn').click()

time.sleep(0.6)
# Center Name
inner_html = browser.find_element_by_xpath(xpath="//div[@class='center-box']").get_attribute('innerHTML')
time.sleep(1)

# Closing Browser
browser.quit()

html_soup = BeautifulSoup(inner_html, 'html.parser')

final_data = []
data_for_table = []
rows = html_soup.findAll('div', attrs={'class': 'row ng-star-inserted'})
for row in rows:
    _slot_details = {}
    _for_table = []
    slot_available_wrap = row.find('ul', attrs={'class': 'slot-available-wrap'})

    _center_name = row.find('h5', attrs={'class': 'center-name-title'}).text.strip()
    _center_address = row.find('p', attrs={'class': 'center-name-text'}).text.strip()
    _temp = {
        'center_name': _center_name,
        'center_address': _center_address
    }
    _for_table.append(_center_name)
    _for_table.append(_center_address)

    for idx, x in enumerate(slot_available_wrap):
        if not isinstance(x, bs4.element.Comment):
            d = (date_time_today + timedelta(days=idx)).strftime("%d-%b-%Y")
            if cols[-1] != (date_time_today + timedelta(days=6)).strftime("%d-%b-%Y"):
                cols.append(d)
            _slot_val = x.text.strip()
            if 'Booked' not in _slot_val and _slot_val != 'NA':
                slot_available = True
            _slot_details[d] = _slot_val
            _for_table.append(_slot_val)

    _temp['slot_details'] = _slot_details
    final_data.append(_temp)
    data_for_table.append(_for_table)

# import json
# print(json.dumps(final_data, indent=4))

# print('Table Data:', data_for_table)
# print('Table Columns:', cols)
# TmlrdW5qU2hhcm1hMDQ=
print_table = False
if print_table:
    table = Tabularize(column_names=cols, right_padding=2, title="Title: Sample Table")
    for entry in data_for_table:
        table.add_row(entry)
    table.generate_table()

quit()
