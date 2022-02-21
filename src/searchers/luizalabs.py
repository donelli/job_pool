
import json
from typing import List
from exceptions.unexpected_status_code import UnexpectedStatusCodeException
import helpers
import requests

from job import Job, Origin
from searcher import Searcher
from tagger import Tagger

class LuizaLabsSearcher(Searcher):

   companyName = 'Luiza Labs'
   baseUrl     = 'https://api-oportunidades.99jobs.com//v1/opportunities?&page=1'
   token       = 'KTrB5f12tdr23mhsGZ8E2gMIu4w3'
   
   def getCompanyName(self) -> str:
      return self.companyName

   def loadDetails(self, job: Job):
      pass

   def search(self) -> List[Job]:

      jobs = []

      headers = helpers.getRandomRequestHeaders()
      headers['authorization'] = 'Token token=' + self.token
      
      currentPage  = 1
      totalOfPages = 1

      tagger = Tagger()
      
      while currentPage <= totalOfPages:
         
         response = requests.get(self.baseUrl + str(currentPage), headers=headers)

         print(" - Loading page " + str(currentPage))
         
         if response.status_code != 200:
            raise UnexpectedStatusCodeException(response)
         
         data = json.loads(response.content)

         if currentPage == 1:
            totalOfPages = data['links']['total_pages']
         
         print("  - Found " + str(len(data['opportunities'])) + " jobs at this page")
         
         if len(data['opportunities']) == 0:
            print("---------------------------")
            print(response.content)
            print("---------------------------")
         
         for jobData in data['opportunities']:
            
            job = Job()
            job.name = jobData['title']
            job.workplace = '-'
            job.url = jobData['links']['subscription']
            job.company = self.companyName
            job.origin = Origin.LUIZA_LABS
            job.remote = 'yes'
            
            job.tags = list(set(tagger.generateTags(helpers.removeHtmlTags(jobData['responsability'])) + tagger.generateTags(helpers.removeHtmlTags(jobData['requirement']))))

            jobs.append(job)

         currentPage += 1
         helpers.waitRandom()
      
      return jobs

