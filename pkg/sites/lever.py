from datetime import datetime
from ..utils import handle_input_field, handle_select_child_options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

def handle_lever_fields(field_name, element, data, questions):
    select_fields = element.find_elements(By.TAG_NAME, 'select')

    if "Today's date" in field_name:
        handle_input_field(element, datetime.today().strftime('%m/%d/%Y'), x_path)
    elif "Full" in field_name:
        handle_input_field(element, f"{data['firstName']} {data['lastName']}", x_path)
    elif "job posting" in field_name:
        handle_select_child_options(element, "linkedin")
    elif "resume" in field_name.lower():
        element.send_keys(data['resume'])
    else:
        for question in questions:
            if any(substr in field_name.lower() for substr in question['question']):
                if len(select_fields) > 0:
                    handle_select_child_options(element, data[f"{question['data']}"])
                else:
                    x_path = './label/div/input'
                    handle_input_field(element, data[f"{question['data']}"], x_path)
    
def find_lever_elements(driver: WebDriver):
    elements = driver.find_elements(By.CLASS_NAME, "application-question")

    elements += driver.find_elements(By.CLASS_NAME, "custom-question")

    elements += driver.find_elements(By.CLASS_NAME, "application-dropdown")

    elements += driver.find_elements(By.CLASS_NAME, "application-additional")

    return elements