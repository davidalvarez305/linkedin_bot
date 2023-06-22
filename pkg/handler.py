from time import sleep
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

from pkg.sites.workdayjobs import click_add_fields, click_hidden_button, click_save_and_continue, enter_login, get_correct_year, handle_inputs, perform_action

class Handler:
    def __init__(self, bot):
        self.bot = bot
    
    def handle_job(self, job):
        if "workdayjobs" in job['apply']:
            self.handle_workdayjobs()
            return
        if "bamboohr" in job['apply']:
            self.click_preapplication_button(driver=self.driver)
            self.bamboo(driver=self.driver, data=self.data)
        if "smartrecruiters" in job['apply']:
            self.upload_smartrecruiters_resume(driver=self.driver)
        try:
            if "greenhouse" in job['apply']:
                self.greenhouse(driver=self.driver, data=self.data, values=self.values)
            elif "smartrecruiters" in job['apply']:
                self.smartrecruiters(driver=self.driver, data=self.data, values=self.values)
            elif "lever" in job['apply']:
                self.lever(driver=self.driver, data=self.data, values=self.values)
            elif "underdog.io" in job['apply']:
                self.underdog(driver=self.driver, data=self.data, values=self.values)
            else:
                self.enter_fields(self.driver, self.values, self.data)
        except BaseException:
            pass
    
    def handle_workdayjobs(self):
        self.bot.driver.get(self.bot.data['apply'])

        WebDriverWait(self.bot.driver, timeout=10).until(
            lambda d: d.find_element(By.TAG_NAME, "html"))
        sleep(2)

        # Navigate to Create Account & Create Account
        click_hidden_button(self.bot.driver, '//button[@data-automation-id="createAccountLink"]')

        # enter_login(self.bot.driver, '//button[@data-automation-id="createAccountSubmitButton"]')
        input("Verify email and come back: ")

        # Return to Sign In Screen
        click_hidden_button(self.bot.driver, '//button[@data-automation-id="signInLink"]')

        # Submit & Verify Email -- Then Login
        enter_login(self.bot.driver, '//button[@data-automation-id="signInSubmitButton"]')
        sleep(5)

        # Apply Manually
        click_hidden_button(self.bot.driver, '//*[@data-automation-id="applyManually"]')
        sleep(5)

        # Enter Fields
        handle_inputs(self.bot.driver)

        # Save & Continue
        click_save_and_continue(self.bot.driver)

        # Click Add Work & Education Experience
        click_add_fields(self.bot.driver)

        # Click "I Currently Work Here"
        perform_action(self.bot.driver, '//input[@data-automation-id="currentlyWorkHere"]', "click")

        # Click Calendar for Dates & Handle Dates
        perform_action(self.bot.driver, '//*[@data-automation-id="dateIcon"]', "click")
        get_correct_year(self.bot.driver)

        months = self.bot.driver.find_elements(By.TAG_NAME, 'li')

        for month in months:
            if month.get_attribute('innerText') == "Nov":
                month.click()
                break

        # Upload Resume
        perform_action(self.bot.driver, '//input[@data-automation-id="file-upload-input-ref"]', "send keys", keys=self.bot.data['resume'])

        # Add Websites
        perform_action(self.bot.driver, '//input[@data-automation-id="website"]', "send keys", keys='https://github.com/davidalvarez305')

        # Add LinkedIn
        perform_action(self.bot.driver, '//input[@data-automation-id="linkedinQuestion"]', "send keys", keys=self.bot.data['linkedin'])

        handle_inputs(self.bot.driver)

        # Save & Continue
        click_save_and_continue(self.bot.driver)

        # Handle Application Questions
        handle_inputs(self.bot.driver)

        # Save & Continue
        click_save_and_continue(self.bot.driver)

        # Handle Voluntary Disclosures
        handle_inputs(self.bot.driver)

        # Save & Continue
        click_save_and_continue(self.bot.driver)

        # Handle Self-Identify
        handle_inputs(self.bot.driver)

        # Select Today's Date
        perform_action(self.bot.driver, '//*[@data-automation-id="dateIcon"]', "click")
        perform_action(self.bot.driver, '//*[@aria-selected="true"]', "click")

        # Save & Continue
        click_save_and_continue(self.bot.driver)