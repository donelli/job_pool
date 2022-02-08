from typing import List
from bs4 import BeautifulSoup
import bs4
import requests
from job import Job, Origin
import helpers
from tagger import Tagger

class AmeDigitalSearcher():
   
   jobs: List[Job] = []

   companyName = 'Ame Digital'
   baseUrl     = 'https://boards.greenhouse.io/amedigital'

   def loadTags(self, job: Job):
         
         helpers.waitRandom()
         
         request = requests.get(job.url, headers=helpers.getRandomRequestHeaders())
         html = request.content
         soup = BeautifulSoup(html, 'html.parser')
         
         jobDescription = soup.find('div', { 'id': 'content' })
         
         if jobDescription is None:
            print("Nao tem conteudo: " + job.url)
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

   def search(self):
      
      print("Buscando empregos da empresa " + self.companyName + " no Greenhouse...")
      
      request = requests.get(self.baseUrl, headers=helpers.getRandomRequestHeaders())
      html = request.content
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

         self.jobs.append(job)
         
      helpers.waitRandom()
      