
from typing import List
import requests
import json
from job import Job, Origin
from searcher import Searcher
from tagger import Tagger
import helpers

class HotmartSearcher(Searcher):

   companyName = 'Hotmart'
   
   areas = [
      'data-science',
      'development',
      'it-infrastructure-and-security'
   ]

   apiUrl = "https://api-hotmart-jobs.hotmart.com/positions"

   def getCompanyName(self) -> str:
      return self.companyName

   def loadDetails(self, job: Job):
      return
   
   def search(self) -> List[Job]:
      
      resp = requests.get(self.apiUrl, headers=helpers.getRandomRequestHeaders())

      data = json.loads(resp.content)
      jobs = []

      for hotmartJob in data['data']:
         
         if not hotmartJob['area']['slug'] in self.areas:
            continue
         
         job = Job()
         job.company = self.companyName
         job.name = hotmartJob['title']
         job.url = 'https://www.hotmart.com/jobs/pt-BR/positions/' + hotmartJob['id']
         job.workplace = hotmartJob['office']['city'] + ' - ' + hotmartJob['office']['country']
         job.department = hotmartJob['area']['title']
         job.origin = Origin.HOTMART

         # Pelo que foi observado no site: https://www.hotmart.com/jobs/pt-BR, a empresa da a liberdade para modificar o ambiente de trabalho.
         job.remote = 'yes'
         
         job.tags = Tagger().generateTags(helpers.removeHtmlTags(hotmartJob['description']))
         
         jobs.append(job)
   
      return jobs
