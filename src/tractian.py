import json
from typing import List
from bs4 import BeautifulSoup
import requests
from job import Job, Origin
import helpers
from tagger import Tagger

class TractianSearcher():

   jobs: List[Job] = []
   url = 'https://tractian.com/carreiras/vagas'

   departmentsToIgnore = [
      'People', 'Sales', 'Finance', 'Customer', 'Marketing', 'Hardware'
   ]
   
   def search(self):
      
      print("Buscando empregos da empresa Tractian...")

      request = requests.get(self.url)
      html = request.content
      soup = BeautifulSoup(html, 'html.parser')

      nextDataStr = soup.find('script', id="__NEXT_DATA__").decode_contents()

      nextData = json.loads(nextDataStr)

      tagger = Tagger()
      
      for departData in nextData['props']['pageProps']['list']:

         departName = departData['department']

         if departName in self.departmentsToIgnore:
            continue

         for jobData in departData['jobs']:

            workplace = jobData['fields']['place']

            job = Job()
            job.company = 'Tractian'
            job.department = departName
            job.name = jobData['fields']['name']
            job.remote = "yes" if "REMOTE" in workplace.upper() else "no"
            job.url = self.url + '/' + jobData['id']
            job.workplace = workplace
            job.type = ''
            job.origin = Origin.TRACTIAN
            
            job.tags = tagger.generateTags(jobData['fields']['requirements'])
            job.differentialTags = tagger.generateTags(jobData['fields']['extra'])
            
            self.jobs.append(job)

      helpers.waitRandom()
         
