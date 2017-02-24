from bs4 import BeautifulSoup
import requests
import json

url = "itcareers.apexsystems.com/search?keywords=&facetcountry=US&location=Portland%2C+OR"
company = 'Apex Systems'

r  = requests.get("http://" +url)
try:
    r.raise_for_status()
except Exception as exc:
    print('There was a problem: %s' % (exc))

data = r.text

soup = BeautifulSoup(data, "html.parser")

#for link in soup.find_all('td', class_="job-title"):
#    print(link.find_next('a').contents[0])

# Example of HTML:
 # <tbody>
	# 	                        		                        <tr>
	# 		                        <td data-title="Job Title" class="job-title"><a href='http://itcareers.apexsystems.com/job/pc-tech-portland/J3J7VS78YXSXBZK69TD/'>PC Tech - Portland</a></td>
	# 		                        <td class="job-location" data-title="Location">Portland, OR</td>
	# 		                        <td class="job-posted" data-title="Date Posted">2/16/2017</td>
	# 	                        </tr>
	# 	                        		                        <tr>
	# 		                        <td data-title="Job Title" class="job-title"><a href='http://itcareers.apexsystems.com/job/sr-ios-engineer/J3G5PT5Z299213M8D13/'>Sr. iOS Engineer</a></td>
	# 		                        <td class="job-location" data-title="Location">Portland, OR</td>
	# 		                        <td class="job-posted" data-title="Date Posted">2/14/2017</td>
	# 	                        </tr>

tableBody = soup.find('tbody')
jobs = []
for link in tableBody.find_all('tr'):
    job = {}

    applicationLink = link.find_next('a').get('href')
    job['ApplicationLink'] = applicationLink

    job['Company'] = company

    datePosted = link.find_next('a').find_next('td').find_next('td').contents[0]
    datePosted = 'Date Posted: ' + datePosted
    job['DatePosted'] = datePosted
    # print(datePosted)

    job['Experience'] = ''

    job['Hours'] = ''

    job['JobID'] = ''

    # Job Title
    jobTitle = link.find_next('a').contents[0]
    # print(jobTitle)
    job['JobTitle'] = jobTitle

    job['LanguagesUsed'] = ''

    # Location
    location = link.find_next('a').find_next('td').contents[0]
    location = 'Location: ' + location
    job['Location'] = location

    job['Salary'] = ''

#    print()
#    print(sorted(job.items()))
#    print()
    jobs.append(job)

with open(company + '.json', 'w') as outfile:
    json.dump(jobs, outfile)

