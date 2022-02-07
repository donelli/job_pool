from time import sleep
from typing import List
from bs4 import BeautifulSoup
import requests
from job import Job, Origin
import helpers
from tagger import Tagger

class TrakstarSearcher():
   
   jobs: List[Job] = []
   
   def loadTags(self, job: Job):
      
      helpers.waitRandom()
      
      request = requests.get(job.url, headers=helpers.getRandomRequestHeaders())
      html = request.content
      soup = BeautifulSoup(html, 'html.parser')
      
      jobDescription = soup.find('div', attrs={ 'class': 'jobdesciption' })
      
      if jobDescription is None:
         print("Nao tem conteudo: " + job.url)
         return
      
      job.tags = Tagger().generateTags(helpers.removeHtmlTags(jobDescription.encode_contents().decode("utf-8")))
   
   def search(self, companyName, baseUrl):
      
      print("Buscando empregos da empresa " + companyName + " no Trakstar...")
      
      request = requests.get(baseUrl, headers=helpers.getRandomRequestHeaders())
      html = request.content
      soup = BeautifulSoup(html, 'html.parser')

      divs = soup.find_all('div', attrs={ 'class': 'js-careers-page-job-list-item' })
      
      for jobDiv in divs:
         
         link = helpers.removeParamsFromLink(baseUrl) + jobDiv.find('a')['href']
         name = helpers.toOneLineString(jobDiv.find('h3')['title'])
         workplace = helpers.removeSpacesAndNewLines(jobDiv.find('span', attrs={ 'class': 'meta-job-location-city' }).contents[0])
         department = helpers.toOneLineString(jobDiv.find('div', attrs={ 'class': 'col-md-4 col-xs-12' }).find('div', attrs={ 'class': 'rb-text-4' }).contents[0])
         remote = helpers.toOneLineString(helpers.removeHtmlTags(jobDiv.find('div', attrs={ 'class': 'js-job-list-opening-meta' }).encode_contents().decode("utf-8")))
         
         job = Job()
         job.company = companyName
         job.department = helpers.removeSpacesAndNewLines(department)
         job.name = name
         job.remote = helpers.removeSpacesAndNewLines(remote)
         job.url = link
         job.workplace = workplace
         job.type = ""
         job.origin = Origin.TRAKSTAR
         
         self.jobs.append(job)

      helpers.waitRandom()