class Handler:
    def __init__(self, driver, data):
        self.driver = driver
        self.data = data
    
    def handle_job(self, job):
        if "workdayjobs" in job['apply']:
            self.handle_workdayjobs(driver=self.driver, data=self.data)
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