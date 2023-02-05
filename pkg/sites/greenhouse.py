import os
from time import sleep
from utils import complete_prompt, field_match, find_fields_by_label, handle_input_field, handle_select_child_options
from selenium.webdriver.common.by import By

def handle_greenhouse_autocomplete(driver, data, field_name):

    def handle_input(input, user_data):
        input.send_keys(user_data)
        sleep(1.5)
        drop_element = driver.find_element(By.ID, "selectedOption")
        drop_element.click()

    autocomplete_fields = driver.find_elements(By.XPATH, '//div[@class="select2-search"]')

    for field in autocomplete_fields:
        try:
            # Handle Autocomplete Fields
            if "School" in field_name:
                handle_input(field.find_element(By.TAG_NAME, "input"), data['user']['school'])
            if "Are you 18" in field_name:
                handle_input(field.find_element(By.TAG_NAME, "input"), "Yes")
            if "authorized" in field_name:
                handle_input(field.find_element(By.TAG_NAME, "input"), data['user']['workAuthorization'])
            if "Degree" in field_name or "degree" in field_name:
                handle_input(field.find_element(By.TAG_NAME, "input"), "Associate")
            if "Discipline" in field_name:
                handle_input(field.find_element(By.TAG_NAME, "input"), "Business")
        except BaseException:
            continue

def handle_hidden_field(field_name, element, driver, data, values):
    select_fields = element.find_elements(By.TAG_NAME, 'select')

    for value in values:
        if "Were you referred by" in field_name:
            handle_select_child_options(element, "No")
        if "resume" in field_name.lower():
            element.send_keys(os.environ.get('RESUME_PATH'))
        if "require" in field_name and "immigration" in field_name:
            btns = driver.find_elements(By.CLASS_NAME, "application-answer-alternative")
            for btn in btns:
                if field_match(btn.get_attribute('textContent'), data=data['user']['immigrationSponsorship']):
                    btn.click()
        if any(substr in field_name.lower() for substr in value['question']):
            if len(select_fields) > 0:
                handle_select_child_options(element, data['user'][f"{value['data']}"])
            else:
                x_path = './label/input[@type="text"]'
                handle_input_field(element, data['user'][f"{value['data']}"], x_path)

def handle_greenhouse(driver, data, values):
    try:
        # Get Fields
        dropdowns = driver.find_elements(By.CLASS_NAME, "field")

        input_fields = find_fields_by_label(driver=driver)

        for input_field in input_fields:
            if "First" in input_field['label']:
                if input_field['element'].get_attribute('value') == "":
                    input_field['element'].send_keys(data['user']['firstName'])
            if "Last" in input_field['label']:
                if input_field['element'].get_attribute('value') == "":
                    input_field['element'].send_keys(data['user']['lastName'])
            if "Email" in input_field['label']:
                if input_field['element'].get_attribute('value') == "":
                    input_field['element'].send_keys(data['user']['email'])
            if "Phone" in input_field['label']:
                if input_field['element'].get_attribute('value') == "":
                    input_field['element'].send_keys(data['user']['phoneNumber'])

        for element in dropdowns:
                element.click()
                field_name = element.find_element(By.XPATH, "./label").get_attribute('innerText')

                if "School" or "Degree" or "Discipline" in field_name:
                    handle_greenhouse_autocomplete(driver, data, field_name)
                    sleep(1)
                
                handle_hidden_field(field_name, element, driver, data, values)
    except BaseException as err:
        print(err)
        pass

def greenhouse(driver, data, values):
    to_continue = True
    while (to_continue):
        try:
            handle_greenhouse(driver, data, values)
            to_continue = complete_prompt()
        except BaseException:
            to_continue = complete_prompt()
            continue