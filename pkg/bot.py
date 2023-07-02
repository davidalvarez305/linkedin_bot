from selenium import webdriver
import os
import json
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pkg.handler import Handler
from. helpers.sheets import get_values, write_values

from .sites.linkedin import extract_job_data, go_to_jobs_search

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
        
        self.driver = initialize_driver()
        handler = Handler(bot=self)

        for job in self.jobs:
            parser = Parser()
            try:
                if job.get('apply') is not None:
                    self.driver.get(job.get('apply'))
                    handler.handle_job(job=job, parser=parser)
            except BaseException as err:
                print("err: ", err)
                continue

    def save_jobs(self):
        rows = get_values(os.environ.get('SHEETS_ID'), f"{os.environ.get('JOBS_TAB')}!A:E")
        headers = rows[0]

        jobs = []
        for job in self.jobs:
            job_data = []
            for header in headers:
                job_data.append(job[header])

            jobs.append(job_data)
        rows += jobs

        write_values(spreadsheet_id=os.environ.get('SHEETS_ID'), range=f"{os.environ.get('JOBS_TAB')}!A:E", values=rows)

    def get_jobs_from_sheets(self):
        rows = get_values(spreadsheet_id=os.environ.get('SHEETS_ID'), range=f"{os.environ.get('JOBS_TAB')}!A:E")
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