from bs4 import BeautifulSoup
import requests
import os.path
import json

company = 'Apex Clearing'
htmlFile = 'temp/' + company + " html.txt"
baseurl = "https://boards.greenhouse.io"
url = baseurl + "/apex#.WKuY6H9aGio"

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
jobs = []
for link in soup.find_all('section'):
    for link2 in link.find_all('div'):
        # Build an individual job
        job = {}

        applicationLink = link2.find_next('a').get('href')
        applicationLink = baseurl + applicationLink
        #print (applicationLink)
        job['ApplicationLink'] = applicationLink

        job['Company'] = company

        job['DatePosted'] = ''

        job['Experience'] = ''

        job['Hours'] = ''

        job['JobID'] = ''

        jobTitle = link2.find_next('a').contents[0]
        #print (jobTitle)
        job['JobTitle'] = jobTitle

        job['LanguagesUsed'] = ''

        location = link2.find_next('span').contents[0]
        #print (location)
        job['Location'] = location

        job['Salary'] = ''

        # put all the jobs into an array, so JSON dumps correctly
        print(sorted(job.items()))

        jobs.append(job)

# Print the json
with open(company + '.json', 'w') as outfile:
     json.dump(jobs, outfile)

