import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from helpers.sheets import get_values
from sites.linkedin import handle_linkedin
from site_router import site_router

def execute(data):

    # Get Spreadsheet Values
    rows = get_values(os.environ.get('SHEETS_ID'), f"{os.environ.get('TAB_NAME')}!A2:E")
    values = []
    for row in rows:
        values.append({ "data": row[0], "question": row[1:] })

    # Initialize Driver
    options = Options()
    options.add_argument(f"user-agent={os.environ.get('USER_AGENT')}")
    driver = webdriver.Firefox()
    driver.get(data['url'])

    if "linkedin" in data['url']:
        handle_linkedin(driver=driver, data=data, values=values)
    else:
        # Route Crawling Depending on URL
        site_router(driver=driver, data=data, values=values)
