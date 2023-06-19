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
    data = {}

    # Click to open right-side card
    web_element.click()
    sleep(1)

    # Company Name
    company_name_card = web_element.find_element(By.CSS_SELECTOR, 'a.ember-view.t-black.t-normal')

    # Title
    job_title = web_element.find_element(By.CSS_SELECTOR, 'h2.t-24.t-bold.jobs-unified-top-card__job-title')

    # Link
    apply_button = web_element.find_element(By.CSS_SELECTOR, 'button.jobs-apply-button.artdeco-button.artdeco-button--icon-right.artdeco-button--3.artdeco-button--primary.ember-view')
    apply_button.click()
    sleep(5)

    # Get link from newly open window, then close it.
    driver.switch_to.window(driver.window_handles[1])
    job_apply_url = driver.current_url
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

    # Salary
    salary_card = web_element.find_element(By.CLASS_NAME, 'app-aware-link ')

    # Location
    location_card = web_element.find_element(By.CSS_SELECTOR, 'span.jobs-unified-top-card__workplace-type')

    data['title'] = job_title.get_attribute('textContent')
    data['link'] = job_apply_url
    data['salary'] = salary_card.get_attribute('textContent')
    data['company'] = company_name_card.get_attribute('textContent')
    data['location'] = location_card.get_attribute('textContent')

    print('data: ', data)

    return data