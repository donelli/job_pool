
from typing import List
import requests
import json
from job import Job, Origin
from tagger import Tagger
import helpers

class HotmartSearcher:
   
   jobs: List[Job] = []
   
   areas = [
      'data-science',
      'development',
      'it-infrastructure-and-security'
   ]

   apiUrl = "https://api-hotmart-jobs.hotmart.com/positions"
   
   def search(self):
      
      resp = requests.get(self.apiUrl)

      data = json.loads(resp.content)

      for hotmartJob in data['data']:
         
         if not hotmartJob['area']['slug'] in self.areas:
            continue
         
         job = Job()
         job.company = 'Hotmart'
         job.name = hotmartJob['title']
         job.url = 'https://www.hotmart.com/jobs/pt-BR/positions/' + hotmartJob['id']
         job.workplace = hotmartJob['office']['city'] + ' - ' + hotmartJob['office']['country']
         job.department = hotmartJob['area']['title']
         job.origin = Origin.HOTMART

         # Pelo que foi observado no site: https://www.hotmart.com/jobs/pt-BR, a empresa da a liberdade para modificar o ambiente de trabalho.
         job.remote = 'yes'
         
         job.tags = Tagger().generateTags(helpers.removeHtmlTags(hotmartJob['description']))
         
         self.jobs.append(job)

