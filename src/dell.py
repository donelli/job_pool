
import json
from time import time
from typing import List
from attr import attr
from bs4 import BeautifulSoup
import bs4
import requests
from job import Job, Origin
import helpers

from tagger import Tagger

class DellSeacher():
   
   jobs: List[Job] = []
   headers = {}

   apiUrl = 'https://carreiras.dell.com/search-jobs/results?ActiveFacetID=66002&CurrentPage=1&RecordsPerPage=15&Distance=50&RadiusUnitType=0&Keywords=&Location=&ShowRadius=False&IsPagination=False&CustomFacetName=&FacetTerm=&FacetType=0&FacetFilters%5B0%5D.ID=71833&FacetFilters%5B0%5D.FacetType=1&FacetFilters%5B0%5D.Count=1&FacetFilters%5B0%5D.Display=Digital&FacetFilters%5B0%5D.IsApplied=true&FacetFilters%5B0%5D.FieldName=&FacetFilters%5B1%5D.ID=65998&FacetFilters%5B1%5D.FacetType=1&FacetFilters%5B1%5D.Count=68&FacetFilters%5B1%5D.Display=Engenharia&FacetFilters%5B1%5D.IsApplied=true&FacetFilters%5B1%5D.FieldName=&FacetFilters%5B2%5D.ID=79470&FacetFilters%5B2%5D.FacetType=1&FacetFilters%5B2%5D.Count=9&FacetFilters%5B2%5D.Display=Software+Engineering&FacetFilters%5B2%5D.IsApplied=true&FacetFilters%5B2%5D.FieldName=&FacetFilters%5B3%5D.ID=70861&FacetFilters%5B3%5D.FacetType=1&FacetFilters%5B3%5D.Count=4&FacetFilters%5B3%5D.Display=SRO&FacetFilters%5B3%5D.IsApplied=true&FacetFilters%5B3%5D.FieldName=&FacetFilters%5B4%5D.ID=66002&FacetFilters%5B4%5D.FacetType=1&FacetFilters%5B4%5D.Count=5&FacetFilters%5B4%5D.Display=Tecnologia+da+informa%C3%A7%C3%A3o+-+TI&FacetFilters%5B4%5D.IsApplied=true&FacetFilters%5B4%5D.FieldName=&FacetFilters%5B5%5D.ID=3469034&FacetFilters%5B5%5D.FacetType=2&FacetFilters%5B5%5D.Count=73&FacetFilters%5B5%5D.Display=Brasil&FacetFilters%5B5%5D.IsApplied=true&FacetFilters%5B5%5D.FieldName=&SearchResultsModuleName=Search+Results&SearchFiltersModuleName=Search+Filters&SortCriteria=0&SortDirection=0&SearchType=5&PostalCode=&fc=&fl=&fcf=&afc=&afl=&afcf='

   def loadTags(self, job: Job):
      
      helpers.waitRandom()
      
      # Por algum motivo, o HTTPS cai em timeout...
      url = job.url.replace('https:', 'http:')
      
      request = requests.get(url, headers=self.headers, timeout=10)
      html = request.content
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
      
      print("Buscando empregos da empresa Dell...")
      
      self.headers = helpers.getRandomRequestHeaders()
      
      response = requests.get(self.apiUrl, headers=self.headers, timeout=10)
      
      print("Processando retorno...")
      
      data = json.loads(response.content)   

      jobsHtml = BeautifulSoup(data['results'], 'html.parser')

      results = jobsHtml.find('section', attrs={ 'id': 'search-results-list' })

      for jobLi in results.find_all('li'):
         
         jobName = jobLi.find('h2')
         aElem = jobLi.find('a')
         jobLoc = jobLi.find('span', attrs={ 'class': 'job-location' })
         
         if not jobName:
            continue

         workPlace = helpers.removeSpacesAndNewLines(jobLoc.get_text())
         
         job = Job()
         job.company = 'Dell'
         job.department = ''
         job.name = helpers.removeSpacesAndNewLines(jobName.get_text())
         job.remote = "yes" if "remote" in workPlace.lower() else "no"
         job.url = 'https://carreiras.dell.com' + aElem['href']
         job.workplace = workPlace
         job.type = ''
         job.tags = []
         job.origin = Origin.DELL
         
         self.jobs.append(job)
      

if __name__ == '__main__':
   
   searcher = DellSeacher()
   searcher.search()

   for job in searcher.jobs:
      searcher.loadTags(job)
      print(job)
      print('--------------------------')