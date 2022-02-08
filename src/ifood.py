
from typing import List
from job import Job, Origin
import requests
import helpers
from bs4 import BeautifulSoup
from tagger import Tagger

class IFoodSearcher():

   pageUrl = 'https://carreiras.ifood.com.br/jobs'
   jobs: List[Job] = []
   
   def loadTags(self, job: Job):
      
      helpers.waitRandom()

      request = requests.get(job.url, headers=helpers.getRandomRequestHeaders())
      html = request.content
      soup = BeautifulSoup(html, 'html.parser')

      for ul in soup.find_all('ul'):
         
         if ul.has_attr('class'):
            continue
         
         for li in ul:
            for tag in Tagger().generateTags(str(li)):
               if tag not in job.tags:
                  job.tags.append(tag)

   def search(self):
   
      print("Buscando empregos da empresa iFood...")

      request = requests.get(self.pageUrl, headers=helpers.getRandomRequestHeaders())
      html = request.content
      soup = BeautifulSoup(html, 'html.parser')
      
      for li in soup.find_all('li'):
         
         if not li.has_attr('class'):
            continue

         isItem = False
         for className in li['class']:
            if className.startswith('styles__Card'):
               isItem = True
               break

         if not isItem:
            continue

         department = ''

         for tagElem in li.find_all('li'):
            if not tagElem.has_attr('class') or not tagElem['class'][0].startswith('styles__Tag'):
               continue

            department = tagElem.get_text()
            
         if not (department == 'Tecnologia' or department == 'Data' or department == ''):
            continue
         
         aElem = li.find('a')
         
         location = ''
         h5 = li.find('h5')
         if h5 is not None:
            location = h5.get_text()
         
         job = Job()
         job.company = 'iFood'
         job.department = department
         job.name = helpers.removeSpacesAndNewLines(aElem['title'])
         job.remote = 'yes'
         job.url = 'https://carreiras.ifood.com.br' + aElem['href']
         job.workplace = location
         job.type = ''
         job.tags = []
         job.origin = Origin.IFOOD
         
         self.jobs.append(job)

