__Author__ = 'NIKUNJ SHARMA'

import time
from datetime import datetime, timedelta

import bs4.element
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Chrome

import settings as _set


class Scrapper(object):
    def __init__(self,
                 state: str,
                 district: str,
                 send_mail=False):

        self.browser = None
        self.entry_mode = True
        self.district = district or 'Indore'
        self.state = state or 'Madhya Pradesh'

        self.mail_body = []

        self.state_id = None
        self.district_id = None

        self.state_xpath = ''
        self.district_xpath = ''

        self.inner_html = None
        self.curr_date = datetime.today()
        self.slot_date = None
        self.cols = ['Center Name', 'Address']
        self.final_data = []

        self.init_browser()
        self.start_scrapping()
        self.exit_chromedriver()
        self.analyze_data()

        # import json
        # _printable_data = json.dumps(self.final_data, indent=4)
        # print(_printable_data)

        if send_mail:
            self.prepare_message_body()
            if self.mail_body:
                self.send_mail()

        self.terminate_app()

    def init_browser(self):
        try:
            print('## Initializing Application')
            chrome_options = webdriver.ChromeOptions()
            self.browser = Chrome(executable_path=_set.DRIVER_PATH, options=chrome_options)
            self.browser.get(url=_set.URL)
        except Exception as e:
            print('Failed to start Chrome-driver, aborting operation, error: {}'.format(e))
            self.terminate_app()
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
            print('** State| ID: {}, Name: {}'.format(self.state_id, self.state))
        else:
            print('Invalid State value provided! value: {}'.format(self.state))
            self.exit_chromedriver()
            self.terminate_app()

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
            print('** District| ID: {}, Name: {}'.format(self.district_id, self.district))
        else:
            print('Invalid District value provided! value: {}'.format(self.state))
            self.exit_chromedriver()
            self.terminate_app()

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
    def scrap_data(vaccine_data=None) -> list:
        v_arr = [_x.strip().split() for _x in vaccine_data.split('+')][:-1]
        tmp_vac = []
        for _data in v_arr:
            if 'book' not in _data[0].lower():
                _get = {
                    'vaccine_name': _data[1],
                    'available_quantity': _data[0],
                    'age_range': str(_data[5])
                }
                tmp_vac.append(_get)

        if tmp_vac:
            return tmp_vac
        else:
            return []

    def analyze_data(self):
        html_soup = BeautifulSoup(self.inner_html, 'html.parser')

        rows = html_soup.findAll('div', attrs={'class': 'row ng-star-inserted'})
        for row in rows:
            _slot_details = {}
            slot_available_wrap = row.find('ul', attrs={'class': 'slot-available-wrap'})

            for idx, x in enumerate(slot_available_wrap):
                if not isinstance(x, bs4.element.Comment):
                    self.slot_date = (self.curr_date + timedelta(days=idx)).strftime("%d-%b-%Y")
                    if self.cols[-1] != (self.curr_date + timedelta(days=6)).strftime("%d-%b-%Y"):
                        self.cols.append(self.slot_date)

                    # Scrap Vaccine details
                    raw = x.text.replace('  ', ' ')
                    vaccine_data = self.scrap_data(vaccine_data=raw)
                    if vaccine_data:
                        _slot_details[self.slot_date] = vaccine_data

            _temp_dict = {
                'center_name': row.find('h5', attrs={'class': 'center-name-title'}).text.strip(),
                'center_address': row.find('p', attrs={'class': 'center-name-text'}).text.strip(),
                'slot_details': _slot_details
            }

            if _slot_details:
                self.final_data.append(_temp_dict)

    def prepare_message_body(self):
        _time = self.curr_date.strftime("%d-%b-%Y %I:%M %p")
        start_ = """<html>
                <body>
                <p>**Following vaccine centers have been found with availability in
                    <strong style='color: green'>%s, %s </strong>
                    <em style='color: blue'>(%s)</em>
                </p>
                    <table border="2" cellspacing="1" cellpadding="5" style="text-align:left;padding:0;"> 
                        <tr> 
                            <th>No.</th> 
                            <th>Center Name</th> 
                            <th>Center Address</th> 
                            <th>Slot Date</th> 
                            <th>Vaccine</th> 
                            <th>Quantity</th> 
                            <th>Age Range</th> 
                        </tr>""" % (self.district, self.state, _time)
        tel = """<tr> 
                    <td style='text-align: center'> %d </td>                <!-- Serial No. -->
                    <td> %s </td>                                           <!-- Center Name -->
                    <td> %s </td>                                           <!-- Center Address -->
                    <td> %s </td>                                           <!-- Slot Date -->
                    <td style='text-align: center'> %s </td>                <!-- Vaccine -->
                    <td style='color: red;text-align: center'> %s </td>     <!-- Quantity -->
                    <td style='text-align: center'> %s+ </td>               <!-- Age Range -->
                </tr>"""
        end_ = """</table>
                <br>
                Thanks,<br>
                Nikunj :)
                <br>
                </body>
                </html>"""

        self.mail_body.append(start_)
        idx = 1
        for slot_data in self.final_data:
            center_name = slot_data['center_name']
            center_address = slot_data['center_address']
            for _date, _arr_1 in slot_data['slot_details'].items():
                for _vac in _arr_1:
                    k = tel % (idx, center_name, center_address, _date, _vac['vaccine_name'],
                               _vac['available_quantity'], _vac['age_range'])
                    self.mail_body.append(k)
                    idx += 1

        self.mail_body.append(end_)
        # print('\n'.join(self.mail_body))

    def send_mail(self):
        import smtplib
        import ssl
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText

        from_add = _set.MAIL_FROM
        pwd = _set.MAIL_PASS
        to_add = _set.MAIL_TO

        msg = MIMEMultipart()
        msg['From'] = from_add
        msg['To'] = ', '.join(to_add)

        _time = self.curr_date.strftime("%d-%b-%Y %I:%M %p")
        msg['Subject'] = _set.MAIL_SUBJECT.format(self.district, self.state, _time)

        body = '\n'.join(self.mail_body)
        msg.attach(MIMEText(body, 'html'))

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(host="smtp.gmail.com", port=465, context=context) as server:
            server.login(user=from_add, password=pwd)
            server.sendmail(from_addr=from_add, to_addrs=to_add, msg=msg.as_string())

        print('Mail Sent to: {}'.format(to_add))

    def exit_chromedriver(self):
        self.browser.quit()

    @staticmethod
    def terminate_app():
        print('## Terminating Application')
        quit()


if __name__ == '__main__':
    Scrapper(state=_set.STATE,
             district=_set.DISTRICT,
             send_mail=_set.SEND_EMAIL)
