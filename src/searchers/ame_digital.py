from typing import List
from bs4 import BeautifulSoup
import bs4
import requests
from exceptions.unexpected_status_code import UnexpectedStatusCodeException
from job import Job, Origin
import helpers
from searcher import Searcher
from tagger import Tagger

class AmeDigitalSearcher(Searcher):
   
   companyName = 'Ame Digital'
   baseUrl     = 'https://boards.greenhouse.io/amedigital'

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
            return
         
         tags: List[str] = []
         differentialTags: List[str] = []
         foundDifferentials = False
         
         for element in jobDescription:
            
            content = ""
            
            if type(element) is bs4.element.Tag:
               content = element.get_text()
            else:
               content = str(element)

            content = content.strip()

            if content == "":
               continue

            if "e outros ;)" in content:
               continue

            if len(content) < 25 and "diferenciais" in content.lower():
               foundDifferentials = True
               continue

            if foundDifferentials:
               
               if content == "Conhecimento/Experiência em:":
                  continue
               
               differentialTags = Tagger().generateTags(helpers.removeHtmlTags(content))
               foundDifferentials = False
               continue
            
            newTags = Tagger().generateTags(helpers.removeHtmlTags(content))
            
            for tag in newTags:
               if tag not in tags:
                  tags.append(tag)

         job.tags = tags
         job.differentialTags = differentialTags

   def search(self) -> List[Job]:
      
      jobs = []
      response = requests.get(self.baseUrl, headers=helpers.getRandomRequestHeaders())

      if response.status_code != 200:
         raise UnexpectedStatusCodeException(response)
      
      html = response.content
      soup = BeautifulSoup(html, 'html.parser')
      
      divs = soup.find_all('div', attrs={ 'class': 'opening' })
      
      for jobDiv in divs:
         
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
         job.origin = Origin.AME_DIGITAL

         job.remote = 'no'
         if "remote" in workplace.lower() or "remoto" in workplace.lower() or "remota" in workplace.lower():
            job.remote = 'yes'

         jobs.append(job)
         
      return jobs