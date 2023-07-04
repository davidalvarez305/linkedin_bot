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

def handle_pre_application_button(driver: WebDriver):
    try:
        apply_button = driver.find_element(By.CLASS_NAME, 'postings-btn template-btn-submit hex-color')
        button_text = apply_button.get_attribute('textContent')

        if button_text is not None and 'Apply' in button_text:
            apply_button.click()
    except BaseException as err:
        raise Exception(err)