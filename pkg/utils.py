from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.webdriver import WebDriver

def find_fields_by_label(driver: WebDriver):
    labels = driver.find_elements(By.TAG_NAME, 'label')

    fields = []

    # Append fields by label.
    for label in labels:
        field = {}

        html_for = label.get_attribute('for')
        if html_for:
            try:

                field['label'] = label.get_attribute('innerText')
                field['id'] = label.get_attribute('for')

                input_field = driver.find_element(By.ID, field['id'])
                field['tagName'] = input_field.get_attribute('tagName')
                field['element'] = input_field

                fields.append(field)

            except BaseException:
                continue
    
    return fields

def click_preapplication_button(driver):
    button = driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/div/div/button")
    button.click()

def field_match(option, data):
    if option == data or data in option:
        return True

    option_arr = option.split(' ')
    data_arr = data.split(' ')

    count = 0
    for f in option_arr:
        for d in data_arr:
            if f.lower() == d.lower():
                count += 1
    return count / len(option_arr) >= .35

def handle_select_child_options(element, user_data):
    options = element.find_elements(By.XPATH, '//li[@role="option"]')

    if (len(options)) == 0:
        options = element.find_elements(By.TAG_NAME, 'option')

    for option in options:
        if field_match(option=option.get_attribute('innerText'), data=user_data):
            option.click()
            return
    
def handle_input_field(element, user_data, xpath):
    input = element.find_element(By.XPATH, xpath)
    if input.get_attribute('value') == "":
        input.send_keys(user_data)

def handle_textarea(element, user_data):
    textarea = element.find_element(By.TAG_NAME, "textarea")
    if textarea.get_attribute('value') == "":
        textarea.send_keys(user_data)

def handle_smart_autocomplete_fields(input, user_data):
    input.send_keys(user_data)
    sleep(1)
    input.send_keys(Keys.ARROW_DOWN)
    input.send_keys(Keys.RETURN)

def handle_calendar_select(driver, user_data):
    elements = driver.find_elements(By.CSS_SELECTOR, 'div.mat-calendar-body-cell-content.mat-focus-indicator')
    for el in elements:
        if str(user_data) in el.get_attribute('textContent'):
            el.click()
            return

def handle_pre_application_button(driver: WebDriver):
    try:
        buttons = driver.find_elements(By.TAG_NAME, 'a')
        buttons += driver.find_elements(By.TAG_NAME, 'button')
        print(f'{len(buttons)} buttons found for pre-application flow.')

        for button in buttons:
            button_text = button.get_attribute('textContent')
            if button_text is not None and 'Apply' in button_text:
                button.click()
                return

    except BaseException as err:
        raise Exception(err)