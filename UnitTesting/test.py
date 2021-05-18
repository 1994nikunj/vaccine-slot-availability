slot_val = '49  COVISHIELD Age 45+ 25  COVISHIELD Age 18+'
slot_val = '49  COVISHIELD Age 45+ '

v_arr = slot_val.strip().split()
if v_arr.count('Age') == 1:
    _a = '{}(Quant: {}, Age: {})'.format(v_arr[1], v_arr[0], str(v_arr[3]))
    vac_arr = _a
else:
    tmp_vac = []
    for x in range(v_arr.count('Age')):
        k = v_arr[x*4: x*4 + 4]
        _a = '{}(Quant: {}, Age: {})'.format(k[1], k[0], str(k[3]))
        tmp_vac.append(_a)
    vac_arr = ', '.join(tmp_vac)

print(vac_arr)

"""
import time

from bs4 import BeautifulSoup
from selenium.webdriver import Chrome


URL = 'https://www.cowin.gov.in/home'
DRIVER = './Drivers/chromedriver.exe'
browser = Chrome(executable_path=DRIVER)
browser.get(url=URL)
browser.find_element_by_class_name(name='status-switch').click()

# Making "State" selection
time.sleep(0.3)
browser.find_element_by_class_name(name='mat-form-field-infix').click()
time.sleep(0.3)
inner_html = browser.find_element_by_xpath(xpath='//div[@id="mat-select-0-panel"]').get_attribute('innerHTML')
time.sleep(1)

browser.refresh()
# Closing Browser
browser.quit()

html_soup = BeautifulSoup(inner_html, 'html.parser')

rows = html_soup.findAll('mat-option', attrs={'class': 'mat-option mat-focus-indicator ng-tns-c64-1 ng-star-inserted'})
for row in rows:
    elem_id = row.get('id')
    elem_val = row.find('span', attrs={'class': 'mat-option-text'}).text.strip()
    print(elem_id, elem_val)
"""
