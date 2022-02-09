

import json
from typing import List
from bs4 import BeautifulSoup
import helpers
import requests
from job import Job, Origin
from searcher import Searcher
from tagger import Tagger

class NetflixSearcher(Searcher):

   companyName = 'Netflix'
   
   loadedIds: List[str] = []
   apiUrl = "https://jobs.netflix.com/api/search"
   
   locations = [
      ('Remote, United States', 'yes'),
      ('Alphaville, Brazil', '-')
   ]
   
   teams = [
      "Client and UI Engineering",
      "Content Engineering",
      "Core Engineering",
      "Data Science and Engineering",
      "Design",
      "Security",
      "Information Security",
      "Infrastructure and Tooling",
      "Netflix Technology Services",
      "Partner Ecosystem Engineering",
      "Product Management"
   ]

   def getCompanyName(self) -> str:
      return self.companyName

   def loadDetails(self, job: Job):
      pass

   def loadTags(self, html) -> List[str]:
      
      soup = BeautifulSoup(html, 'html.parser')
      jobTags: List[str] = []
      
      for div in soup:
         
         tags = Tagger().generateTags(helpers.removeHtmlTags(div.get_text()))
         
         for tag in tags:
            if tag not in jobTags:
               jobTags.append(tag)
      
      return jobTags
   
   def search(self) -> List[Job]:
      
      jobs = []
      
      for location in self.locations:
      
         helpers.waitRandom()
      
         page = 1
         
         while True:
            
            url = self.apiUrl + '?location=' + location[0] + '&page=' + str(page)
            
            # print(" -> " + url)
            
            response = requests.get(url, headers=helpers.getRandomRequestHeaders())
            
            data = json.loads(response.content)

            if data['record_count'] == 0:
               break
            
            for jobData in data['records']['postings']:
               
               if jobData['external_id'] in self.loadedIds:
                  continue
               
               hasTeam = False
               for team in self.teams:
                  if 'team' in jobData and team in jobData['team']:
                     hasTeam = True
                     break
                  elif 'lever_team' in jobData and team == jobData['lever_team']:
                     hasTeam = True
                     break
               
               if not hasTeam:
                  continue
               
               self.loadedIds.append(jobData['external_id'])

               job = Job()
               job.company = self.companyName
               job.name = jobData['text']
               job.department = jobData['lever_team']
               job.remote = location[1]
               job.url = 'https://jobs.netflix.com/jobs/' + jobData['external_id']
               job.workplace = jobData['location']
               job.origin = Origin.NETFLIX
               
               job.tags = self.loadTags(jobData['description'])
               
               jobs.append(job)
            
            page += 1
      
      return jobs