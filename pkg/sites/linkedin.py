from lib2to3.pytree import Base
import os
from random import uniform
from time import sleep
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebElement, WebDriver

def login(driver):
    # Get Input Fields
    username_input = driver.find_element(By.ID, "session_key")
    password_input = driver.find_element(By.ID, "session_password")

    # Enter Input
    simulate_typing(username_input, os.environ.get('EMAIL'))
    username_input.send_keys(Keys.TAB)
    sleep(1)
    simulate_typing(password_input, os.environ.get('LINKEDIN_PASSWORD'))
    sleep(1)
    password_input.send_keys(Keys.RETURN)

def simulate_typing(element, txt):
    for letter in txt:
        sleep(uniform(0.0250, 0.25))
        element.send_keys(letter)

def find_jobs_button(driver):
    try:
        filters = driver.find_elements(By.XPATH, '//*[@class="search-reusables__primary-filter"]')

        for filter in filters:
            btn = filter.find_element(By.TAG_NAME, 'button')
            if "Jobs" in btn.get_attribute('innerText'):
                btn.click()
    except BaseException:
        input("Press enter after looking up jobs: ")
        pass

def go_to_jobs_search(driver, keywords):
    try:
        search_input = driver.find_element(
            By.XPATH, '//input[@placeholder="Search"]')
        search_input.send_keys(keywords)
        search_input.send_keys(Keys.RETURN)
        sleep(4)
        find_jobs_button(driver)
    except BaseException:
        input("Press enter after looking up jobs: ")
        pass

def extract_job_data(web_element: WebElement, driver: WebDriver):
    # Click to open right-side card
    web_element.click()
    sleep(1)

    cards = [
        {
            'card': 'company_name',
            'by': By.XPATH,
            'search_string': '//a[@class="ember-view t-black t-normal"]',
        },
        {
            'card': 'job_title',
            'by': By.XPATH,
            'search_string': '//h2[@class="t-24 t-bold jobs-unified-top-card__job-title"]',
        },
        {
            'card': 'salary',
            'by': By.XPATH,
            'search_string': '//a[@href="#SALARY"]',
        },
        {
            'card': 'location',
            'by': By.XPATH,
            'search_string': '//span[@class="jobs-unified-top-card__workplace-type"]',
        },
        {
            'card': 'appply',
            'by': By.XPATH,
            'search_string': '//button[@class="jobs-apply-button artdeco-button artdeco-button--icon-right artdeco-button--3 artdeco-button--primary ember-view"]',
        },
    ]

    job_data = {}

    for card in cards:
        try:
            if card['card'] == 'apply':
                apply_button = web_element.find_element(card['by'], card['search_string'])
                apply_button.click()
                sleep(5)

                # Get link from newly open window, then close it.
                driver.switch_to.window(driver.window_handles[1])
                job_apply_url = driver.current_url
                driver.close()
                driver.switch_to.window(driver.window_handles[0])

                job_data[card['card']] = job_apply_url.strip()
            else:
                el = web_element.find_element(card['by'], card['search_string'])
                job_data[card['card']] = el.get_attribute('textContent').strip()
        except BaseException as err:
            print("FAILED CRAWLING ELEMENT: ", err)
            continue

    print('data: ', job_data)

    return job_data