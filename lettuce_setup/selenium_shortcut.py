'''
Created on Apr 10, 2014

@author: eastagile
'''
from lettuce import world, after
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement


def browser():
    '''
    @return: selenium.webdriver.Firefox
    '''
    if not hasattr(world, 'browser'):
        world.browser = webdriver.Firefox()
        world.browser.maximize_window()
        world.browser.implicitly_wait(3)
    return world.browser


@after.each_scenario
def close_browser(scenario):
    if hasattr(world, 'browser'):
        world.browser.quit()
        del world.browser


def find_all(selector):
    return browser().find_elements_by_css_selector(selector)


def find(selector):
    return browser().find_element_by_css_selector(selector)


def xpath(selector):
    return browser().find_element_by_xpath(selector)


WebElement.find = WebElement.find_element_by_css_selector
WebElement.find_all = WebElement.find_elements_by_css_selector
WebElement.xpath = WebElement.find_element_by_xpath


def select(self, value):
    self.xpath("./option[text()='%s']" % value).click()


WebElement.select = select
