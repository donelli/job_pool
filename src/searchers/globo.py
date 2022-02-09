from typing import List
from bs4 import BeautifulSoup
import requests
from exceptions.element_not_found import ElementNotFoundException
from exceptions.unexpected_status_code import UnexpectedStatusCodeException
from job import Job, Origin
import helpers
from searcher import Searcher
from tagger import Tagger

class GloboSearcher(Searcher):
   
   companyName = 'Globo'
   baseUrl = 'https://vempraglobo.hire.trakstar.com/?q=&limit=1000'
   
   def getCompanyName(self) -> str:
      return self.companyName
   
   def loadDetails(self, job: Job):
      
      response = requests.get(job.url, headers=helpers.getRandomRequestHeaders())

      if response.status_code != 200:
         raise UnexpectedStatusCodeException(response)
      
      html = response.content
      soup = BeautifulSoup(html, 'html.parser')
      
      jobDescription = soup.find('div', attrs={ 'class': 'jobdesciption' })
      
      if jobDescription is None:
         raise ElementNotFoundException('div', class_='jobdesciption')
      
      job.tags = Tagger().generateTags(helpers.removeHtmlTags(jobDescription.encode_contents().decode("utf-8")))
   
   def search(self) -> List[Job]:
      
      jobs = []
      
      response = requests.get(self.baseUrl, headers=helpers.getRandomRequestHeaders())
      
      if response.status_code != 200:
         raise UnexpectedStatusCodeException(response)
            
      html = response.content
      soup = BeautifulSoup(html, 'html.parser')

      divs = soup.find_all('div', attrs={ 'class': 'js-careers-page-job-list-item' })
      
      for jobDiv in divs:
         
         link = helpers.removeParamsFromLink(self.baseUrl) + jobDiv.find('a')['href']
         name = helpers.toOneLineString(jobDiv.find('h3')['title'])
         workplace = helpers.removeSpacesAndNewLines(jobDiv.find('span', attrs={ 'class': 'meta-job-location-city' }).contents[0])
         department = helpers.toOneLineString(jobDiv.find('div', attrs={ 'class': 'col-md-4 col-xs-12' }).find('div', attrs={ 'class': 'rb-text-4' }).contents[0])
         remote = helpers.toOneLineString(helpers.removeHtmlTags(jobDiv.find('div', attrs={ 'class': 'js-job-list-opening-meta' }).encode_contents().decode("utf-8")))
         
         job = Job()
         job.company = self.companyName
         job.department = helpers.removeSpacesAndNewLines(department)
         job.name = name
         job.remote = helpers.removeSpacesAndNewLines(remote)
         job.url = link
         job.workplace = workplace
         job.type = ""
         job.origin = Origin.TRAKSTAR
         
         jobs.append(job)

      return jobs