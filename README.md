# "Automated Web Scrapper for Health-Center Scheduling Data"
Brief description: Notifies the user(s) via email of the vaccine slot availability in the city they enqired for.

> By: Nikunj Sharma (1994nikunj@git, 1994nikunj@gmail)

### Libraries in use:
> - bs4 - For parsing and scrapping the web data
> - selenium - For browser automation
> - smtplib, ssl, email - For mailing services used by the application

### Detailed description:
The code implements a web scrapper using the Selenium and BeautifulSoup libraries. The scrapper is designed to extract data from a specific URL (specified in the    settings module) that provides information on vaccination centers. The scrapper class Scrapper takes two parameters - state and district, both of which are used to filter the results. If the send_mail parameter is set to True, an email is sent with the extracted data as its body.

The code initializes the Chrome web driver in the init_browser method, and navigates to the target URL. The methods validate_state_selection and validate_district_selection parse the HTML content of the dropdown menus to select the specified state and district.

The start_scrapping method extracts the relevant data from the webpage, and the analyze_data method processes it into the required format. The prepare_message_body method is called to format the data into a message body, which is sent as an email if the send_mail parameter is set to True. Finally, the terminate_app method closes the Chrome web driver and terminates the application.

### Screenshots:
![alt text](https://github.com/1994nikunj/vaccine-slot-availability/blob/master/AboutMeStuff/img.png?raw=true)
