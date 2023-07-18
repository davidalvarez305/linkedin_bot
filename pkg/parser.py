from logging import Logger
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.common.by import By
from time import sleep

class Parser:
    def __init__(self, questions, data, driver):
        self.fields = []
        self.questions = questions
        self.data = data
        self.driver = driver

    def get_element(self, element: WebElement):
        attributes = ['id', 'name', 'class']
        for attr in attributes:
            attribute = element.get_attribute(attr)
            for question in self.questions:
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

    def find_form_fields(self):
        form_elements = []

        tag_names = ['select', 'input', 'button', 'textarea']

        for tag in tag_names:
            if len(form_elements) > 0:
                form_elements += self.driver.find_elements(By.TAG_NAME, tag)
            else:
                form_elements = self.driver.find_elements(By.TAG_NAME, tag)

        for element in form_elements:
            field = self.get_element(element=element)
            if field:
                self.fields.append(field)

    def find_fields_by_label(self):
        labels = self.driver.find_elements(By.TAG_NAME, 'label')

        # Append fields by label.
        for label in labels:
            field = {}

            html_for = label.get_attribute('for')
            if html_for:
                try:
                    field['label'] = label.get_attribute('textContent')
                    field['id'] = label.get_attribute('for')

                    input_field = self.driver.find_element(By.ID, field['id'])
                    field['tagName'] = input_field.get_attribute('tagName')
                    field['element'] = input_field

                    self.fields.append(field)
                except BaseException:
                    continue

    def handle_fields(self):
        print('Handling generic fields...')

        # Find fields and append to self.fields
        self.find_fields_by_label()
        self.find_form_fields()
            
        if len(self.fields) == 0:
            raise Exception('No fields were found.')

        print(f'{len(self.fields)} input fields found.')

        for field in self.fields:
            print('FIELD: ', field)
            try:
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
                                field['element'].send_keys(self.data['resume'])

                # Handle Select Buttons
                elif field['tagName'] == 'SELECT':
                    for question in self.questions:
                        if any(substr in field['label'].lower() for substr in question['question']):
                            if self.data[f"{question['data']}"].lower() in field['element'].get_attribute('value').lower():
                                field['element'].click()
                                sleep(1)

                            options = field['element'].find_elements(By.TAG_NAME, 'option')
                            for option in options:
                                if self.data[f"{question['data']}"].lower() in option.get_attribute('textContent').lower():
                                    option.click()

                # Handle Checkboxes & Radio Buttons
                elif field['tagName'] == 'INPUT' and field['element'].get_attribute('type') in ['checkbox', 'radio']:
                    for question in self.questions:
                        if any(substr in field['label'].lower() for substr in question['question']):
                            if self.data[f"{question['data']}"].lower() in field['element'].get_attribute('value').lower():
                                field['element'].click()

                # Handle Normal Inputs
                else:
                    for question in self.questions:
                        if any(substr in field['label'].lower() for substr in question['question']):
                            if field['element'].get_attribute('value') == "":
                                field['element'].send_keys(self.data[f"{question['data']}"])

            except BaseException as err:
                print(f'Error handling parser field: {err}')
                continue