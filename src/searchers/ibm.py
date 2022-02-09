
# https://jobsapi-internal.m-cloud.io/api/stjobbulk?organization=2242&limitkey=4A8B5EF8-AA98-4A8B-907D-C21723FE4C6B&facet=publish_to_cws:true&fields=ref,title,primary_city,primary_state,primary_country,primary_category,level,url,sub_category,addtnl_locations,brand

import json
from typing import List
from exceptions.unexpected_status_code import UnexpectedStatusCodeException
from job import Job, Origin
import requests
import helpers
from bs4 import BeautifulSoup
from searcher import Searcher
from tagger import Tagger

class IbmSearcher(Searcher):

   apiUrl = 'https://jobsapi-internal.m-cloud.io/api/stjobbulk?organization=2242&limitkey=4A8B5EF8-AA98-4A8B-907D-C21723FE4C6B&facet=publish_to_cws:true&fields=title,primary_city,primary_state,primary_country,primary_category,url,level'
      
   categoriesToIgnore = [
      'Consultant',
      'Project Management',
      'Sales',
      'Marketing',
      'Human Resources',
      'Finance',
      'Supply Chain',
      'Hardware Development & Support',
      'Research',
      'Services Solutions Management',
      'Communications',
      'Offering Management',
      'Project Executive',
      'Manufacturing',
      'General Management',
      'Enterprise Operations'
   ]

   def getCompanyName(self) -> str:
      return 'IBM'

   def loadDetails(self, job: Job):
      
      helpers.waitRandom()
      
      response = requests.get(job.url, headers=helpers.getRandomRequestHeaders())
      
      if response.status_code != 200:
         raise UnexpectedStatusCodeException(response)

      html = response.content
      soup = BeautifulSoup(html, 'html.parser')
      
      description = soup.find('div', {'class': 'jd-description'})
      
      if not description:
         return
      
      content = helpers.removeHtmlTags(" ".join(str(tag) for tag in description.contents))
      
      job.tags = Tagger().generateTags(content)
      
      helpers.waitRandom()
   
   def search(self) -> List[Job]:

      jobs = []
      
      response = requests.get(self.apiUrl, headers=helpers.getRandomRequestHeaders())

      if response.status_code != 200:
         raise UnexpectedStatusCodeException(response)

      data = json.loads(response.content)
      
      categories = {}
      
      for result in data['queryResult']:

         if result['level'] == 'Intern':
            continue

         if result['primary_category'] in self.categoriesToIgnore:
            continue
         
         if result['primary_category'] == 'Architect' and "developer" not in result['title'].lower():
            continue
         
         if 'Operations Desk' in result['title']:
            continue

         company = "IBM"
         
         isRemote = result['url'].endswith("-remote/")
         
         if result['primary_country'] == "BR":
            company = "IBM - Brazil"
         # elif isRemote:
            
         #    if result['primary_country'] == "US":
         #       company = "IBM - US"
         #    elif result['primary_country'] == "AU":
         #       company = "IBM - Australia"
         #    elif result['primary_country'] == "CA":
         #       company = "IBM - Canada"
         #    else:
         #       continue
            
         else:
            continue
         
         if isRemote:
            company = company + " Remote"
         
         job = Job()
         job.company = company
         job.department = result['primary_category']
         job.name = result['title']
         job.remote = ('yes' if isRemote else 'no')
         job.url = result['url']
         job.workplace = result['primary_city'] + ' - ' + result['primary_state']
         job.type = ''
         job.tags = []
         job.origin = Origin.IBM
         
         jobs.append(job)

         if result['primary_category'] not in categories:
            categories[result['primary_category']] = 1
         else:
            categories[result['primary_category']] += 1

      return jobs

