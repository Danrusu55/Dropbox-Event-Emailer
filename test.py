import selenium
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

firefox_capabilities = DesiredCapabilities.FIREFOX
firefox_capabilities['marionette'] = True

driver = webdriver.Firefox(capabilities=firefox_capabilities)
driver.get('http://google.com')
