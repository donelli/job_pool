from typing import List
from bs4 import BeautifulSoup
import bs4
import requests
from job import Job, Origin
import helpers
from tagger import Tagger

class NubankSearcher():
   
   jobs: List[Job] = []

   companyName = 'Nubank'
   baseUrl     = 'https://boards.greenhouse.io/nubank'

   categoriesToExclude = [
      'Capital Markets',
      'Compliance',
      'Controllership',
      'FP&A',
      'Legal',
      'Marketing Insights & Analytics',
      'People',
      'Product Manager',
      'Public Policy',
      'Regulatory Operations',
      'Risk Management',
      'Xpeer'
   ]

   def loadTags(self, job: Job):
         
      helpers.waitRandom()
      
      request = requests.get(job.url)
      html = request.content
      soup = BeautifulSoup(html, 'html.parser')
      
      jobDescription = soup.find('div', { 'id': 'content' })
      
      if jobDescription is None:
         print("Nao tem conteudo: " + job.url)
         return
      
      tags: List[str] = []
      
      for element in jobDescription:
         
         content = ""
         
         if type(element) is bs4.element.Tag:
            content = element.get_text()
         else:
            content = str(element)

         content = content.strip()

         if content == "":
            continue

         newTags = Tagger().generateTags(helpers.removeHtmlTags(content))
         
         for tag in newTags:
            if tag not in tags:
               tags.append(tag)

      job.tags = tags

   def search(self):
      
      print("Buscando empregos da empresa " + self.companyName + " no Greenhouse...")
      
      request = requests.get(self.baseUrl)
      html = request.content
      soup = BeautifulSoup(html, 'html.parser')
      
      categoryDivs = soup.find_all('section', attrs={ 'class': 'level-0' })
      
      for categoryDiv in categoryDivs:
         
         categoryName = categoryDiv.find('h2').get_text()

         if categoryName in self.categoriesToExclude:
            continue
         
         jobDivs = categoryDiv.find_all('div', attrs={ 'class': 'opening' })
         
         for jobDiv in jobDivs:
         
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
            job.origin = Origin.NUBANK

            self.jobs.append(job)
         
      helpers.waitRandom()
   