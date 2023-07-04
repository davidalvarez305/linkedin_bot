from time import sleep
from ..utils import field_match, find_fields_by_label, handle_input_field, handle_select_child_options
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
            element.send_keys(data['resume'])
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