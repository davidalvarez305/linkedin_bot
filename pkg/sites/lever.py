from datetime import datetime
import os
from utils import complete_prompt, handle_input_field, handle_select_child_options
from selenium.webdriver.common.by import By


def handle_lever_fields(field_name, element, data, values):
    select_fields = element.find_elements(By.TAG_NAME, 'select')

    if "Today's date" in field_name:
        handle_input_field(element, datetime.today().strftime('%m/%d/%Y'), x_path)
    elif "Full" in field_name:
        handle_input_field(element, f"{data['user']['firstName']} {data['user']['lastName']}", x_path)
    elif "job posting" in field_name:
        handle_select_child_options(element, "linkedin")
    elif "resume" in field_name.lower():
        element.send_keys(os.environ.get('RESUME_PATH'))
    else:
        for value in values:
            if any(substr in field_name.lower() for substr in value['question']):
                if len(select_fields) > 0:
                    handle_select_child_options(element, data['user'][f"{value['data']}"])
                else:
                    x_path = './label/div/input'
                    handle_input_field(element, data['user'][f"{value['data']}"], x_path)

def handle_lever(driver, data, values):
    try:
        elements = driver.find_elements(By.CLASS_NAME, "application-question")

        elements += driver.find_elements(By.CLASS_NAME, "custom-question")

        elements += driver.find_elements(By.CLASS_NAME, "application-dropdown")

        elements += driver.find_elements(By.CLASS_NAME, "application-additional")

        for element in elements:
            field_name =  element.find_element(By.XPATH, "./label").get_attribute('innerText')

            if not "Resume" in field_name:
                element.click()

            handle_lever_fields(field_name, element, data, values)
    except BaseException as err:
        print(err)
        pass

def lever(driver, data, values):
    to_continue = True
    while (to_continue):
        try:
            handle_lever(driver, data, values)
            to_continue = complete_prompt()
        except BaseException:
            to_continue = complete_prompt()
            continue