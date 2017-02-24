from bs4 import BeautifulSoup
import requests
import os.path
import json

company = 'Angel Vision'
htmlFile = 'temp/' + company + " html.txt"
#baseurl = "https://boards.greenhouse.io"
url = "http://www.angelvisiontech.com/news/"

# Write the raw data out, so we don't have to re-access the website every time
# This makes testing faster, since we don't have to re-access the website
# each time
if os.path.exists(htmlFile):
    # read the raw data
    with open(htmlFile, 'r') as file:
        data = file.read()

else:
    # access the website
    r  = requests.get(url)
    try:
        r.raise_for_status()
    except Exception as exc:
        print('There was a problem: %s' % (exc))

    data = r.text

    # Write the raw data
    os.makedirs(os.path.dirname(htmlFile), exist_ok=True)
    with open(htmlFile, 'w') as file:
        file.write(data)

# Make the soup
soup = BeautifulSoup(data, "html.parser")

#for link in soup.find_all('td', class_="job-title"):
#    print(link.find_next('a').contents[0])

# tableBody = soup.find('section')
start = soup.find(attrs={"data-action" : "mail"})
applicationLink = start.contents[0]

print(applicationLink)

jobs = []
count = 0
for link in soup.find_all(attrs = { "style" : "font-size: 14px;"}):

    jobTitle = ''
    # Find the Job Title
    if count > 1:
        jobTitle = link.contents[0]
    elif (count == 1):
        jobTitle = link.find_next('a').contents[0]
    elif (count == 0):
        count+=1
        continue
    count+=1

    # Build an individual job
    job = {'ApplicationLink': applicationLink,
           'Company': company,
           'DatePosted': '',
           'Experience': '',
           'Hours': '',
           'JobID': '',
           'JobTitle': jobTitle,
           'LanguagesUsed' : '',
           'Location' : '',
           'Salary' : '',
    }

    # put all the jobs into an array, so JSON dumps correctly
    # print(sorted(job.items()))

    jobs.append(job)

# Print the json
with open(company + '.json', 'w') as outfile:
     json.dump(jobs, outfile)

