
import json
from typing import List
from bs4 import BeautifulSoup
import bs4
from exceptions.element_not_found import ElementNotFoundException
from job import Job, Origin
import helpers
from searcher import Searcher

from tagger import Tagger

class DellSearcher(Searcher):

   # Por algum motivo o servidor da Dell não responde corratamente de vez em quando
   # quando utilizado a biblioteca requests, então fiz um workaround utilizando o comando 'curl'
   
   companyName = 'Dell'
   headers: dict = {}
   
   apiUrl = 'https://carreiras.dell.com/search-jobs/results?ActiveFacetID=66002&CurrentPage=1&RecordsPerPage=15&Distance=50&RadiusUnitType=0&Keywords=&Location=&ShowRadius=False&IsPagination=False&CustomFacetName=&FacetTerm=&FacetType=0&FacetFilters%5B0%5D.ID=71833&FacetFilters%5B0%5D.FacetType=1&FacetFilters%5B0%5D.Count=1&FacetFilters%5B0%5D.Display=Digital&FacetFilters%5B0%5D.IsApplied=true&FacetFilters%5B0%5D.FieldName=&FacetFilters%5B1%5D.ID=65998&FacetFilters%5B1%5D.FacetType=1&FacetFilters%5B1%5D.Count=68&FacetFilters%5B1%5D.Display=Engenharia&FacetFilters%5B1%5D.IsApplied=true&FacetFilters%5B1%5D.FieldName=&FacetFilters%5B2%5D.ID=79470&FacetFilters%5B2%5D.FacetType=1&FacetFilters%5B2%5D.Count=9&FacetFilters%5B2%5D.Display=Software+Engineering&FacetFilters%5B2%5D.IsApplied=true&FacetFilters%5B2%5D.FieldName=&FacetFilters%5B3%5D.ID=70861&FacetFilters%5B3%5D.FacetType=1&FacetFilters%5B3%5D.Count=4&FacetFilters%5B3%5D.Display=SRO&FacetFilters%5B3%5D.IsApplied=true&FacetFilters%5B3%5D.FieldName=&FacetFilters%5B4%5D.ID=66002&FacetFilters%5B4%5D.FacetType=1&FacetFilters%5B4%5D.Count=5&FacetFilters%5B4%5D.Display=Tecnologia+da+informa%C3%A7%C3%A3o+-+TI&FacetFilters%5B4%5D.IsApplied=true&FacetFilters%5B4%5D.FieldName=&FacetFilters%5B5%5D.ID=3469034&FacetFilters%5B5%5D.FacetType=2&FacetFilters%5B5%5D.Count=73&FacetFilters%5B5%5D.Display=Brasil&FacetFilters%5B5%5D.IsApplied=true&FacetFilters%5B5%5D.FieldName=&SearchResultsModuleName=Search+Results&SearchFiltersModuleName=Search+Filters&SortCriteria=0&SortDirection=0&SearchType=5&PostalCode=&fc=&fl=&fcf=&afc=&afl=&afcf='

   def getCompanyName(self) -> str:
      return self.companyName

   def loadDetails(self, job: Job):
      
      html = helpers.performGetCurl(job.url)
      soup = BeautifulSoup(html, 'html.parser')
      
      jobDescription = soup.find('div', { 'class': 'ats-description' })
      
      jobDiv = jobDescription.find('div')
      
      if jobDiv is not None:
         jobDescription = jobDiv
      
      if jobDescription is None:
         print("Nao tem conteudo: " + job.url)
         return
         
      tags = []
      
      for elem in jobDescription:
         
         content = ""
         
         if type(elem) is bs4.element.Tag:
            content = elem.get_text()
         else:
            content = str(elem)

         content = helpers.removeHtmlTags(content.strip())

         if content == "":
            continue
         
         if "Dell Technologies helps organizations" in content:
            continue

         for tag in Tagger().generateTags(content):
            if tag not in tags:
               tags.append(tag)

      job.tags = tags
      
   def search(self):
      
      jobs = []
      
      self.headers = helpers.getRandomRequestHeaders()
      
      data = json.loads(helpers.performGetCurl(self.apiUrl))
      
      jobsHtml = BeautifulSoup(data['results'], 'html.parser')

      results = jobsHtml.find('section', attrs={ 'id': 'search-results-list' })

      if not results:
         raise ElementNotFoundException("section", id="search-results-list")

      for jobLi in results.find_all('li'):
         
         jobName = jobLi.find('h2')
         aElem = jobLi.find('a')
         jobLoc = jobLi.find('span', attrs={ 'class': 'job-location' })
         
         if not jobName:
            continue

         workPlace = helpers.removeSpacesAndNewLines(jobLoc.get_text())
         
         if workPlace.startswith(", "):
            workPlace = workPlace[2:].strip()
         
         job = Job()
         job.company = self.companyName
         job.department = ''
         job.name = helpers.removeSpacesAndNewLines(jobName.get_text())
         job.remote = "yes" if "remote" in workPlace.lower() else "no"
         job.url = 'https://carreiras.dell.com' + aElem['href']
         job.workplace = workPlace
         job.type = ''
         job.tags = []
         job.origin = Origin.DELL
         
         jobs.append(job)
      
      return jobs
