from selenium.webdriver.common.by import By
from handle_fields import enter_fields
from sites.bamboo import bamboo
from sites.underdog import underdog
from sites.lever import lever
from sites.smartrecruiters import smartrecruiters, upload_smartrecruiters_resume
from sites.greenhouse import greenhouse
from sites.workdayjobs import handle_workdayjobs
from utils import click_preapplication_button

def site_router(driver, data, values):
    if "workdayjobs" in data['url']:
        handle_workdayjobs(driver, data)
        return

    if "bamboohr" in data['url']:
        click_preapplication_button(driver)
        bamboo(driver=driver, data=data)

    if "smartrecruiters" in data['url']:
        upload_smartrecruiters_resume(driver=driver)

    try:
        if "greenhouse" in data['url']:
            greenhouse(driver=driver, data=data, values=values)
        elif "smartrecruiters" in data['url']:
            smartrecruiters(driver=driver, data=data, values=values)
        elif "lever" in data['url']:
            lever(driver=driver, data=data, values=values)
        elif "underdog.io" in data['url']:
            underdog(driver=driver, data=data, values=values)
        else:
            enter_fields(driver, values, data)
    except BaseException:
       pass