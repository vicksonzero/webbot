import os
import time
from selenium import webdriver

chromedriver = "C:\Python35-32\chromedriver"
#os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)

driver.get('http://www.google.com/xhtml');
time.sleep(5) # Let the user actually see something!
search_box = driver.find_element_by_id('gs_lc0')
search_box = search_box.find_element_by_css_selector(".gsfi");
print(search_box);
search_box.send_keys('ChromeDriver')
search_box.submit()
time.sleep(5) # Let the user actually see something!
driver.quit()
