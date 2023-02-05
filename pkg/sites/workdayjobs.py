import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from list import NO_APPLICATION_QUESTIONS, YES_APPLICATION_QUESTIONS


def click_hidden_button(driver, btn_xpath):
    try:
        submit_button = driver.find_element(By.XPATH, btn_xpath)
        actions = ActionChains(driver=driver)
        actions.move_to_element(submit_button).click().perform()
    except BaseException:
        pass


def enter_login(driver, btn_xpath):
    form = driver.find_element(By.TAG_NAME, 'form')

    elements = form.find_elements(By.XPATH, './*')

    for element in elements:
        try:
            label = element.find_element(
                By.TAG_NAME, "label").get_attribute('innerText')
            input = element.find_element(By.TAG_NAME, 'input')

            if "Email" in label:
                input.send_keys(os.environ.get('EMAIL'))

            if "Password" in label:
                input.send_keys(os.environ.get('PASSWORD'))

        except BaseException:
            continue

    click_hidden_button(driver, btn_xpath)


def select_options(driver, attr, input_id):
    try:
        if "Fluent" in attr:

            btn_xpath = f'//button[@id="{input_id}"]'
            click_hidden_button(driver, btn_xpath)

            elements = driver.find_elements(By.TAG_NAME, 'li')
            for el in elements:
                if attr in el.get_attribute('textContent'):
                    el.click()
                    break
        else:
            element = driver.find_element(By.ID, input_id)
            element.click()

            elements = driver.find_elements(By.TAG_NAME, 'li')
            for el in elements:
                if attr.lower() in el.get_attribute('textContent').lower():
                    el.click()
                    break
    except BaseException as err:
        print(err)


def handle_multiple_input(driver, element, skills):

    def handle_multi_select(skill, options):
        for option in options:
            if skill in option.get_attribute('innerText'):
                option.click()
                return skill
        
        return ""

    for skill in skills:
        element.send_keys(skill)
        element.send_keys(Keys.RETURN)
        sleep(0.5)

        options = driver.find_elements(By.XPATH, '//*[@data-automation-id="promptOption"]')
        if len(options) > 0:
            selected = handle_multi_select(skill=skill, options=options)
            if selected == "":
                element.send_keys(Keys.CLEAR)


def handle_inputs(driver):
    elements = driver.find_elements(By.TAG_NAME, 'input')
    elements += driver.find_elements(By.TAG_NAME, 'button')
    elements += driver.find_elements(By.TAG_NAME, 'textarea')

    def input_field(element, user_data):
        try:
            if element.get_attribute('value') == "":
                element.send_keys(user_data)
        except BaseException:
            pass


    for el in elements:
        try:
            if el.get_attribute('tagName') == "INPUT" or el.get_attribute('tagName') == "TEXTAREA":
                input_id = el.get_attribute('id')
                if len(input_id) > 0:
                    label = driver.find_element(
                        By.XPATH, f'//label[@for="{input_id}"]').get_attribute('innerText')

                    if "No" in label:
                        el.click()
                    if "First Name" in label:
                        input_field(el, 'David')
                    if "Last Name" in label:
                        input_field(el, 'Alvarez')
                    if label == "Name":
                        input_field(el, 'David Alvarez')
                    if "Address Line 1" in label:
                        input_field(el, os.environ.get('ADDRESS'))
                    if "City" in label:
                        input_field(el, os.environ.get('COMPANY_LOCATION'))
                    if "Postal Code" in label:
                        input_field(el, os.environ.get('ZIP_CODE'))
                    if "Phone Number" in label:
                        input_field(el, os.environ.get('PHONE_NUMBER'))
                    if "Job Title" in label:
                        input_field(el, os.environ.get('TITLE'))
                    if "Company" in label:
                        input_field(el, 'CURRENT COMPANY')
                    if "Location" in label:
                        input_field(el, os.environ.get('COMPANY_LOCATION'))
                    if "currently working here" in label or "No, I Don't Have A Disability" in label:
                        el.click()
                    if "fluent in this language" in label or "terms and conditions" in label:
                        el.click()
                    if "Role Description" in label:
                        input_field(el, os.environ.get('JOB_DESCRIPTION'))
                    if "School or University" in label:
                        input_field(el, os.environ.get('UNIVERSITY'))
                    if "Field of Study" in label:
                        handle_multiple_input(driver, el, ['Marketing', 'Advertising'])
                    if "Skills" in label:
                        handle_multiple_input(driver, el, ['Javascript', 'Python', 'Go', 'Amazon Web Services', 'Google Cloud Platform',
                                              'Docker', 'Linux', 'Nginx', "SQL", "GraphQL", 'Postgres', 'MongoDB'])

            if el.get_attribute('tagName') == "BUTTON":
                input_id = el.get_attribute('id')
                if len(input_id) > 0 and "input" in input_id:
                    label = driver.find_element(
                        By.XPATH, f'//label[@for="{input_id}"]').get_attribute('innerText')
                    if "State" in label:
                        select_options(
                            driver=driver, input_id=input_id, attr="Florida")
                    if "Phone Device Type" in label:
                        select_options(
                            driver=driver, input_id=input_id, attr="Mobile")
                    if "Degree" in label:
                        select_options(driver=driver, input_id=input_id,
                                       attr="Associate")
                    if "Veteran" in label:
                        select_options(driver=driver, input_id=input_id,
                                       attr="No")
                    if "Gender" in label:
                        select_options(driver=driver, input_id=input_id,
                                       attr="Male")
                    if "Race" in label:
                        select_options(driver=driver, input_id=input_id,
                                       attr="Hispanic or Latino (United States of America)")
                    if "Language" in label:
                        select_options(driver=driver, input_id=input_id,
                                       attr="English")
                    if "Reading" in label or "Speaking" in label or "Assessment" in label or "Writing" in label:
                        el.send_keys(Keys.ARROW_DOWN)
                        select_options(driver=driver, input_id=input_id,
                                       attr="Fluent")
                    if any(sub_str in label for sub_str in YES_APPLICATION_QUESTIONS):
                        select_options(driver=driver, input_id=input_id,
                                       attr="Yes")
                    if any(sub_str in label for sub_str in NO_APPLICATION_QUESTIONS):
                        select_options(driver=driver, input_id=input_id,
                                       attr="No")
        except BaseException:
            continue


def get_correct_year(driver):
    try:
        year = driver.find_element(
            By.XPATH, '//*[@data-automation-id="monthPickerSpinnerLabel"]').get_attribute('innerText')
        while int(os.environ.get('JOB_START_YEAR')) < int(year):
            driver.find_element(
                By.XPATH, '//*[@aria-label="Previous Year"]').click()
            current_year = driver.find_element(
                By.XPATH, '//*[@data-automation-id="monthPickerSpinnerLabel"]').get_attribute('innerText')
            year = current_year
    except BaseException as err:
        print(err)


def click_save_and_continue(driver):
    try:
        driver.find_element(
        By.XPATH, '//button[@data-automation-id="bottom-navigation-next-button"]').click()
        sleep(3)

        error = driver.find_elements(By.XPATH, '//*[@data-automation-id="errorBanner"]')

        if len(error) > 0:
            input("Handle the error & press enter.")
    except BaseException as err:
        print(err)

def perform_action(driver, xpath, action, *args, **kwargs):
    try:
        element = driver.find_element(By.XPATH, xpath)
        if action == "click":
            element.click()

        if action == "send keys":
            keys = kwargs.get('keys')
            element.send_keys(keys)

    except BaseException:
        pass

def click_add_fields(driver):
    add_btns = driver.find_elements(By.XPATH, '//*[@data-automation-id="Add"]')
    for btn in add_btns:
        try:
            btn.click()
        except BaseException as err:
            print(err)

def handle_workdayjobs(driver, data):
    driver.get(data['url'])

    WebDriverWait(driver, timeout=10).until(
        lambda d: d.find_element(By.TAG_NAME, "html"))
    sleep(2)

    # Navigate to Create Account & Create Account
    click_hidden_button(driver, '//button[@data-automation-id="createAccountLink"]')

    # enter_login(driver, '//button[@data-automation-id="createAccountSubmitButton"]')
    input("Verify email and come back: ")

    # Return to Sign In Screen
    click_hidden_button(driver, '//button[@data-automation-id="signInLink"]')

    # Submit & Verify Email -- Then Login
    enter_login(driver, '//button[@data-automation-id="signInSubmitButton"]')
    sleep(5)

    # Apply Manually
    click_hidden_button(driver, '//*[@data-automation-id="applyManually"]')
    sleep(5)

    # Enter Fields
    handle_inputs(driver)

    # Save & Continue
    click_save_and_continue(driver)

    # Click Add Work & Education Experience
    click_add_fields(driver)

    # Click "I Currently Work Here"
    perform_action(driver, '//input[@data-automation-id="currentlyWorkHere"]', "click")

    # Click Calendar for Dates & Handle Dates
    perform_action(driver, '//*[@data-automation-id="dateIcon"]', "click")
    get_correct_year(driver)

    months = driver.find_elements(By.TAG_NAME, 'li')

    for month in months:
        if month.get_attribute('innerText') == "Nov":
            month.click()
            break

    # Upload Resume
    perform_action(driver, '//input[@data-automation-id="file-upload-input-ref"]', "send keys", keys=os.environ.get('RESUME_PATH'))

    # Add Websites
    perform_action(driver, '//input[@data-automation-id="website"]', "send keys", keys='https://github.com/davidalvarez305')

    # Add LinkedIn
    perform_action(driver, '//input[@data-automation-id="linkedinQuestion"]', "send keys", keys=os.environ.get('LINKED_URL'))

    handle_inputs(driver)

    # Save & Continue
    click_save_and_continue(driver)

    # Handle Application Questions
    handle_inputs(driver)

    # Save & Continue
    click_save_and_continue(driver)

    # Handle Voluntary Disclosures
    handle_inputs(driver)

    # Save & Continue
    click_save_and_continue(driver)

    # Handle Self-Identify
    handle_inputs(driver)

    # Select Today's Date
    perform_action(driver, '//*[@data-automation-id="dateIcon"]', "click")
    perform_action(driver, '//*[@aria-selected="true"]', "click")

    # Save & Continue
    click_save_and_continue(driver)
