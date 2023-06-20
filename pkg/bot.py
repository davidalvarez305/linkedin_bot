from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import os
import json
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from. helpers.sheets import get_values, write_values

from .sites.linkedin import extract_job_data, go_to_jobs_search
from .handle_fields import enter_fields
from .sites.bamboo import bamboo
from .sites.underdog import underdog
from .sites.lever import lever
from .sites.smartrecruiters import smartrecruiters, upload_smartrecruiters_resume
from .sites.greenhouse import greenhouse
from .sites.workdayjobs import handle_workdayjobs
from .utils import click_preapplication_button

def read_data_from_json():
    file_path = os.path.join(os.getcwd(), "data.json")
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"Error: The file 'data.json' does not exist.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON in 'data.json'.")
        return None

class Bot:
    def __init__(self):
        self.jobs = []
        self.values = []
        self.keywords = []
        self.data = read_data_from_json()

        # Get Spreadsheet Values
        rows = get_values(os.environ.get('SHEETS_ID'), f"{os.environ.get('TAB_NAME')}!A2:E")
        for row in rows:
            self.values.append({ "data": row[0], "question": row[1:] })

        if self.data is None:
            raise Exception("Data from JSON file could not be loaded.")

    def crawl_jobs(self, keyword):
        # Initialize Driver
        self.driver = webdriver.Firefox()
        self.driver.get("https://www.linkedin.com/login")

        input("Press enter after logging in: ")

        # Access Job Search
        go_to_jobs_search(driver=self.driver, keyword=keyword)

        sleep(5)
        current_page = 1

        while (current_page < 40):
            try:
                pages_list = self.driver.find_element(By.CSS_SELECTOR, 'ul.artdeco-pagination__pages.artdeco-pagination__pages--number')
                pg_buttons = pages_list.find_elements(By.TAG_NAME, 'li')

                jobs_container = self.driver.find_element(By.CLASS_NAME, 'scaffold-layout__list-container')
                jobs = jobs_container.find_elements(By.TAG_NAME, 'li')

                for job in jobs:
                    
                    # Only the links with the following attribute are job listings -> so if it's not found, skip
                    if job.get_attribute('data-occludable-job-id') is None:
                        continue

                    try:
                        job_data = extract_job_data(web_element=job, driver=self.driver)
                        self.jobs.append(job_data)
                    except BaseException as err:
                        print("ERROR FINDING JOB: ", err)
                    finally:
                        continue

                for index, btn in enumerate(pg_buttons):
                    if int(btn.get_attribute('data-test-pagination-page-btn')) == current_page + 1:
                        btn.click()
                        sleep(5)
            except BaseException as err:
                # Only click the tree dots if the previous index was not one, otherwise, we'll keep circling back.
                if "int() argument must be a string" in err.__str__() and int(pg_buttons[index - 1].get_attribute('data-test-pagination-page-btn')) != 1:
                    btn.click()
                    sleep(5)
                else:
                    print(err)
            finally:
                current_page += 1

                self.save_jobs()

                # After jobs are saved in Google Sheets -> reset the list so that they're not saved twice
                self.jobs = []
                continue

    def apply_to_jobs(self):

        if len(self.jobs) == 0:
            raise Exception("There are no jobs to apply for.")

        for job in self.jobs:
            if "workdayjobs" in job['link']:
                handle_workdayjobs(driver=self.driver, data=self.data)
                return
            if "bamboohr" in job['link']:
                click_preapplication_button(driver=self.driver)
                bamboo(driver=self.driver, data=self.data)
            if "smartrecruiters" in job['link']:
                upload_smartrecruiters_resume(driver=self.driver)
            try:
                if "greenhouse" in job['link']:
                    greenhouse(driver=self.driver, data=self.data, values=self.values)
                elif "smartrecruiters" in job['link']:
                    smartrecruiters(driver=self.driver, data=self.data, values=self.values)
                elif "lever" in job['link']:
                    lever(driver=self.driver, data=self.data, values=self.values)
                elif "underdog.io" in job['link']:
                    underdog(driver=self.driver, data=self.data, values=self.values)
                else:
                    enter_fields(self.driver, self.values, self.data)
            except BaseException:
                continue

    def save_jobs(self):
        rows = get_values(os.environ.get('SHEETS_ID'), f"{os.environ.get('JOBS_TAB')}!A2:E")
        headers = rows[0]

        jobs = []
        for job in self.jobs:
            job_data = []
            for header in headers:
                job_data.append(job[header])

            jobs.append(job_data)
        rows += jobs

        write_values(spreadsheet_id=os.environ.get('SHEETS_ID'), range=f"{os.environ.get('JOBS_TAB')}!A2:E", values=rows)

    def get_jobs_from_sheets(self):
        rows = get_values(spreadsheet_id=os.environ.get('SHEETS_ID'), range=f"{os.environ.get('JOBS_TAB')}!A:E")
        headers = rows[0]

        for job in rows[0:]:
            job_data = {}
            for header in headers:
                job_data[header] = job[header]

            self.jobs.append(job_data)

    def get_keywords(self):
        rows = get_values(spreadsheet_id=os.environ.get('SHEETS_ID'), range=f"{os.environ.get('KEYWORDS_TAB')}!A:C")
        headers = rows[0]

        for job in rows[0:]:
            job_data = {}
            for header in headers:
                job_data[header] = job[header]

            self.keywords.append(job_data)