import os
from time import sleep
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from pkg.list import COMMON_QUESTIONS
from pkg.sites.greenhouse import handle_greenhouse_autocomplete, handle_hidden_field
from pkg.sites.lever import find_lever_elements, handle_lever_fields
from pkg.sites.underdog import auto_complete
from pathlib import Path

from pkg.sites.workdayjobs import click_add_fields, click_hidden_button, click_save_and_continue, enter_login, get_correct_year, handle_inputs, perform_action
from pkg.utils import click_preapplication_button, find_fields_by_label, handle_calendar_select, handle_pre_application_button, handle_smart_autocomplete_fields, handle_textarea

class Handler:
    def __init__(self, bot):
        self.bot = bot

    def is_completed(self):
        val = input("Press any key to re-try, other press Enter: ")
        if len(val) > 0:
            return False
        return True
    
    def handle_job(self, job, parser):
        while True:
            try:
                if job.get('applied') == 'True':
                    continue
                if "workdayjobs" in job.get('apply'):
                    self.handle_workdayjobs()
                    return
                elif "bamboohr" in job.get('apply'):
                    click_preapplication_button(driver=self.bot.driver)
                    self.handle_bamboo()
                    return
                elif "smartrecruiters" in job.get('apply'):
                    resume_upload = self.bot.driver.find_element(By.XPATH, '//input[@class="file-upload-input"]')
                    resume_upload.send_keys(os.path.join(Path(__file__).parent.parent, self.bot.data['resume']))
                    sleep(5)
                    self.handle_smartrecruiters(parser=parser)
                    return
                elif "underdog.io" in job.get('apply'):
                    self.handle_underdog_fields()
                    return
                elif "lever" in job.get('apply'):
                    self.handle_lever()
                    return
                elif "greenhouse" in job.get('apply'):
                    self.handle_greenhouse()
                    return
                else:
                    parser.handle_fields()
                    return
            except BaseException as err:
                print('ERROR: ', err)
            finally:
                if self.is_completed() == True:
                    self.bot.mark_applied(job=job)
                    break
                else:
                    continue

    
    def handle_workdayjobs(self):
        print('Handling workday jobs...')

        try:
            WebDriverWait(self.bot.driver, timeout=10).until(
            lambda d: d.find_element(By.TAG_NAME, "html"))
            sleep(2)

            print('Creating account...')
            # Navigate to Create Account & Create Account
            click_hidden_button(self.bot.driver, '//button[@data-automation-id="createAccountLink"]')

            enter_login(self.bot.driver, '//button[@data-automation-id="createAccountSubmitButton"]', self.bot.data)
            input("Verify email and come back: ")

            # Enter Fields
            handle_inputs(self.bot.driver, self.bot.data)

            # Save & Continue
            click_save_and_continue(self.bot.driver)

            # Click Add Work & Education Experience
            click_add_fields(self.bot.driver)

            # Click "I Currently Work Here"
            perform_action(self.bot.driver, '//input[@data-automation-id="currentlyWorkHere"]', "click")

            # Click Calendar for Dates & Handle Dates
            perform_action(self.bot.driver, '//*[@data-automation-id="dateIcon"]', "click")
            get_correct_year(self.bot.driver, self.bot.data)

            months = self.bot.driver.find_elements(By.TAG_NAME, 'li')

            for month in months:
                if month.get_attribute('innerText') == "Nov":
                    month.click()
                    break

            # Upload Resume
            perform_action(self.bot.driver, '//input[@data-automation-id="file-upload-input-ref"]', "send keys", keys=self.bot.data['resume'])

            # Add Websites
            perform_action(self.bot.driver, '//input[@data-automation-id="website"]', "send keys", keys=self.bot.data['github'])

            # Add LinkedIn
            perform_action(self.bot.driver, '//input[@data-automation-id="linkedinQuestion"]', "send keys", keys=self.bot.data['linkedin'])

            handle_inputs(self.bot.driver, self.bot.data)

            # Save & Continue
            click_save_and_continue(self.bot.driver)

            # Handle Application Questions
            handle_inputs(self.bot.driver, self.bot.data)

            # Save & Continue
            click_save_and_continue(self.bot.driver)

            # Handle Voluntary Disclosures
            handle_inputs(self.bot.driver, self.bot.data)

            # Save & Continue
            click_save_and_continue(self.bot.driver)

            # Handle Self-Identify
            handle_inputs(self.bot.driver, self.bot.data)

            # Select Today's Date
            perform_action(self.bot.driver, '//*[@data-automation-id="dateIcon"]', "click")
            perform_action(self.bot.driver, '//*[@aria-selected="true"]', "click")

            # Save & Continue
            click_save_and_continue(self.bot.driver)
        except BaseException as err:
            raise(f'Failed to handle WorkDayJobs: {err}')
    
    def handle_smartrecruiters(self, parser):
        print('Handling smartrecruiters...')
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

            if len(sections) == 0:
                raise Exception('No sections found.')
            
            # What I need to do here is click all of the "Add" buttons, then handle the form inputs as I do with the "generic handler." #

            for section in sections:
                try:
                    section_header = section.find_element(By.TAG_NAME, 'h2').get_attribute('innerText')
                    print('Handling section: ', section_header)
                    
                    if "Experience" in section_header:
                        button = section.find_element(By.TAG_NAME, 'button')
                        button.click()

                        form_fields = section.find_elements(By.CLASS_NAME, 'form-control')

                        for field in form_fields:
                            try:
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
                            except BaseException as err:
                                print(err)
                                continue

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
                                currently_attend = field.find_element(By.XPATH, '//*[@data-test="education-current"]')
                                currently_attend.click()
                                
                                calendar_button = field.find_element(By.XPATH, '//button[@aria-label="Open calendar"]')
                                calendar_button.click()

                                # Select Year
                                handle_calendar_select(self.bot.driver, self.bot.data['universityStartYear'])
                                
                                # Select Month
                                handle_calendar_select(self.bot.driver, self.bot.data['universityStartMonth'])

                                # Save
                                save_button = field.find_element(By.XPATH, '//button[@data-test="education-save"]')
                                save_button.click()
                except BaseException as err:
                    print(f'Error: {err}')
                    continue
            
            # Handle remaining generic fields
            parser.handle_fields()
        except BaseException as err:
            raise Exception(f'Failed to handle SmartRecruiters: {err}')

    def handle_underdog_fields(self):
        print('Handling underdog...')

        def select_option(selection):
            options = self.bot.driver.find_elements(By.TAG_NAME, "option")
            for option in options:
                option_name = option.get_attribute('textContent')
                if option_name == selection:
                    option.click()

        try:
            dropdowns = self.bot.driver.find_elements(By.CLASS_NAME, "div-block-37")
            print(f'{len(dropdowns)} dropdowns found.')

            if len(dropdowns) == 0:
                try:
                    print('Attempting to find pre-application button')
                    # Try to click 'Apply' button in order to find dropdowns.
                    handle_pre_application_button(driver=self.bot.driver)
                    sleep(2)

                    # If click is successful, try finding dropdowns again.
                    dropdowns = self.bot.driver.find_elements(By.CLASS_NAME, "div-block-37")
                except BaseException as err:
                    print("Error: ", err)
                    raise Exception('Error finding dropdowns and/or apply button.')
        
            for element in dropdowns:
                element.click()

                options = self.bot.driver.find_elements(By.TAG_NAME, "option")
                print(f'{len(options)} options found.')

                select_fields = self.bot.driver.find_elements(By.TAG_NAME, "select")
                print(f'{len(select_fields)} select fields found.')

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
                print(f'{len(hidden_inputs)} hidden inputs found.')

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
                            input.send_keys(self.bot.data['jobSkills'])
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
                            element.send_keys(os.path.dirname(os.path.abspath(__file__)), os.path.join(self.bot.data['resume']))
                        if "last" in field_name.lower():
                            element.send_keys(self.bot.data['lastName'])
                        if "email" in field_name.lower():
                            element.send_keys(self.bot.data['email'])
                        if "website" in field_name.lower():
                            element.send_keys(self.bot.data['linkedIn'])
                        if "github" in field_name.lower() or "portfolio" in field_name.lower():
                            element.send_keys(self.bot.data['portfolio'])

        except BaseException as err:
            print('Error: ', err)
            raise Exception('Failed to complete underdog handling.')
        
    def handle_lever(self):
        try:
            print('Running lever.co handler...')
            elements = find_lever_elements(driver=self.bot.driver)
            print(f'{len(elements)} elements found.')

            # If no elements found, it's because I need to handle some interaction.
            if len(elements) == 0:
                try:
                    # Try to see if application button is found, if not raise exception.
                    handle_pre_application_button(driver=self.bot.driver)
                    sleep(3)

                    # If button was clicked successfully, re-assign elements variable to newly found elements.
                    elements = find_lever_elements(driver=self.bot.driver)
                except BaseException as err:
                    raise Exception('No elements found on page. Apply button not able to be clicked.')

            print(f'Handling {len(elements)} elements...')
            for element in elements:
                try:
                    field_name =  element.find_element(By.TAG_NAME, "label").get_attribute('innerText')

                    if not "Resume" in field_name:
                        element.click()

                    print('Handling lever fields...')
                    handle_lever_fields(field_name, element, self.bot.data, self.bot.questions)
                except BaseException as err:
                    print(f'Error handling field: {err}')
                    continue

        except BaseException as err:
            print('Error: ', err)
            raise Exception('Failed to complete lever handling.')
    
    def handle_greenhouse(self):
        try:
            print('Running greenhouse handler...')
            dropdowns = self.bot.driver.find_elements(By.CLASS_NAME, "field")

            input_fields = find_fields_by_label(driver=self.bot.driver)

            print(f'Handling {len(input_fields)} input fields...')
            for input_field in input_fields:
                if "First" in input_field['label']:
                    if input_field['element'].get_attribute('value') == "":
                        input_field['element'].send_keys(self.bot.data['firstName'])
                if "Last" in input_field['label']:
                    if input_field['element'].get_attribute('value') == "":
                        input_field['element'].send_keys(self.bot.data['lastName'])
                if "Email" in input_field['label']:
                    if input_field['element'].get_attribute('value') == "":
                        input_field['element'].send_keys(self.bot.data['email'])
                if "Phone" in input_field['label']:
                    if input_field['element'].get_attribute('value') == "":
                        input_field['element'].send_keys(self.bot.data['phoneNumber'])

            print(f'Handling {len(dropdowns)} dropdowns...')
            for element in dropdowns:
                try:
                    element.click()
                    field_name = element.find_element(By.TAG_NAME, "label").get_attribute('innerText')

                    if "School" or "Degree" or "Discipline" in field_name:
                        handle_greenhouse_autocomplete(driver=self.bot.driver, data=self.bot.data, field_name=field_name)
                        sleep(1)
                    
                    handle_hidden_field(field_name, element, driver=self.bot.driver, data=self.bot.data, questions=self.bot.questions)
                except BaseException as err:
                    print(f'Error handling field: {err}')
                    continue

        except BaseException as err:
            print('Error: ', err)
            raise Exception('Failed to complete greenhouse handling.')