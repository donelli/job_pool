
import json
from typing import List
import requests
from exceptions.unexpected_status_code import UnexpectedStatusCodeException
from job import Job, Origin
import helpers
from bs4 import BeautifulSoup
from searcher import Searcher
from tagger import Tagger

# Filters:
# - Location: Remote
# - Categories: Engineering, Data Science, Developer Tools & Infrastructure, UX Writing
# - Type: all

class SpotifySearcher(Searcher):
   
   apiUrl = 'https://api-dot-new-spotifyjobs-com.nw.r.appspot.com/wp-json/animal/v1/job/search?l=remote&c=engineering%2Cdata-research-insights'
   companyName = 'Spotify'

   def getCompanyName(self) -> str:
      return self.companyName

   def loadDetails(self, job: Job):
      
      response = requests.get(job.url, headers=helpers.getRandomRequestHeaders())
      
      if response.status_code != 200:
         raise UnexpectedStatusCodeException(response)
      
      soup = BeautifulSoup(response.content, 'html.parser')
      
      tagger = Tagger()
      
      for ul in soup.find_all('ul', attrs={ 'class': ['line-150', 'size-6', 'size-7-mobile'] }):
         
         for li in ul:
            
            tags = tagger.generateTags(helpers.removeHtmlTags(li.encode_contents().decode("utf-8")))
            
            for tag in tags:
               if tag not in job.tags:
                  job.tags.append(tag)
      
   def search(self) -> List[Job]:
      
      response = requests.get(self.apiUrl, headers=helpers.getRandomRequestHeaders())

      if response.status_code != 200:
         raise UnexpectedStatusCodeException(response)
      
      data = json.loads(response.content)
      jobs = []

      for jobData in data['result']:

         # Europa, Oriente Médio e África
         if "EMEA" in jobData['remote_name']['name']:
            continue
         
         job = Job()
         job.company = self.companyName
         job.department = jobData['main_category']['name']
         job.name = jobData['text']
         job.remote = ('yes' if jobData['is_remote'] else 'no')
         job.url = 'https://www.lifeatspotify.com/jobs/' + jobData['id']
         job.workplace = jobData['location']['location']
         job.type = jobData['job_type']['name']
         job.tags = []
         job.origin = Origin.SPOTIFY
         
         jobs.append(job)

      return jobs
      