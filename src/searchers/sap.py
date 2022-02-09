
from typing import List
from exceptions.unexpected_status_code import UnexpectedStatusCodeException
import helpers
import requests
from bs4 import BeautifulSoup
import bs4

from job import Job, Origin
from searcher import Searcher
from tagger import Tagger

class SapSearcher(Searcher):

   companyName = 'SAP Brasil'

   departments = [
      'Software-Design+and+Development',
      'Software-Development+Operations',
      'Software-User+Experience'
   ]

   baseUrl = 'https://jobs.sap.com/search/?optionsFacetsDD_country=BR&optionsFacetsDD_department='

   def getCompanyName(self) -> str:
      return self.companyName

   def loadDetails(self, job: Job):
      
      helpers.waitRandom()
      
      response = requests.get(job.url, headers=helpers.getRandomRequestHeaders())
      
      if response.status_code != 200:
         raise UnexpectedStatusCodeException(response)
      
      html = response.content
      soup = BeautifulSoup(html, 'html.parser')
      
      jobDescription = soup.find('span', attrs={ "class": "jobdescription" })
      
      tags: List[str] = []
      strsToSearch: List[str] = []
      
      lisElem = jobDescription.find_all('li')
      
      for element in lisElem:

         content = ""
         
         if type(element) is bs4.element.Tag:
            content = element.get_text()
         else:
            content = str(element)

         content = helpers.removeHtmlTags(content.strip())

         if content != "":
            strsToSearch.append(content)

      spanElements = jobDescription.find_all('span')
      
      for element in spanElements:

         content = ""
         
         if type(element) is bs4.element.Tag:
            content = element.get_text()
         else:
            content = str(element)

         content = helpers.removeHtmlTags(content.strip())

         if content == "":
            continue

         if content[0] != "•":
            continue

         strsToSearch.append(content)

      for content in strsToSearch:
                  
         newTags = Tagger().generateTags(content)
         
         for tag in newTags:
            
            if tag == "SAP":
               continue
            
            if tag not in tags:
               tags.append(tag)


      job.tags = tags

   def search(self) -> List[Job]:

      jobs = []

      for department in self.departments:

         print(" - Departamento: " + department)

         url = self.baseUrl + department
         
         response = requests.get(url, headers=helpers.getRandomRequestHeaders())
         
         if response.status_code != 200:
            raise UnexpectedStatusCodeException(response)
         
         soup = BeautifulSoup(response.content, 'html.parser')

         for tr in soup.find_all('tr', attrs={ 'class': 'data-row clickable' }):
            
            aElement = tr.find('a')
            spanElement = tr.find('span', attrs={ 'class': 'jobLocation' })

            job = Job()
            job.name = helpers.removeSpacesAndNewLines(aElement.get_text())
            job.department = department
            job.workplace = helpers.removeSpacesAndNewLines(spanElement.get_text())
            job.url = "https://jobs.sap.com" + aElement['href']
            job.company = self.companyName
            job.origin = Origin.SAP
            job.remote = 'yes'
            
            jobs.append(job)
         
         helpers.waitRandom()

      return jobs
