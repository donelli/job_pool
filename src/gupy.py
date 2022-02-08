
import os
import sys
from typing import List
from bs4 import BeautifulSoup
import requests
from job import Job, Origin
import helpers

from tagger import Tagger

class GupySearcher():
   
   jobs: List[Job] = []

   def loadTags(self, job: Job) -> None:

      helpers.waitRandom()
      
      response = requests.get(job.url, headers=helpers.getRandomRequestHeaders())
      
      if response.status_code != 200:
         helpers.reportGenerationError([
            "Erro ao buscar detalhes do emprego da Gupy. Status code: " + str(response.status_code),
            "Job: " + str(job),
            "Content: " + response.content
         ], fatal=True)
      
      html = response.content
      soup = BeautifulSoup(html, 'html.parser')
      
      description = soup.find('div', attrs={ "class": "description" })

      if description is None:
         helpers.reportGenerationError([
            "Não encontrou a div com a classe 'description'",
            "Content: " + response.content
         ], fatal=True)

      job.tags = Tagger().generateTags(helpers.removeHtmlTags(description.encode_contents().decode("utf-8")))
   
   def search(self, companyName, baseUrl, departments = [], workplaces = []):
      
      print("Buscando empregos da empresa " + companyName + " no Gupy...")
      
      response = requests.get(baseUrl, headers=helpers.getRandomRequestHeaders())
      
      if response.status_code != 200:
         helpers.reportGenerationError([
            "Erro ao buscar empregos da empresa " + companyName + " no Gupy. Status code: " + str(response.status_code),
            "URL: " + baseUrl,
            "Content: " + response.content
         ], fatal=True)
         
      html = response.content
      soup = BeautifulSoup(html, 'html.parser')
      
      divs = soup.find('div', attrs={ "class": "job-list" })
      
      if divs is None:
         helpers.reportGenerationError([
            "Não encontrou a div com a classe 'job-list'",
            "Content: " + response.content
         ], fatal=True)
      
      trs = divs.find_all("tr")

      if len(trs) == 0:
         print(" -> Não encontrou nenhum emprego")
         return
      
      for tr in trs:
         
         href = tr.find_all("a", attrs={ "class": "job-list__item" })[0]['href'].strip()
         title = tr.find_all("span", attrs={ "class": "title" })[0].getText().strip()
         type = tr['data-type'].strip()
         workplace = tr['data-workplace'].strip()
         department = tr['data-department'].strip()
         remote = tr['data-remote'].strip()
         
         job = Job()
         job.name = title
         job.url = baseUrl + href
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
         
         self.jobs.append(job)
      
      helpers.waitRandom()
