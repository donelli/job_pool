from typing import List
from bs4 import BeautifulSoup
import bs4
import requests
from exceptions.unexpected_status_code import UnexpectedStatusCodeException
from job import Job, Origin
import helpers
from searcher import Searcher
from tagger import Tagger

class NubankSearcher(Searcher):
   
   companyName = 'Nubank'
   baseUrl     = 'https://boards.greenhouse.io/nubank'

   categoriesToExclude = [
      'Capital Markets',
      'Compliance',
      'Controllership',
      'FP&A',
      'Legal',
      'Marketing Insights & Analytics',
      'People',
      'Product Manager',
      'Public Policy',
      'Regulatory Operations',
      'Risk Management',
      'Xpeer'
   ]

   def getCompanyName(self) -> str:
      return self.companyName

   def loadDetails(self, job: Job):
         
      response = requests.get(job.url, headers=helpers.getRandomRequestHeaders())
      
      if response.status_code != 200:
         raise UnexpectedStatusCodeException(response)
      
      html = response.content
      soup = BeautifulSoup(html, 'html.parser')
      
      jobDescription = soup.find('div', { 'id': 'content' })
      
      if jobDescription is None:
         print("Nao tem conteudo: " + job.url)
         return
      
      tags: List[str] = []
      
      lisElem = jobDescription.find_all('li')
      
      for element in lisElem:
         
         content = ""
         
         if type(element) is bs4.element.Tag:
            content = element.get_text()
         else:
            content = str(element)

         content = content.strip()

         if content == "":
            continue

         newTags = Tagger().generateTags(helpers.removeHtmlTags(content))
         
         for tag in newTags:
            if tag not in tags:
               tags.append(tag)

      job.tags = tags

   def search(self) -> List[Job]:

      jobs = []
      
      response = requests.get(self.baseUrl, headers=helpers.getRandomRequestHeaders())
      
      if response.status_code != 200:
         raise UnexpectedStatusCodeException(response)
      
      html = response.content
      soup = BeautifulSoup(html, 'html.parser')
      
      categoryDivs = soup.find_all('section', attrs={ 'class': 'level-0' })
      
      for categoryDiv in categoryDivs:
         
         categoryName = categoryDiv.find('h2').get_text()

         if categoryName in self.categoriesToExclude:
            continue
         
         jobDivs = categoryDiv.find_all('div', attrs={ 'class': 'opening' })
         
         for jobDiv in jobDivs:
         
            jobUrl = jobDiv.find('a')['href']
            barPos = jobUrl.index('/', 1)
            
            link = self.baseUrl + jobUrl[barPos:]
            workplace = jobDiv.find('span', attrs={ 'class': 'location' }).encode_contents().decode("utf-8")
            name = jobDiv.find('a').encode_contents().decode("utf-8")
            
            job = Job()
            job.name = name
            job.workplace = workplace
            job.url = link
            job.company = self.companyName
            job.origin = Origin.NUBANK
            job.remote = '-'

            jobs.append(job)

      return jobs