from typing import List
from bs4 import BeautifulSoup
import requests
from job import Job, Origin
import helpers
from tagger import Tagger

class WhatsAppSearcher():

   jobs: List[Job] = []
   url = 'https://www.whatsapp.com'

   def loadDetais(self, job: Job):

      print("Carregando detalhes de um emprego do WhatsApp: " + job.name)
      
      request = requests.get(job.url, headers=helpers.getRandomRequestHeaders())
      html = request.content
      soup = BeautifulSoup(html, 'html.parser')

      firstParagraph = soup.find('p')

      job.workplace = firstParagraph.get_text() if firstParagraph else ""
      
      tags = []
      tagger = Tagger()
      
      for liElem in soup.find_all('li'):
         text = helpers.removeSpacesAndNewLines(helpers.removeHtmlTags(liElem.get_text()))
         
         liTags = tagger.generateTags(text)

         for tag in liTags:
            if tag not in tags:
               tags.append(tag)
      
      job.tags = tags

      helpers.waitRandom()

   def search(self):
      
      print("Buscando empregos da empresa WhatsApp...")

      request = requests.get(self.url + '/join', headers=helpers.getRandomRequestHeaders())
      html = request.content
      soup = BeautifulSoup(html, 'html.parser')

      departments = []

      for elem in soup.find_all('a'):

         if not elem['href']:
            continue
         
         href = elem['href']
         
         if not (href.startswith('/join/?dept=') and "&id" not in href):
            continue

         departUrl  = self.url + href
         departName = elem.get_text()

         if departName in [ 'Business Development & Partnerships', 'Communications & Public Policy', 'Legal, Finance, Facilities & Admin', 'Research', 'Sales & Marketing', 'Messenger' ]:
            continue
         
         alreadyAdded = False
         
         for dep in departments:
            if dep[0] == departUrl:
               alreadyAdded = True
               break
         
         if not alreadyAdded:
            departments.append(( departUrl, departName ))

      if len(departments) == 0:
         return

      helpers.waitRandom()

      for depUrl, depName in departments:
         
         request = requests.get(depUrl, headers=helpers.getRandomRequestHeaders())
         html = request.content
         soup = BeautifulSoup(html, 'html.parser')

         content = soup.find('div', {'class': '_wauiJobDepartment__content'})

         for aElem in content.find_all('a'):
            
            if not "&id" in aElem['href']:
               continue

            job = Job()
            job.company = 'WhatsApp'
            job.department = depName
            job.name = helpers.removeSpacesAndNewLines(aElem.get_text())
            job.remote = '-'
            job.url = self.url + aElem['href']
            job.workplace = ''
            job.type = ''
            job.tags = []
            job.origin = Origin.WHATSAPP
            
            self.jobs.append(job)

         helpers.waitRandom()
         