__Author__ = ' NIKUNJ SHARMA '
__Date__ = '   18th May 2021 '

import time
from datetime import datetime, timedelta

import bs4.element
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Chrome


class Scrapper(object):
    URL = 'https://www.cowin.gov.in/home'
    DRIVER_PATH = './Drivers/chromedriver.exe'

    def __init__(self,
                 state: str,
                 district: str,
                 print_all_data=False,
                 send_mail=False):

        self.browser = None
        self.entry_mode = True
        self.slot_found = []
        self.district = district or 'Indore'
        self.state = state or 'Madhya Pradesh'

        self.final_data = []
        self.data_for_table = []
        self.mail_body = ''

        self.state_id = None
        self.district_id = None

        self.state_xpath = ''
        self.district_xpath = ''

        self.inner_html = None
        self.curr_date = datetime.today()
        self.cols = ['Center Name', 'Address']

        # Start application
        self.init_browser()
        self.start_scrapping()
        self.exit_chromedriver()
        self.analyze_data()

        if print_all_data:
            self.print_all_scrap()

        self.final_verdict()
        if send_mail and self.mail_body:
            self.send_mail()

        # End application
        self.end_app()

    def init_browser(self):
        try:
            print('## Initializing Application')
            chrome_options = webdriver.ChromeOptions()
            self.browser = Chrome(executable_path=Scrapper.DRIVER_PATH, options=chrome_options)
            self.browser.get(url=Scrapper.URL)
        except Exception as e:
            print('Failed to start Chrome-driver, aborting operation, error: {}'.format(e))
            self.end_app()
        time.sleep(1)

    def validate_state_selection(self):
        self.browser.find_element_by_class_name(name='mat-form-field-infix').click()
        _html = self.browser.find_element_by_xpath(xpath='//div[@id="mat-select-0-panel"]').get_attribute('innerHTML')
        time.sleep(1)

        _soup_states = BeautifulSoup(_html, 'html.parser')
        rows = _soup_states.findAll('mat-option',
                                    attrs={'class': 'mat-option mat-focus-indicator ng-tns-c64-1 ng-star-inserted'})
        for row in rows:
            if self.state == row.find('span', attrs={'class': 'mat-option-text'}).text.strip():
                self.state_id = row.get('id')
        if self.state_id:
            self.state_xpath = '' '//*[@id="{}"]/span'.format(self.state_id)
            self.browser.find_element_by_xpath(xpath=self.state_xpath).click()
            # print('** State| ID: {}, Name: {}'.format(self.state_id, self.state))
        else:
            print('Invalid State value provided! value: {}'.format(self.state))
            self.exit_chromedriver()
            self.end_app()

    def validate_district_selection(self):
        self.browser.find_element_by_class_name(name='mat-select-placeholder').click()
        _html = self.browser.find_element_by_xpath(xpath='//div[@id="mat-select-2-panel"]').get_attribute('innerHTML')
        time.sleep(1)

        html_soup = BeautifulSoup(_html, 'html.parser')

        rows = html_soup.findAll('mat-option',
                                 attrs={'class': 'mat-option mat-focus-indicator ng-tns-c64-3 ng-star-inserted'})
        for row in rows:
            if self.district == row.find('span', attrs={'class': 'mat-option-text'}).text.strip():
                self.district_id = row.get('id')

        if self.district_id:
            self.district_xpath = '//*[@id="{}"]/span'.format(self.district_id)
            self.browser.find_element_by_xpath(xpath=self.district_xpath).click()
            # print('** District| ID: {}, Name: {}'.format(self.district_id, self.district))
        else:
            print('Invalid District value provided! value: {}'.format(self.state))
            self.exit_chromedriver()
            self.end_app()

    def start_scrapping(self):
        # Make selection on Switch element
        self.browser.find_element_by_class_name(name='status-switch').click()

        if self.entry_mode:
            time.sleep(0.5)
            self.validate_state_selection()
            time.sleep(0.5)
            self.validate_district_selection()
            self.entry_mode = False
        else:
            # Making "State" selection
            time.sleep(0.5)
            self.browser.find_element_by_class_name(name='mat-form-field-infix').click()
            self.browser.find_element_by_xpath(xpath=self.state_xpath).click()

            # Making "District" selection
            time.sleep(0.5)
            self.browser.find_element_by_class_name(name='mat-select-placeholder').click()
            self.browser.find_element_by_xpath(xpath=self.district_xpath).click()

        # Hit Search Button
        time.sleep(0.3)
        self.browser.find_element_by_class_name(name='pin-search-btn').click()

        # Vaccine Center Name list
        time.sleep(0.6)
        _temp_elem = self.browser.find_element_by_xpath(xpath="//div[@class='center-box']")

        self.inner_html = _temp_elem.get_attribute('innerHTML')
        time.sleep(1)

    @staticmethod
    def scrap_data(_val) -> str:
        v_arr = _val.strip().split()
        if v_arr.count('Age') == 1:
            _a = '{}(Quant: {}, Age: {})'.format(v_arr[1], v_arr[0], str(v_arr[3]))
            vac_arr = _a
        else:
            tmp_vac = []
            for x in range(v_arr.count('Age')):
                k = v_arr[x * 4: x * 4 + 4]
                _a = '{}(Quant: {}, Age: {})'.format(k[1], k[0], str(k[3]))
                tmp_vac.append(_a)
            vac_arr = ', '.join(tmp_vac)
        return vac_arr

    def analyze_data(self):
        html_soup = BeautifulSoup(self.inner_html, 'html.parser')

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
                    slot_date = (self.curr_date + timedelta(days=idx)).strftime("%d-%b-%Y")
                    if self.cols[-1] != (self.curr_date + timedelta(days=6)).strftime("%d-%b-%Y"):
                        self.cols.append(slot_date)
                    _slot_val = x.text.strip()
                    if 'Booked' not in _slot_val and _slot_val != 'NA':
                        vacc_val = self.scrap_data(_slot_val)
                        self.slot_found.append([_center_name, _center_address, slot_date, vacc_val])
                    _slot_details[slot_date] = _slot_val
                    _for_table.append(_slot_val)

            _temp['slot_details'] = _slot_details
            self.final_data.append(_temp)
            self.data_for_table.append(_for_table)

    def final_verdict(self):
        from tabularize import Tabularize

        _col = ['Center Name', 'Center Address', 'Slot Date', 'Vaccine Availability Details']
        _time = self.curr_date.strftime("%d-%b-%Y %I:%M %p")
        _title = 'Realtime Vaccine data: {}, {} >> {}'.format(self.state, self.district, _time)
        table = Tabularize(column_names=_col, right_padding=2, title=_title)
        if self.slot_found:
            for slot in self.slot_found:
                table.add_row(slot)
            self.mail_body = table.generate_table(_return=True)

    def print_all_scrap(self):
        from tabularize import Tabularize

        _title = 'Vaccine Availability Date: %s, %s' % (self.state, self.district)
        table = Tabularize(column_names=self.cols, right_padding=2, title=_title)
        for entry in self.data_for_table:
            table.add_row(entry)
        table.generate_table()

    def exit_chromedriver(self):
        self.browser.quit()

    def send_mail(self):
        import smtplib
        import ssl
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        import base64

        from_add = "tranecanz@gmail.com"
        pwd = b'TmlrdW5qU2hhcm1hMDQ='
        to_add = ["1994nikunj@gmail.com"]

        msg = MIMEMultipart()
        msg['From'] = from_add
        msg['To'] = ', '.join(to_add)

        _time = self.curr_date.strftime("%d-%b-%Y %I:%M %p")
        msg['Subject'] = "Vaccine Slot Found for {}-{}, DateTime: {}".format(self.district, self.state, _time)

        body = self.mail_body
        msg.attach(MIMEText(body, 'plain'))

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(host="smtp.gmail.com", port=465, context=context) as server:
            server.login(user=from_add, password=base64.b64decode(pwd).decode())
            server.sendmail(from_addr=from_add, to_addrs=to_add, msg=msg.as_string())

        print('Mail Sent to: {}'.format(to_add))

    @staticmethod
    def end_app():
        print('## Terminating Application')
        quit()


if __name__ == '__main__':
    Scrapper(state='Maharashtra',
             district='Mumbai',
             print_all_data=False,
             send_mail=True)
