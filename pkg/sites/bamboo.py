from list import COMMON_QUESTIONS
from utils import complete_prompt, handle_textarea
from selenium.webdriver.common.by import By


def handle_select_div(driver, user_data):
    options = driver.find_elements(By.CLASS_NAME, "fab-MenuOption__row")
    for option in options:
        option_name = option.get_attribute('innerText')
        if user_data.lower() in option_name.lower():
            option.click()

def handle_bamboo(driver, data):
    try:
        elements = driver.find_elements(By.CLASS_NAME, "CandidateForm__row")

        for element in elements:
            field_name = element.find_element(By.TAG_NAME, "label").get_attribute('innerText')

            # Handle Radiobuttons
            if "Veteran" in field_name:
                btns = driver.find_elements(By.XPATH, '//*[@type="radio"]')
                for btn in btns:
                    label = btn.find_element(By.XPATH, '../label').get_attribute('innerText')
                    if data['user']['veteranStatus'].lower() in label.lower():
                        btn.click()

            # Handle Selects
            if "Gender" in field_name:
                element.click()
                handle_select_div(driver, data['user']['gender'])
            elif "Disability" in field_name:
                element.click()
                handle_select_div(driver, data['user']['disabilityStatus'])
            elif "Ethnicity" in field_name:
                element.click()
                handle_select_div(driver, data['user']['race'])

            # Handle Inputs
            else:
                for question in COMMON_QUESTIONS:
                    if question['question'].lower() in field_name.lower():
                        field = question['data']
                        handle_textarea(element, data['user'][f"{field}"])
    except BaseException as err:
        print(err)
        pass

def bamboo(driver, data):
    to_continue = True
    while (to_continue):
        try:
            handle_bamboo(driver, data)
            to_continue = complete_prompt()
        except BaseException:
            to_continue = complete_prompt()
            continue