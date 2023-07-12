from lib2to3.pytree import Base
import os
from random import uniform
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebElement, WebDriver

def extract_job_data(web_element: WebElement, driver: WebDriver):
    # Click to open right-side card
    web_element.click()
    sleep(1)

    cards = [
        {
            'card': 'company_name',
            'by': By.XPATH,
            'search_string': '//a[@data-tracking-control-name="public_jobs_topcard-org-name"]',
        },
        {
            'card': 'job_title',
            'by': By.XPATH,
            'search_string': '//h2[@class="top-card-layout__title font-sans text-lg papabear:text-xl font-bold leading-open text-color-text mb-0 topcard__title"]',
        },
        {
            'card': 'salary',
            'by': By.XPATH,
            'search_string': '//a[@href="#SALARY"]',
        },
        {
            'card': 'location',
            'by': By.XPATH,
            'search_string': '//span[@class="topcard__flavor topcard__flavor--bullet"]',
        },
        {
            'card': 'apply',
            'by': By.XPATH,
            'search_string': '//button[@class="sign-up-modal__outlet top-card-layout__cta mt-2 ml-1.5 h-auto babybear:flex-auto top-card-layout__cta--primary btn-md btn-primary"]',
        },
    ]

    job_data = {}

    for card in cards:
        try:
            if card['card'] == 'apply':
                apply_button = web_element.find_element(card['by'], card['search_string'])
                apply_button.click()
                sleep(1)

                # Deal with 'sign up' popup
                x_button_popup = driver.find_element(By.XPATH, '//button[@data-tracking-control-name="public_jobs_apply-link-offsite_sign-up-modal_modal_dismiss"]')
                x_button_popup.click()
                sleep(2)

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
        finally:
            # Try to get easy apply information
            if card['card'] == 'apply' and job_data.get(card['card']) == None:
                easy_apply_button = web_element.find_element(card['by'], '//div[@class="display-flex justify-space-between"]')
                link_el = easy_apply_button.find_element(By.TAG_NAME, 'a')

                job_data[card['card']] = link_el.get_attribute('href').strip()
            if job_data.get(card['card']) == None:
                job_data[card['card']] = ""

    return job_data