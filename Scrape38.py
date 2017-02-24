from bs4 import BeautifulSoup
import requests
import os.path
import json

company = 'AltSource'
htmlFile = 'temp/' + company + " html.txt"
baseurl = "https://careers.jobscore.com"
url = baseurl + "/careers/altsrc"

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
# start = soup.find(attrs={"data-action" : "mail"})
# applicationLink = start.contents[0]
#
# print(applicationLink)


jobs = []
for link in soup.find_all('div', class_ = "js-job-container"):

    jobTitle = ''
    # Find the Job Title
    jobTitle = link.find_next('a').contents[0]
    location = link.find_next('span', class_ = "js-job-location").contents[0].strip()

    # Find the Application Link
    applicationLink = link.find_next('a').get('href')
    applicationLink = baseurl + applicationLink

    # Build an individual job
    job = {'ApplicationLink': applicationLink,
           'Company': company,
           'DatePosted': '',
           'Experience': '',
           'Hours': '',
           'JobID': '',
           'JobTitle': jobTitle,
           'LanguagesUsed' : '',
           'Location' : location,
           'Salary' : '',
    }

    # put all the jobs into an array, so JSON dumps correctly
    # print(sorted(job.items()))

    jobs.append(job)



# Print the json
with open(company + '.json', 'w') as outfile:
     json.dump(jobs, outfile)

