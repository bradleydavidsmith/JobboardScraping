from selenium import webdriver
import os.path
import time
from bs4 import BeautifulSoup

#driver = webdriver.PhantomJS(executable_path='')

htmlFile = 'temp/' + 'ajexDemo' + " html.txt"

if os.path.exists(htmlFile):
    # read the raw data
    with open(htmlFile, 'r') as file:
        data = file.read()
else:
    driver = webdriver.Firefox()
    driver.get("http://pythonscraping.com/pages/javascript/ajaxDemo.html")
    time.sleep(3)

    # Write the raw data
    os.makedirs(os.path.dirname(htmlFile), exist_ok=True)
    data = driver.page_source
    with open(htmlFile, 'w') as file:
        #file.write(str(data.encode('UTF-8')))
        file.write(data)
        print(driver.find_element_by_id("content").text)
        driver.close()

soup = BeautifulSoup(data, "html.parser")
print(soup.find('div').contents[0])