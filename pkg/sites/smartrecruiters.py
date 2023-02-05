
import os
from time import sleep
from selenium.webdriver.common.by import By

from utils import complete_prompt, handle_calendar_select, handle_smart_autocomplete_fields

def upload_smartrecruiters_resume(driver):
    resume_upload = driver.find_element(By.XPATH, '//input[@class="file-upload-input"]')
    resume_upload.send_keys(os.environ.get('RESUME_PATH'))
    sleep(5)

def handle_smartrecruiters(driver, data, values):
    sleep(1)

    try:
        # Delete Resume Fields
        field_options = driver.find_elements(By.XPATH, '//button[@aria-label="See options"]')
        for option in field_options:
            option.click()

            # Click 'Delete Position in Dropdown & Wait for Dialogue Box to Open'
            delete_position = driver.find_element(By.XPATH, '//button[@data-test="entry-delete"]')
            delete_position.click()
            sleep(2)

            yes_button = driver.find_element(By.XPATH, '//mat-dialog-container/oc-yes-no/div/div/button[2]')
            yes_button.click()

        sections = driver.find_elements(By.CLASS_NAME, 'form-section')

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
                    handle_smart_autocomplete_fields(input_element, os.environ.get('TITLE'))
                if "Company" in label:
                    input_element = field.find_element(By.TAG_NAME, 'input')
                    handle_smart_autocomplete_fields(input_element, data['user']['currentCompany'])
                if "Office location" in label:
                    input_element = field.find_element(By.CLASS_NAME, 'sr-location-autocomplete')
                    handle_smart_autocomplete_fields(input_element, os.environ.get('COMPANY_LOCATION'))
                if "Description" in label:
                    input_element = field.find_element(By.TAG_NAME, 'textarea')
                    handle_smart_autocomplete_fields(input_element, os.environ.get('JOB_DESCRIPTION'))
                if "From" in label:
                    work_here = field.find_element(By.XPATH, '//*[@data-test="experience-current"]')
                    work_here.click()
                    
                    calendar_button = field.find_element(By.XPATH, '//button[@aria-label="Open calendar"]')
                    calendar_button.click()

                    # Select Year
                    handle_calendar_select(driver, os.environ.get('JOB_START_YEAR'))
                    # Select Month
                    handle_calendar_select(driver, os.environ.get('JOB_START_MONTH'))

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
                        handle_smart_autocomplete_fields(input_element, data['user']['school'])
                    if "Major" in label:
                        input_element = field.find_element(By.TAG_NAME, 'input')
                        input_element.send_keys(data['user']['discipline'])
                    if "Degree" in label:
                        input_element = field.find_element(By.TAG_NAME, 'input')
                        input_element.send_keys(data['user']['degree'])
                    if "School location" in label:
                        input_element = field.find_element(By.CLASS_NAME, 'sr-location-autocomplete')
                        handle_smart_autocomplete_fields(input_element, os.environ.get('SCHOOL_LOCATION'))
                    if "Description" in label:
                        input_element = field.find_element(By.TAG_NAME, 'textarea')
                        handle_smart_autocomplete_fields(input_element, os.environ.get('DEGREE_DESCRIPTION'))
                    if "From" in label:
                        work_here = field.find_element(By.XPATH, '//*[@data-test="education-current"]')
                        work_here.click()
                        
                        calendar_button = field.find_element(By.XPATH, '//button[@aria-label="Open calendar"]')
                        calendar_button.click()

                        # Select Year
                        handle_calendar_select(driver, os.environ.get('SCHOOL_START_YEAR'))
                        # Select Month
                        handle_calendar_select(driver, os.environ.get('SCHOOL_START_MONTH'))

                        # Save
                        save_button = field.find_element(By.XPATH, '//button[@data-test="education-save"]')
                        save_button.click()
    except BaseException as err:
        print(err)
        pass

def smartrecruiters(driver, data, values):
    to_continue = True
    while (to_continue):
        try:
            handle_smartrecruiters(driver, data, values)
            to_continue = complete_prompt()
        except BaseException:
            to_continue = complete_prompt()
            continue