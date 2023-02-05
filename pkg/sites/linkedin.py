from lib2to3.pytree import Base
import os
from random import uniform
from time import sleep
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from site_router import site_router


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
        filters = driver.find_elements(
            By.XPATH, '//*[@class="search-reusables__primary-filter"]')

        for filter in filters:
            btn = filter.find_element(By.TAG_NAME, 'button')
            if "Jobs" in btn.get_attribute('innerText'):
                btn.click()
    except BaseException:
        input("Press enter after looking up jobs: ")
        pass


def go_to_jobs_search(driver, data):
    try:
        search_input = driver.find_element(
            By.XPATH, '//input[@placeholder="Search"]')
        search_input.send_keys(data['keywords'])
        search_input.send_keys(Keys.RETURN)
        sleep(4)
        find_jobs_button(driver)
    except BaseException:
        input("Press enter after looking up jobs: ")
        pass


def handle_job(driver, data, values):
    try:
        print("Handling job...")
        job_details = driver.find_element(By.CLASS_NAME, 'jobs-details')
        buttons = job_details.find_elements(By.TAG_NAME, 'button')

        for button in buttons:
            if "Apply" in button.get_attribute('innerText'):
                button.click()

        sleep(5)

        # Switch Tab & Fill Fields
        driver.switch_to.window(driver.window_handles[1])
        data['url'] = driver.current_url

        site_router(driver=driver, data=data, values=values)

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    except BaseException:
        pass


def handle_jobs(driver, data, values):
    jobs = driver.find_elements(
        By.XPATH, '//a[@class="disabled ember-view job-card-container__link job-card-list__title"]')

    for job in jobs:
        try:
            print('Running job...')
            job.click()
            handle_job(driver=driver, data=data, values=values)
        except BaseException:
            input("Press enter to move on to next job: ")
            continue


def handle_linkedin(driver, data, values):

    # Attempt to Login
    # login(driver)
    input("Press enter after logging in: ")

    # Access Job Search
    go_to_jobs_search(driver=driver, data=data)

    sleep(5)
    current_page = 1

    while (current_page < 40):
        pages_list = driver.find_element(
            By.XPATH, '//ul[@class="artdeco-pagination__pages artdeco-pagination__pages--number"]')

        pg_buttons = pages_list.find_elements(
            By.XPATH, './/li[@class="artdeco-pagination__indicator artdeco-pagination__indicator--number ember-view"]')

        try:
            handle_jobs(driver=driver, data=data, values=values)
            for index, btn in enumerate(pg_buttons):
                if int(btn.get_attribute('data-test-pagination-page-btn')) == current_page + 1:
                    btn.click()
                    sleep(5)
        except BaseException as err:
            # Only click the tree dots if the previous index was not one, otherwise, we'll keep circling back.
            if "int() argument must be a string" in err.__str__() and int(pg_buttons[index - 1].get_attribute('data-test-pagination-page-btn')) != 1:
                btn.click()
                sleep(5)
            continue
        finally:
            current_page += 1
