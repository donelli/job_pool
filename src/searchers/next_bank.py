
import json
from typing import List
from bs4 import BeautifulSoup
import requests
from exceptions.unexpected_status_code import UnexpectedStatusCodeException
from job import Job, Origin
import helpers
import re
from searcher import Searcher

from tagger import Tagger

class NextBankSearcher(Searcher):

   apiUrl = 'https://us.api.csod.com/rec-job-search/external/jobs'
   apiBody = {
      "careerSiteId": 10,
      "careerSitePageId": 10,
      "pageNumber": 1,
      "pageSize": 500,
      "cultureId": 12,
      "searchText": "",
      "cultureName": "pt-BR",
      "states": [],
      "countryCodes": [], 
      "cities": [],
      "placeID": "",
      "customFieldCheckboxKeys": [],
      "customFieldDropdowns": [],
      "customFieldRadios": []
   }
   tokenPageUrl = 'https://bradesco.csod.com/ux/ats/careersite/10/home?c=bradesco'
   companyName = 'Banco Next'

   def getCompanyName(self) -> str:
      return self.companyName
   
   def loadDetails(self, job: Job):
      
      helpers.waitRandom()
      
      response = requests.get(job.url, headers=helpers.getRandomRequestHeaders())
      
      if response.status_code != 200:
         raise UnexpectedStatusCodeException(response)
      
      html = response.content
      soup = BeautifulSoup(html, 'html.parser')

      jsonData = soup.find("script", type="application/ld+json")

      data = json.loads(jsonData.string)
      
      description = helpers.removeHtmlTags(helpers.toOneLineString(data['Description']))

      if "O que o next te oferece?" in description:
         description = description[:description.index('O que o next te oferece?')] + ' '
      
      job.tags = Tagger().generateTags(description)

   def search(self):
      
      jobs = []

      self.headers = helpers.getRandomRequestHeaders()
      
      response = requests.get(self.tokenPageUrl, headers=self.headers)

      if response.status_code != 200:
         raise UnexpectedStatusCodeException(response)
      
      tokens = re.findall(r'(?<=token":").*?(?=")', response.content.decode('utf-8'))

      if len(tokens) != 1:
         print("Token nao encontrado!")
         return

      self.headers['Authorization'] = 'Bearer ' + tokens[0]
      self.headers['Accept'] = '*/*'
      
      response = requests.post(self.apiUrl, headers=self.headers, json=self.apiBody)

      if response.status_code != 200:
         raise UnexpectedStatusCodeException(response)
      
      resp = json.loads(response.content.decode('utf-8'))
      
      for jobData in resp['data']['requisitions']:
         
         workplace = ''
         for loc in jobData['locations']:
            
            if workplace != '':
               workplace += '\n'
            
            if 'city' in loc:
               workplace += (loc['city'] + ', ' + loc['state'] + '-' + loc['country'])
            else:
               workplace += loc['country']
         
         job = Job()
         job.name = helpers.capitalizeWords(jobData['displayJobTitle'])
         job.workplace = workplace
         job.url = 'https://bradesco.csod.com/ux/ats/careersite/10/home/requisition/' + str(jobData['requisitionId']) + '?c=bradesco'
         job.company = self.companyName
         job.origin = Origin.NEXT
         job.remote = '-'

         jobs.append(job)

      return jobs
