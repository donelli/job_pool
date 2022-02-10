
from typing import List
from attr import attr
from bs4 import BeautifulSoup
import requests
from exceptions.unexpected_status_code import UnexpectedStatusCodeException
from exceptions.element_not_found import ElementNotFoundException
from job import Job, Origin
import helpers
from searcher import Searcher
from tagger import Tagger

class DockerSearcher(Searcher):
   
   companyName = 'Docker'
   apiurl      = 'https://recruitingbypaycor.com/career/CareerHomeSearch.action?clientId=8a7883c6708df1d40170a6df29950b39'

   def getCompanyName(self) -> str:
      return self.companyName

   def loadDetails(self, job: Job):
      
      response = requests.post(job.url, headers=helpers.getRandomRequestHeaders())
      
      if response.status_code != 200:
         raise UnexpectedStatusCodeException(response)
      
      html = response.content
      soup = BeautifulSoup(html, 'html.parser')

      mainElem = soup.find('td', attrs={'id': 'gnewtonJobDescriptionText'})
      
      if not mainElem:
         raise ElementNotFoundException("td", id="gnewtonJobDescriptionText")

      tagger = Tagger()

      for li in mainElem.find_all('li'):
         
         text = li.get_text()

         if "Freedom & flexibility" in text:
            break

         for tag in tagger.generateTags(text):
            if tag not in job.tags:
               job.tags.append(tag)
         

   def search(self) -> List[Job]:

      jobs = []
      
      response = requests.post(self.apiurl, headers=helpers.getRandomRequestHeaders(), data = {
        "departmentId": "8a7883c6708df1d40170a6ed456f0c0a"
      })
      
      if response.status_code != 200:
         raise UnexpectedStatusCodeException(response)
      
      html = response.content
      soup = BeautifulSoup(html, 'html.parser')

      mainTable = soup.find("table", attrs={ "id": "gnewtonCareerHome" })

      if not mainTable:
         raise ElementNotFoundException("table", id="gnewtonCareerHome")
      
      trs = mainTable.find_all("tr")

      if len(trs) < 3:
         raise ElementNotFoundException("tr[3]", id="gnewtonCareerHome")

      tr = trs[3]
      
      for row in tr.find_all('tr'):

         jobLink = row.find('td', attrs={ 'class': 'gnewtonJobLink' })
         jobLoc  = row.find('td', attrs={ 'class': 'gnewtonJobLocation' })

         if not jobLink and not jobLoc:
            continue

         if (jobLink is None and jobLoc is not None) or (jobLink is not None and jobLoc is None):
            raise ElementNotFoundException("td", class_="gnewtonJobLink/gnewtonJobLocation")

         aElem = jobLink.find('a')

         if not aElem:
            raise ElementNotFoundException("td->a", class_="gnewtonJobLink")
         
         location = helpers.removeSpacesAndNewLines(jobLoc.get_text())
         url = aElem['href']
         name = helpers.removeSpacesAndNewLines(jobLink.get_text())

         if not "Brazil" in location and not "Brasil" in location:
            continue

         job = Job()
         job.name = name
         job.workplace = 'Brazil'
         job.department = 'Engineering'
         job.url = url
         job.company = self.companyName
         job.origin = Origin.DOCKER
         job.remote = 'yes'
         job.tags = []

         jobs.append(job)

      return jobs
