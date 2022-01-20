from ast import If
from traceback import print_tb
from typing import List
from bs4 import BeautifulSoup
import bs4
import requests
from job import Job, Origin
import helpers
from tagger import Tagger

class GreenhouseSearcher():
   
   jobs: List[Job] = []

   def loadTags(self, job: Job):
         
         helpers.waitRandom()
         
         request = requests.get(job.url)
         html = request.content
         soup = BeautifulSoup(html, 'html.parser')
         
         # TODO: Buscar corretamente as tags, na pagina tem todos as tecnologias utilizadas pela empresa, alterar para pegar somente o que importa.
         # https://boards.greenhouse.io/amedigital/jobs/5117595002

         # TODO boa oportunidade para buscar tags que são requisitos, e tags que são diferenciais
         
         jobDescription = soup.find('div', { 'id': 'content' })
         
         if jobDescription is None:
            print("Nao tem conteudo: " + job.url)
            return
         
         tags: List[str] = []
         differentialTags: List[str] = []
         foundRequirements = False
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

   def search(self, companyName, baseUrl):
      
      print("Buscando empregos da empresa " + companyName + " no Greenhouse...")
      
      request = requests.get(baseUrl)
      html = request.content
      soup = BeautifulSoup(html, 'html.parser')
      
      divs = soup.find_all('div', attrs={ 'class': 'opening' })
      
      for jobDiv in divs:
         
         jobUrl = jobDiv.find('a')['href']
         barPos = jobUrl.index('/', 1)
         
         link = baseUrl + jobUrl[barPos:]
         workplace = jobDiv.find('span', attrs={ 'class': 'location' }).encode_contents().decode("utf-8")
         name = jobDiv.find('a').encode_contents().decode("utf-8")
         
         job = Job()
         job.name = name
         job.workplace = workplace
         job.url = link
         job.company = companyName
         job.origin = Origin.GREENHOUSE

         self.jobs.append(job)
         
      helpers.waitRandom()
      

if __name__ == "__main__":

   g = GreenhouseSearcher()

   job = Job()
   job.url = "https://boards.greenhouse.io/amedigital/jobs/5117595002"
   
   print(g.loadTags(job))