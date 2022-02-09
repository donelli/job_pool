import json
from typing import List
from bs4 import BeautifulSoup
import requests
from exceptions.unexpected_status_code import UnexpectedStatusCodeException
from job import Job, Origin
import helpers
from searcher import Searcher
from tagger import Tagger

class TractianSearcher(Searcher):

   url = 'https://tractian.com/carreiras/vagas'
   companyName = 'Tractian'

   departmentsToIgnore = [
      'People', 'Sales', 'Finance', 'Customer', 'Marketing', 'Hardware'
   ]

   def loadDetails(self, job: Job) -> None:
      pass

   def getCompanyName(self) -> str:
      return self.companyName
   
   def search(self) -> List[Job]:

      jobs = []

      response = requests.get(self.url, headers=helpers.getRandomRequestHeaders())
      
      if response.status_code != 200:
         raise UnexpectedStatusCodeException(response)
      
      html = response.content
      soup = BeautifulSoup(html, 'html.parser')

      nextDataStr = soup.find('script', id="__NEXT_DATA__").decode_contents()

      nextData = json.loads(nextDataStr)

      tagger = Tagger()
      
      for departData in nextData['props']['pageProps']['list']:

         departName = departData['department']

         if departName in self.departmentsToIgnore:
            continue

         for jobData in departData['jobs']:

            workplace = jobData['fields']['place']

            job = Job()
            job.company = self.companyName
            job.department = departName
            job.name = jobData['fields']['name']
            job.remote = "yes" if "REMOTE" in workplace.upper() else "no"
            job.url = self.url + '/' + jobData['id']
            job.workplace = workplace
            job.type = ''
            job.origin = Origin.TRACTIAN
            
            job.tags = tagger.generateTags(jobData['fields']['requirements'])
            job.differentialTags = tagger.generateTags(jobData['fields']['extra'])
            
            jobs.append(job)

      return jobs