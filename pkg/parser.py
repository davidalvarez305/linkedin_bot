from selenium.webdriver.remote.webdriver import WebElement, WebDriver
from selenium.webdriver.common.by import By

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