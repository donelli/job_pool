
# https://jobsapi-internal.m-cloud.io/api/stjobbulk?organization=2242&limitkey=4A8B5EF8-AA98-4A8B-907D-C21723FE4C6B&facet=publish_to_cws:true&fields=ref,title,primary_city,primary_state,primary_country,primary_category,level,url,sub_category,addtnl_locations,brand

import json
from typing import List
from job import Job, Origin
import requests
import helpers
from bs4 import BeautifulSoup
from tagger import Tagger

class IbmSearcher():

   jobs: List[Job] = []
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

   def loadTags(self, job: Job):
      
      helpers.waitRandom()
      
      request = requests.get(job.url)
      html = request.content
      soup = BeautifulSoup(html, 'html.parser')
      
      description = soup.find('div', {'class': 'jd-description'})
      
      if not description:
         print("Não encontrou a descrição")
         return
      
      content = helpers.removeSpacesAndNewLines(helpers.removeHtmlTags(" ".join(str(tag) for tag in description.contents)))
      
      job.tags = Tagger().generateTags(content)
      
      helpers.waitRandom()
   
   def search(self):
      
      print("Buscando empregos da empresa IBM...")
      
      request = requests.get(self.apiUrl)
      data = json.loads(request.content)
      
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
         
         self.jobs.append(job)

         if result['primary_category'] not in categories:
            categories[result['primary_category']] = 1
         else:
            categories[result['primary_category']] += 1

      helpers.waitRandom()


if __name__ == "__main__":
   searcher = IbmSearcher()
   
   job = Job()
   job.url = 'https://careers.ibm.com/job/14950066/data-engineer-bi-hortol-ndia-br/?codes=IBM_CareerWebSite'

   searcher.loadTags(job)

   print(job)
   
