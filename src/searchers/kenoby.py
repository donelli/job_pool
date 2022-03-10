
from typing import List
from bs4 import BeautifulSoup
import requests
from exceptions.element_not_found import ElementNotFoundException
from exceptions.unexpected_status_code import UnexpectedStatusCodeException
from job import Job, Origin
import helpers
from searcher import Searcher

from tagger import Tagger

class KenobySearcher(Searcher):

   differentialsStrs = helpers.getDifferentialStrs()

   def getCompanyName(self) -> str:
      return 'Kenoby'

   def loadDetails(self, job: Job) -> None:
      
      response = requests.get(job.url, headers=helpers.getRandomRequestHeaders())
      
      if response.status_code != 200:
         raise UnexpectedStatusCodeException(response)
         
      html = response.content
      soup = BeautifulSoup(html, 'html.parser')

      descriptionDiv = soup.find('div', attrs={ "class": "description" })

      if not descriptionDiv:
         raise ElementNotFoundException('div', class_='description')

      text = descriptionDiv.get_text(separator=" ")
      upperText = text.upper()
      differTags: List[str] = []
      
      for startStr in self.differentialsStrs:

         upperStr = startStr.upper()
         
         if upperText.count(upperStr) != 1:
            continue
         
         pos = upperText.find(upperStr)
         differTags = Tagger().generateTags(text[pos:])
         text = text[:pos].strip()
         
         break

      job.tags = Tagger().generateTags(text)
      job.differentialTags = [ tag for tag in differTags if tag not in job.tags ]
   
   def search(self):
      pass

   def searchWithParams(self, companyName: str, htmlUrl: str, segmentsToFilter: List[str], onlyRemote: bool) -> List[Job]:
      
      jobs: List[Job] = []
      response = requests.get(htmlUrl, headers=helpers.getRandomRequestHeaders())
      
      if response.status_code != 200:
         raise UnexpectedStatusCodeException(response)
         
      html = response.content
      soup = BeautifulSoup(html, 'html.parser')

      # Ensure that the content is correctly loaded
      if not soup.find('div', attrs={ 'id': 'content' }):
         raise ElementNotFoundException('div', id='content')
      
      segmentDivs = soup.find_all('div', attrs={ "class": "segment" })
      
      for segmentDiv in segmentDivs:
         
         segmentName = segmentDiv['data-segment']
         
         if segmentName not in segmentsToFilter:
            continue

         positionsDiv = segmentDiv.find("div", attrs={ 'class': 'positions' })

         if not positionsDiv:
            raise ElementNotFoundException('div', class_='positions')

         containerDiv = positionsDiv.find("div", attrs={ 'class': 'container' })

         if not containerDiv:
            raise ElementNotFoundException('div', class_='container')

         for jobAElem in containerDiv.find_all('a'):

            workplace =  helpers.toOneLineString(jobAElem.find('span', attrs={ 'class': 'location' }).getText())
            remote = False

            if "HOME OFFICE" in workplace.upper() or "REMOTO" in workplace.upper() or "REMOTE" in workplace.upper():
               remote = True

            if onlyRemote and not remote:
               continue
            
            job = Job()
            job.name = jobAElem['data-title'].strip()
            job.url = jobAElem['href']
            job.workplace = workplace
            job.department = segmentName
            job.remote = 'yes' if remote else 'no'
            job.company = companyName
            job.origin = Origin.KENOBY
         
            jobs.append(job)
      
      return jobs
