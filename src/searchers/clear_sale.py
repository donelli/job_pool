import json
from typing import List
from bs4 import BeautifulSoup
import bs4
import requests
from exceptions.unexpected_status_code import UnexpectedStatusCodeException
from job import Job, Origin
import helpers
from searcher import Searcher
from tagger import Tagger

class ClearSaleSearcher(Searcher):
   
   companyName = 'Clear Sale'
   apiUrl     = 'https://clearsalebrapi.azurewebsites.net/api/JobVacancies'

   segmentsToConsider = [
      'IDLAB',
      'ANALYTICS',
      'DADOS',
      'EXPLORE',
      'TI',
      'ENG DE SOFTWARE - PRODUTOS'
   ]

   def getCompanyName(self) -> str:
      return self.companyName

   def loadDetails(self, job: Job):
      
      response = requests.get(job.url, headers=helpers.getRandomRequestHeaders())
      
      if response.status_code != 200:
         raise UnexpectedStatusCodeException(response)
         
      soup = BeautifulSoup(response.text, 'html.parser')
      
      jobDesc = soup.find("div", class_="description").get_text(separator=' ')
      
      if "QUAIS SERÃO AS SUAS RESPONSABILIDADES" in jobDesc:
         jobDesc = jobDesc[jobDesc.index("QUAIS SERÃO AS SUAS RESPONSABILIDADES"):]
      
      if "Benefícios Oferecidos:" in jobDesc:
         jobDesc = jobDesc[:jobDesc.index("Benefícios Oferecidos:")]
      
      differTags = []   
   
      if "Desejável:" in jobDesc:
         differTags = Tagger().generateTags(jobDesc[jobDesc.index("Desejável:"):])
         jobDesc = jobDesc[:jobDesc.index("Desejável:")]
      
      job.tags = Tagger().generateTags(jobDesc)

      job.differentialTags = [diff for diff in differTags if diff not in job.tags]
      
   def search(self) -> List[Job]:

      jobs = []
      
      response = requests.get(self.apiUrl, headers=helpers.getRandomRequestHeaders())
      
      if response.status_code != 200:
         raise UnexpectedStatusCodeException(response)
      
      data = json.loads(response.text)
      
      for jobData in data['Jobs']:
         
         if jobData['Segment'] not in self.segmentsToConsider:
            continue
         
         job = Job()
         job.name = jobData['Title']
         job.workplace = jobData['City']
         job.url = jobData['Link']
         job.company = self.companyName
         job.department = jobData['Segment']
         job.origin = Origin.NUBANK
         job.remote = 'yes'
         
         jobs.append(job)
         
      return jobs