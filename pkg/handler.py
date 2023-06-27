import os
from time import sleep
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from pkg.handle_fields import find_form_fields
from pkg.list import COMMON_QUESTIONS
from pkg.sites.bamboo import handle_select_div
from pkg.sites.underdog import auto_complete

from pkg.sites.workdayjobs import click_add_fields, click_hidden_button, click_save_and_continue, enter_login, get_correct_year, handle_inputs, perform_action
from pkg.utils import click_preapplication_button, find_fields_by_label, handle_calendar_select, handle_smart_autocomplete_fields, handle_textarea

class Handler:
    def __init__(self, bot):
        self.bot = bot
    
    def handle_job(self, job):
        key = " "
        while (key == " "):
            print('KEY START OF LOOP: ', key)
            try:
                if "workdayjobs" in job['apply']:
                    self.handle_workdayjobs()
                    return
                if "bamboohr" in job['apply']:
                    click_preapplication_button(driver=self.driver)
                    self.handle_bamboo()
                    if "smartrecruiters" in job['apply']:
                        resume_upload = self.bot.driver.find_element(By.XPATH, '//input[@class="file-upload-input"]')
                        resume_upload.send_keys(self.bot.data['resume'])
                        sleep(5)
                        self.handle_smartrecruiters()
                    elif "underdog.io" in job['apply']:
                        self.handle_underdog_fields()
                    else:
                        self.handle_fields()
            except BaseException as err:
                user_input = input()
                if user_input != ' ':
                    os.abort()
                else:
                    continue
            finally:
                user_input = input("Press 1 to keep going. Press 2 to re-try. Press 3 to terminte program.")
                if user_input == "1":
                    break
                if user_input == "2":
                    continue
                if user_input == "3":
                    os.abort()

    
    def handle_workdayjobs(self):
        self.bot.driver.get(self.bot.data['apply'])

        WebDriverWait(self.bot.driver, timeout=10).until(
            lambda d: d.find_element(By.TAG_NAME, "html"))
        sleep(2)

        # Navigate to Create Account & Create Account
        click_hidden_button(self.bot.driver, '//button[@data-automation-id="createAccountLink"]')

        # enter_login(self.bot.driver, '//button[@data-automation-id="createAccountSubmitButton"]')
        input("Verify email and come back: ")

        # Return to Sign In Screen
        click_hidden_button(self.bot.driver, '//button[@data-automation-id="signInLink"]')

        # Submit & Verify Email -- Then Login
        enter_login(self.bot.driver, '//button[@data-automation-id="signInSubmitButton"]')
        sleep(5)

        # Apply Manually
        click_hidden_button(self.bot.driver, '//*[@data-automation-id="applyManually"]')
        sleep(5)

        # Enter Fields
        handle_inputs(self.bot.driver)

        # Save & Continue
        click_save_and_continue(self.bot.driver)

        # Click Add Work & Education Experience
        click_add_fields(self.bot.driver)

        # Click "I Currently Work Here"
        perform_action(self.bot.driver, '//input[@data-automation-id="currentlyWorkHere"]', "click")

        # Click Calendar for Dates & Handle Dates
        perform_action(self.bot.driver, '//*[@data-automation-id="dateIcon"]', "click")
        get_correct_year(self.bot.driver)

        months = self.bot.driver.find_elements(By.TAG_NAME, 'li')

        for month in months:
            if month.get_attribute('innerText') == "Nov":
                month.click()
                break

        # Upload Resume
        perform_action(self.bot.driver, '//input[@data-automation-id="file-upload-input-ref"]', "send keys", keys=self.bot.data['resume'])

        # Add Websites
        perform_action(self.bot.driver, '//input[@data-automation-id="website"]', "send keys", keys='https://github.com/davidalvarez305')

        # Add LinkedIn
        perform_action(self.bot.driver, '//input[@data-automation-id="linkedinQuestion"]', "send keys", keys=self.bot.data['linkedin'])

        handle_inputs(self.bot.driver)

        # Save & Continue
        click_save_and_continue(self.bot.driver)

        # Handle Application Questions
        handle_inputs(self.bot.driver)

        # Save & Continue
        click_save_and_continue(self.bot.driver)

        # Handle Voluntary Disclosures
        handle_inputs(self.bot.driver)

        # Save & Continue
        click_save_and_continue(self.bot.driver)

        # Handle Self-Identify
        handle_inputs(self.bot.driver)

        # Select Today's Date
        perform_action(self.bot.driver, '//*[@data-automation-id="dateIcon"]', "click")
        perform_action(self.bot.driver, '//*[@aria-selected="true"]', "click")

        # Save & Continue
        click_save_and_continue(self.bot.driver)
    
    def handle_smartrecruiters(self):
        sleep(1)

        try:
            # Delete Resume Fields
            field_options = self.bot.driver.find_elements(By.XPATH, '//button[@aria-label="See options"]')
            for option in field_options:
                option.click()

                # Click 'Delete Position in Dropdown & Wait for Dialogue Box to Open'
                delete_position = self.bot.driver.find_element(By.XPATH, '//button[@data-test="entry-delete"]')
                delete_position.click()
                sleep(2)

                yes_button = self.bot.driver.find_element(By.XPATH, '//mat-dialog-container/oc-yes-no/div/div/button[2]')
                yes_button.click()

            sections = self.bot.driver.find_elements(By.CLASS_NAME, 'form-section')

            for section in sections:
                section_header = section.find_element(By.TAG_NAME, 'h3').get_attribute('innerText')
                
                if "Experience" in section_header:
                    button = section.find_element(By.TAG_NAME, 'button')
                    button.click()

                    form_fields = section.find_elements(By.CLASS_NAME, 'form-control')

                    for field in form_fields:
                        label = field.find_element(By.TAG_NAME, 'label').get_attribute('innerText')

                    if "Title" in label:
                        input_element = field.find_element(By.TAG_NAME, 'input')
                        handle_smart_autocomplete_fields(input_element, self.bot.data['title'])
                    if "Company" in label:
                        input_element = field.find_element(By.TAG_NAME, 'input')
                        handle_smart_autocomplete_fields(input_element, self.bot.data['currentCompany'])
                    if "Office location" in label:
                        input_element = field.find_element(By.CLASS_NAME, 'sr-location-autocomplete')
                        handle_smart_autocomplete_fields(input_element, self.bot.data['companyLocation'])
                    if "Description" in label:
                        input_element = field.find_element(By.TAG_NAME, 'textarea')
                        handle_smart_autocomplete_fields(input_element, self.bot.data['jobDescription'])
                    if "From" in label:
                        work_here = field.find_element(By.XPATH, '//*[@data-test="experience-current"]')
                        work_here.click()
                        
                        calendar_button = field.find_element(By.XPATH, '//button[@aria-label="Open calendar"]')
                        calendar_button.click()

                        # Select Year
                        handle_calendar_select(self.bot.driver, self.bot.data['jobStartYear'])
                        # Select Month
                        handle_calendar_select(self.bot.driver, self.bot.data['jobStartMonth'])

                        # Save
                        save_button = field.find_element(By.XPATH, '//button[@data-test="experience-save"]')
                        save_button.click()

                if "Education" in section_header:
                    button = section.find_element(By.TAG_NAME, 'button')
                    button.click()

                    form_fields = section.find_elements(By.CLASS_NAME, 'form-control')

                    for field in form_fields:
                        label = field.find_element(By.TAG_NAME, 'label').get_attribute('innerText')

                        if "Institution" in label:
                            input_element = field.find_element(By.TAG_NAME, 'input')
                            handle_smart_autocomplete_fields(input_element, self.bot.data['school'])
                        if "Major" in label:
                            input_element = field.find_element(By.TAG_NAME, 'input')
                            input_element.send_keys(self.bot.data['discipline'])
                        if "Degree" in label:
                            input_element = field.find_element(By.TAG_NAME, 'input')
                            input_element.send_keys(self.bot.data['degree'])
                        if "School location" in label:
                            input_element = field.find_element(By.CLASS_NAME, 'sr-location-autocomplete')
                            handle_smart_autocomplete_fields(input_element, self.bot.data['schoolLocation'])
                        if "Description" in label:
                            input_element = field.find_element(By.TAG_NAME, 'textarea')
                            handle_smart_autocomplete_fields(input_element, self.bot.data['degreeDescription'])
                        if "From" in label:
                            work_here = field.find_element(By.XPATH, '//*[@data-test="education-current"]')
                            work_here.click()
                            
                            calendar_button = field.find_element(By.XPATH, '//button[@aria-label="Open calendar"]')
                            calendar_button.click()

                            # Select Year
                            handle_calendar_select(self.bot.driver, self.bot.data['universityStartDate'])
                            
                            # Select Month
                            handle_calendar_select(self.bot.driver, self.bot.data['universityEndDate'])

                            # Save
                            save_button = field.find_element(By.XPATH, '//button[@data-test="education-save"]')
                            save_button.click()
        except BaseException as err:
            print(err)
            pass
    
    def handle_bamboo(self):
        try:
            elements = self.bot.driver.find_elements(By.CLASS_NAME, "CandidateForm__row")

            for element in elements:
                field_name = element.find_element(By.TAG_NAME, "label").get_attribute('innerText')

                # Handle Radiobuttons
                if "Veteran" in field_name:
                    btns = self.bot.driver.find_elements(By.XPATH, '//*[@type="radio"]')
                    for btn in btns:
                        label = btn.find_element(By.XPATH, '../label').get_attribute('innerText')
                        if self.bot.data['veteranStatus'].lower() in label.lower():
                            btn.click()

                # Handle Selects
                if "Gender" in field_name:
                    element.click()
                    handle_select_div(self.bot.driver, self.bot.data['gender'])
                elif "Disability" in field_name:
                    element.click()
                    handle_select_div(self.bot.driver, self.bot.data['disabilityStatus'])
                elif "Ethnicity" in field_name:
                    element.click()
                    handle_select_div(self.bot.driver, self.bot.data['race'])

                # Handle Inputs
                else:
                    for question in COMMON_QUESTIONS:
                        if question['question'].lower() in field_name.lower():
                            field = question['data']
                            handle_textarea(element, self.bot.data[f"{field}"])
        except BaseException as err:
            print(err)
            pass

    def handle_underdog_fields(self):
        try:
            dropdowns = self.bot.driver.find_elements(By.CLASS_NAME, "div-block-37")
        
            for element in dropdowns:
                element.click()

                options = self.bot.driver.find_elements(
                        By.TAG_NAME, "option")

                select_fields = self.bot.driver.find_elements(By.TAG_NAME, "select")

                def select_option(selection):
                    options = self.bot.driver.find_elements(By.TAG_NAME, "option")
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

                hidden_inputs = self.bot.driver.find_elements(By.CLASS_NAME, "autocomplete__input")

                for input in hidden_inputs:
                    input_name = input.find_element(By.XPATH, ".//ancestor::label").get_attribute('textContent')
                    try:
                        if "Current location" in input_name:
                            input.send_keys("Hialeah, FL, USA")
                            input.click()
                            sleep(1.5)
                            auto_complete(self.bot.driver, "li")
                        if "Location preference" in input_name:
                            input.send_keys("Remote")
                            input.click()
                            auto_complete(self.bot.driver, "li")
                        if "Skills" in input_name:
                            input.send_keys("Python, Javascript, SQL, Go, Docker, AWS, Linux, Google Cloud Platform")
                            input.click()
                            auto_complete(self.bot.driver, "li")
                        if "Job type preference(s)" in input_name:
                            input.send_keys("I want a full")
                            input.click()
                            auto_complete(self.bot.driver, "li")
                    except BaseException as err:
                        print(err)

                for element in options:
                    if element.get_attribute('value') == "":
                        field_name = element.get_attribute('name')
                        if "first" in field_name.lower():
                            element.send_keys(self.bot.data['firstName'])
                        if "resume" in field_name.lower():
                            element.send_keys(self.bot.data['resume'])
                        if "last" in field_name.lower():
                            element.send_keys(self.bot.data['lastName'])
                        if "email" in field_name.lower():
                            element.send_keys(self.bot.data['email'])
                        if "website" in field_name.lower():
                            element.send_keys(self.bot.data['linkedIn'])
                        if "github" in field_name.lower() or "portfolio" in field_name.lower():
                            element.send_keys(self.bot.data['portfolio'])
        except BaseException as err:
                print(err)
                pass
        
    def handle_fields(self):
        # Find Fields by Form Label
        fields = find_fields_by_label(self.bot.driver)

        # Append Form Fields
        form_fields = find_form_fields(self.bot.driver, self.bot.values)
        fields += form_fields

        for field in fields:
                # Handle Resume Upload
                if field['tagName'] == 'BUTTON':
                    resume_fields = [
                        field['label'],
                        field['element'].get_attribute('textContent'),
                        field['element'].get_attribute('innerText'),
                        field['element'].get_attribute('innerHTML'),
                        field['element'].get_attribute('id'),
                        field['element'].get_attribute('name'),
                        field['element'].get_attribute('class')
                    ]
                    if "resume" in resume_fields:
                            if field['element'].get_attribute('value') == "":
                                field['element'].send_keys(self.bot.data['resume'])

                # Handle Select Buttons
                elif field['tagName'] == 'SELECT':
                    for question in self.bot.values:
                        if any(substr in field['label'].lower() for substr in question['question']):
                            if self.bot.data[f"{question['data']}"].lower() in field['element'].get_attribute('value').lower():
                                field['element'].click()
                                sleep(1)

                            options = field['element'].find_elements(By.TAG_NAME, 'option')
                            for option in options:
                                if self.bot.data[f"{question['data']}"].lower() in option.get_attribute('textContent').lower():
                                    option.click()

                # Handle Checkboxes & Radio Buttons
                elif field['tagName'] == 'INPUT' and field['element'].get_attribute('type') in ['checkbox', 'radio']:
                    for question in self.bot.values:
                        if any(substr in field['label'].lower() for substr in question['question']):
                            if self.bot.data[f"{question['data']}"].lower() in field['element'].get_attribute('value').lower():
                                field['element'].click()

                # Handle Normal Inputs
                else:
                    for question in self.bot.values:
                        if any(substr in field['label'].lower() for substr in question['question']):
                            if field['element'].get_attribute('value') == "":
                                field['element'].send_keys(self.bot.data[f"{question['data']}"])