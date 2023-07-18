from selenium import webdriver
import os
import json
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pkg.parser import Parser

from pkg.handler import Handler
from. helpers.sheets import get_values, write_values

from .sites.linkedin import extract_job_data
from urllib.parse import quote

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

def initialize_driver():
    driver = webdriver.Firefox()
    
    # Maximize the browser window (optional)
    driver.maximize_window()
    
    # Wait for the page to be loaded completely
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    
    return driver

class Bot:
    def __init__(self):
        self.jobs = []
        self.questions = []
        self.keywords = []
        self.data = read_data_from_json()

        # Get Spreadsheet Values
        rows = get_values(os.environ.get('SHEETS_ID'), f"{os.environ.get('TAB_NAME')}!A2:E")
        for row in rows:
            self.questions.append({ "data": row[0], "question": row[1:] })

        if self.data is None:
            raise Exception("Data from JSON file could not be loaded.")

    def crawl_jobs(self, keyword):
        try:
            # Initialize Driver
            self.driver = webdriver.Firefox()

            self.driver.get(f"https://www.linkedin.com/jobs/search/?f_E=2%2C3&f_WT=2&keywords={quote(keyword)}")

            i = 500
            n = 0

            # First scroll to the bottom of the page so that all of the potential job listings are available
            while(i < 2000):
                try:
                    self.driver.execute_script(f'window.scrollBy({n}, {i})')
                    n = i
                    i += 500
                    sleep(2)

                    see_more_jobs = self.driver.find_element(By.XPATH, '//button[@data-tracking-control-name="infinite-scroller_show-more"]')
                    see_more_jobs.click()

                except BaseException as err:
                    continue

            # Now, actually save the jobs
            try:
                jobs_container = self.driver.find_element(By.CLASS_NAME, 'jobs-search__results-list')
                jobs = jobs_container.find_elements(By.TAG_NAME, 'li')

                print(f'{len(jobs)} jobs were found.')

                index = 0
                for job in jobs:
                    try:
                        job_data = extract_job_data(web_element=job, driver=self.driver)
                        self.jobs.append(job_data)
                    except BaseException as err:
                        print("ERROR FINDING JOB: ", err)
                        continue
                    finally:
                        index += 1
                        if index % 10 == 0:
                            self.save_jobs()

                # After jobs are saved in Google Sheets -> reset the list so that they're not saved twice
                self.jobs = []

            except BaseException as err:
                raise Exception(f'Failed to find jobs: {err}')

        except BaseException as err:
            raise Exception(f'Failed to while crawling: {err}')

    def apply_to_jobs(self):

        if len(self.jobs) == 0:
            raise Exception("There are no jobs to apply for.")
        
        self.driver = initialize_driver()
        handler = Handler(bot=self)

        for job in self.jobs:
            # Initialie a new parser for every new job. The parser will keep program state for the fields.
            parser = Parser(questions=self.questions, data=self.data, driver=self.driver)
            try:
                if job.get('apply') is not None:
                    self.driver.get(job.get('apply'))
                    handler.handle_job(job=job, parser=parser)
            except BaseException as err:
                print("err: ", err)
                continue

    def save_jobs(self):
        rows = get_values(os.environ.get('SHEETS_ID'), f"{os.environ.get('JOBS_TAB')}!A:F")
        headers = rows[0]

        jobs = []
        for first_index, job in enumerate(self.jobs):
            exists = False
            job_data = []
            for header in headers:
                job_data.append(job[header])
        
            # Find if job exists already
            for second_index, diff_job in enumerate(self.jobs):

                # If the links match, and it's not the same index in the list
                if job.get('apply') == diff_job.get('apply') and first_index != second_index:
                    exists = True

            if not exists:
                jobs.append(job_data)

            exists = False
        rows += jobs

        write_values(spreadsheet_id=os.environ.get('SHEETS_ID'), range=f"{os.environ.get('JOBS_TAB')}!A:F", values=rows)

    def get_jobs_from_sheets(self):
        rows = get_values(spreadsheet_id=os.environ.get('SHEETS_ID'), range=f"{os.environ.get('JOBS_TAB')}!A:F")
        headers = rows[0]

        for job in rows[1:]:
            job_data = {}
            for index, data in enumerate(job):
                job_data[headers[index]] = data

            self.jobs.append(job_data)

    def get_keywords(self):
        rows = get_values(spreadsheet_id=os.environ.get('SHEETS_ID'), range=f"{os.environ.get('KEYWORDS_TAB')}!A:A")
        for keyword in rows[1:]:
            self.keywords.append(keyword[0])

    def mark_applied(self, job):
        rows = get_values(os.environ.get('SHEETS_ID'), f"{os.environ.get('JOBS_TAB')}!A:F")

        if job is None:
            raise Exception("No job passed as parameter.")
        
        jobs_to_save = []
        for this_job in self.jobs:
            if this_job.get('apply') == job.get('apply'):
                this_job['applied'] == True
            
            job_data = []
            for header in rows[0]:
                job_data.append(this_job[header])
            
            jobs_to_save.append(job_data)
        
        rows = jobs_to_save
        write_values(spreadsheet_id=os.environ.get('SHEETS_ID'), range=f"{os.environ.get('JOBS_TAB')}!A:F", values=rows)