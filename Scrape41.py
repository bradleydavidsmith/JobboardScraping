from bs4 import BeautifulSoup
import requests
import os.path
import json

company = 'Anitian'
htmlFile = 'temp/' + company + " html.txt"
url = "https://careers.smartrecruiters.com/Anitian/"

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

jobs = []

# find all the job titles
for link in soup.find_all('h3', class_ = "job-title"):
    jobTitle = link.contents[0]
    print (jobTitle)

        # Build an individual job dictionary
    job = {'ApplicationLink': '',
           'Company': '',
           'DatePosted': '',
           'Experience': '',
           'Hours': '',
           'JobID': '',
           'JobTitle': jobTitle,
           'LanguagesUsed' : '',
           'Location' : '',
           'Salary' : '',
    }

    # put each job into the jobs array, so JSON dumps correctly
    # print(sorted(job.items()))

    jobs.append(job)

# Print the json
with open(company + '.json', 'w') as outfile:
     json.dump(jobs, outfile)

