
from typing import List
from exceptions.unexpected_status_code import UnexpectedStatusCodeException
from job import Job, Origin
import requests
import helpers
from bs4 import BeautifulSoup
from searcher import Searcher
from tagger import Tagger

class PaypalSearcher(Searcher):

   baseUrl = 'https://jobsearch.paypal-corp.com/en-US/search?facetcountry=br&facetcategory='
   categories = [
      'solutions engineering',
      'integration engineering',
      'technical support engineering'
   ]

   companyName = 'PayPal'

   def getCompanyName(self) -> str:
      return self.companyName
   
   def loadDetails(self, job: Job):
         
      response = requests.get(job.url, headers=helpers.getRandomRequestHeaders())
      
      if response.status_code != 200:
         raise UnexpectedStatusCodeException(response)
      
      html = response.content
      soup = BeautifulSoup(html, 'html.parser')
      
      jobDescription = soup.find('div', { 'class': 'jdp-job-description-card' })
      
      if jobDescription is None:
         print("Nao tem conteudo: " + job.url)
         return
      
      tagger = Tagger()
      tags: List[str] = []
      
      elements = []
      elements.extend([el for el in jobDescription.find_all('li')])
      elements.extend([el for el in jobDescription.find_all('p')])
      
      for el in elements:

         text = helpers.removeSpacesAndNewLines(helpers.removeHtmlTags(el.get_text()))

         elementTags = tagger.generateTags(text)

         for tag in elementTags:
            if tag not in tags:
               tags.append(tag)
      
      job.tags = tags
      
   def search(self):

      jobs = []
      
      for category in self.categories:

         print("-> category: " + category + "...")
         
         url = self.baseUrl + category
         
         response = requests.get(url, headers=helpers.getRandomRequestHeaders())
         
         if response.status_code != 200:
            raise UnexpectedStatusCodeException(response)
         
         html = response.content
         soup = BeautifulSoup(html, 'html.parser')

         for jobTr in soup.find_all('tr', class_="job-result"):

            aElem = jobTr.find('a')
            
            job = Job()
            job.company = self.companyName
            job.department = category
            job.name = helpers.removeSpacesAndNewLines(aElem.get_text())
            job.remote = '-'
            job.url = 'https://jobsearch.paypal-corp.com' + aElem['href']
            job.workplace = helpers.removeSpacesAndNewLines(jobTr.find('td', class_="job-result-location-cell").get_text())
            job.type = ''
            job.tags = []
            job.origin = Origin.PAYPAL
            
            jobs.append(job)
         
         helpers.waitRandom()
         
      return jobs
