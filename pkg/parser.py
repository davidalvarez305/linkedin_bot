from selenium.webdriver.remote.webdriver import WebElement, WebDriver
from selenium.webdriver.common.by import By
from time import sleep

class Parser:
    def __init__(self):
        self.fields = []

    def get_element(element: WebElement, values):
        attributes = ['id', 'name', 'class']
        for attr in attributes:
            attribute = element.get_attribute(attr)
            for question in values:
                try:
                    if attribute and attribute.lower() in question['question']:
                        field = {}

                        field['label'] = question['question'][0]
                        field[attr] = attribute

                        field['tagName'] = element.get_attribute('tagName')
                        field['element'] = element
                        return field
                except BaseException:
                    continue

    def find_form_fields(self, driver: WebDriver, values):
        form_elements = []

        tag_names = ['select', 'input', 'button', 'textarea']

        for tag in tag_names:
            form_elements += driver.find_elements(By.TAG_NAME, tag)

        for element in form_elements:
            field = self.get_element(element, values)
            if field:
                self.fields.append(field)

    def find_fields_by_label(self, driver: WebDriver):
        labels = driver.find_elements(By.TAG_NAME, 'label')

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

                    self.fields.append(field)

                except BaseException:
                    continue

    def handle_fields(self, values, data):
        for field in self.fields:
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
                                field['element'].send_keys(data['resume'])

                # Handle Select Buttons
                elif field['tagName'] == 'SELECT':
                    for question in values:
                        if any(substr in field['label'].lower() for substr in question['question']):
                            if data[f"{question['data']}"].lower() in field['element'].get_attribute('value').lower():
                                field['element'].click()
                                sleep(1)

                            options = field['element'].find_elements(By.TAG_NAME, 'option')
                            for option in options:
                                if data[f"{question['data']}"].lower() in option.get_attribute('textContent').lower():
                                    option.click()

                # Handle Checkboxes & Radio Buttons
                elif field['tagName'] == 'INPUT' and field['element'].get_attribute('type') in ['checkbox', 'radio']:
                    for question in values:
                        if any(substr in field['label'].lower() for substr in question['question']):
                            if data[f"{question['data']}"].lower() in field['element'].get_attribute('value').lower():
                                field['element'].click()

                # Handle Normal Inputs
                else:
                    for question in values:
                        if any(substr in field['label'].lower() for substr in question['question']):
                            if field['element'].get_attribute('value') == "":
                                field['element'].send_keys(data[f"{question['data']}"])