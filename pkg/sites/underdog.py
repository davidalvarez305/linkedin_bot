import os
from time import sleep
from selenium.webdriver.common.by import By

from utils import complete_prompt

def auto_complete(driver, tag):
    hidden_input = driver.find_element(By.TAG_NAME, tag)
    hidden_input.click()

def handle_underdog(options, data, driver):
    select_fields = driver.find_elements(By.TAG_NAME, "select")

    def select_option(selection):
        options = driver.find_elements(By.TAG_NAME, "option")
        for option in options:
            option_name = option.get_attribute('textContent')
            if option_name == selection:
                option.click()

    for select_field in select_fields:
        select_field.click()
        field_name = select_field.get_attribute('name')
        if "location" in field_name.lower():
            select_option("Remote")
        if "search_status" in field_name.lower():
            select_option("Actively interviewing")
        if "technical" in field_name.lower():
            select_option("Technical")
        if "experience_level" in field_name.lower():
            select_option("1-2 years")
        if "visa_toggle" in field_name.lower():
            select_option("I am a U.S. citizen or a lawful permanent resident")

    hidden_inputs = driver.find_elements(By.CLASS_NAME, "autocomplete__input")

    for input in hidden_inputs:
        input_name = input.find_element(By.XPATH, ".//ancestor::label").get_attribute('textContent')
        try:
            if "Current location" in input_name:
                input.send_keys("Hialeah, FL, USA")
                input.click()
                sleep(1.5)
                auto_complete(driver, "li")
            if "Location preference" in input_name:
                input.send_keys("Remote")
                input.click()
                auto_complete(driver, "li")
            if "Skills" in input_name:
                input.send_keys("Python, Javascript, SQL, Go, Docker, AWS, Linux, Google Cloud Platform")
                input.click()
                auto_complete(driver, "li")
            if "Job type preference(s)" in input_name:
                input.send_keys("I want a full")
                input.click()
                auto_complete(driver, "li")
        except BaseException as err:
            print(err)

    for element in options:
        if element.get_attribute('value') == "":
            field_name = element.get_attribute('name')
            if "first" in field_name.lower():
                element.send_keys(data['user']['firstName'])
            if "resume" in field_name.lower():
                element.send_keys(os.environ.get('RESUME_PATH'))
            if "last" in field_name.lower():
                element.send_keys(data['user']['lastName'])
            if "email" in field_name.lower():
                element.send_keys(data['user']['email'])
            if "website" in field_name.lower():
                element.send_keys(data['user']['linkedIn'])
            if "github" in field_name.lower() or "portfolio" in field_name.lower():
                element.send_keys(data['user']['portfolio'])

def handle_underdog_fields(driver, data, values):
    try:
        dropdowns = driver.find_elements(By.CLASS_NAME, "div-block-37")
    
        for element in dropdowns:
            element.click()

            options = driver.find_elements(
                    By.TAG_NAME, "option")

            handle_underdog(options, data, driver)
    except BaseException as err:
        print(err)
        pass
    
def underdog(driver, data, values):
    to_continue = True
    while (to_continue):
        try:
            handle_underdog_fields(driver, data, values)
            to_continue = complete_prompt()
        except BaseException:
            to_continue = complete_prompt()
            continue