from bs4 import BeautifulSoup
import requests
from job import Job
import helpers
from tagger import Tagger

class GreenhouseSearcher():
   
   jobs = []

   def getTags(self, url):
         
         helpers.waitRandom()
         
         request = requests.get(url)
         html = request.content
         soup = BeautifulSoup(html, 'html.parser')
         
         jobDescription = soup.find('div', { 'id': 'content' })

         if jobDescription is None:
            print("Nao tem conteudo: " + url)
            return []
         
         return Tagger().generateTags(helpers.removeHtmlTags(jobDescription.encode_contents().decode("utf-8")))
   
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

         job.tags = self.getTags(link)
         
         self.jobs.append(job)
         
      helpers.waitRandom()
      