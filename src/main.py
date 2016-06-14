import time
from selenium import webdriver

driver = webdriver.Chrome("/c/Python35-32/chromedriver.exe")
time.sleep(5)
driver.quit()
