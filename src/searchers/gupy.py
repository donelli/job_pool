
from typing import List
from bs4 import BeautifulSoup
import requests
from exceptions.element_not_found import ElementNotFoundException
from exceptions.unexpected_status_code import UnexpectedStatusCodeException
from job import Job, Origin
import helpers
from searcher import Searcher

from tagger import Tagger

class GupySearcher(Searcher):
   
   def getCompanyName(self) -> str:
      return 'Gupy'

   def loadDetails(self, job: Job) -> None:

      helpers.waitRandom()
      
      response = requests.get(job.url, headers=helpers.getRandomRequestHeaders())
      
      if response.status_code != 200:
         raise UnexpectedStatusCodeException(response)
      
      html = response.content
      soup = BeautifulSoup(html, 'html.parser')
      
      description = soup.find('div', attrs={ "class": "description" })

      if description is None:
         raise ElementNotFoundException('div', class_='description')

      job.tags = Tagger().generateTags(helpers.removeHtmlTags(description.encode_contents().decode("utf-8")))
   
   def search(self):
      pass

   def searchWithParams(self, companyName, baseUrl, departments = [], workplaces = []) -> List[Job]:
      
      jobs = []
      response = requests.get(baseUrl, headers=helpers.getRandomRequestHeaders())
      
      if response.status_code != 200:
         raise UnexpectedStatusCodeException(response)
         
      html = response.content
      soup = BeautifulSoup(html, 'html.parser')
      
      divs = soup.find('div', attrs={ "class": "job-list" })
      
      if divs is None:
         raise ElementNotFoundException('div', class_='job-list')
      
      trs = divs.find_all("tr")

      if len(trs) == 0:
         return []
      
      for tr in trs:
         
         hrefElem = tr.find("a", attrs={ "class": "job-list__item" })
         
         if not hrefElem:
            raise ElementNotFoundException('a', class_='job-list__item')
         
         titleElem = tr.find("span", attrs={ "class": "title" })
         
         if not titleElem:
            raise ElementNotFoundException('span', class_='title')
         
         type = tr['data-type'].strip()
         workplace = tr['data-workplace'].strip()
         department = tr['data-department'].strip()
         remote = tr['data-remote'].strip()
         
         job = Job()
         job.name = titleElem.getText().strip()
         job.url = baseUrl + hrefElem['href'].strip()
         job.type = type
         job.workplace = workplace
         job.department = department
         job.remote = remote
         job.company = companyName
         job.origin = Origin.GUPY
         
         if job.remote == 'true':
            job.remote = 'yes'
         elif job.remote == 'false':
            job.remote = 'no'
         else:
            job.remote = '-'
         
         if len(departments) > 0:
      
            find = False
            departmentFilter = helpers.remove_accent_chars(department)
            
            for depart in departments:
               if helpers.remove_accent_chars(depart) == departmentFilter:
                  find = True
                  break
            
            if not find:
               continue
            
         if len(workplaces) > 0:
            
            find = False
            workplacesFilter = helpers.remove_accent_chars(workplace)
            
            for place in workplaces:
               if helpers.remove_accent_chars(place) == workplacesFilter:
                  find = True
                  break
            
            if not find:
               continue
         
         jobs.append(job)
      
      return jobs