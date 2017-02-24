from bs4 import BeautifulSoup
#import requests
import os.path
import json
from selenium import webdriver
import time

company = 'Amazon'
htmlFile = 'temp/' + company + " html.txt"
baseurl = "https://www.amazon.jobs"
url = baseurl + "/en/search?base_query=portland&loc_query=&job_count=100&result_limit=100&sort=relevant&cache"

# Write the raw data out, so we don't have to re-access the website every time
# This makes testing faster, since we don't have to re-access the website
# each time
if os.path.exists(htmlFile):
    # read the raw data
    with open(htmlFile, 'r') as file:
        data = file.read()

else:
     # access the website
    driver = webdriver.Firefox()
    driver.get(url)
    time.sleep(3)

    # Write the raw data
    os.makedirs(os.path.dirname(htmlFile), exist_ok=True)
    data = driver.page_source
    with open(htmlFile, 'w') as file:
        file.write(str(data.encode('UTF-8')))
        #file.write(data)
        #print(driver.find_element_by_id("content").text)
        driver.close()

# Make the soup
soup = BeautifulSoup(data, "html.parser")
#print(str(data.encode('UTF-8')))

#for link in soup.find_all('td', class_="job-title"):
#    print(link.find_next('a').contents[0])

# tableBody = soup.find('section')
#start = soup.find(attrs={"data-action" : "mail"})
#applicationLink = start.contents[0]

#print(applicationLink)

jobs = []
#count = 0
start = soup.find('div', attrs={"id" : "search-results"})
for link in start.find_all('a'):
    # Application Link
    applicationLink = link.get('href')
    applicationLink = baseurl + applicationLink
#    print (applicationLink)

    # Parse the Job Title
    jobTitle = link.find('h2', class_ = 'job-title').contents[0]
#    print(jobTitle)

    # Job ID|Location
    jobIDLoc = link.find('span').contents[0]
    (location, jobID) = jobIDLoc.split("|")
    location = location.strip()
    jobID = jobID.strip()
#    print (location)
#    print (jobID)

    # Date Posted
    datePosted = link.find('h2', class_ = "posting-date").contents[0]
#    print (datePosted)

     # Build an individual job
    job = {'ApplicationLink': applicationLink,
            'Company': company,
            'DatePosted': datePosted,
            'Experience': '',
            'Hours': '',
            'JobID': jobID,
            'JobTitle': jobTitle,
            'LanguagesUsed' : '',
            'Location' : location,
            'Salary' : '',
     }

    # put all the jobs into an array, so JSON dumps correctly
    #  print(sorted(job.items()))
    #
    # put all the jobs into an array, so JSON dumps correctly
    jobs.append(job)

#
# Print the json
with open(company + '.json', 'w') as outfile:
    json.dump(jobs, outfile)