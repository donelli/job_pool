
import json
from traceback import print_tb
from typing import List
import requests
from job import Job, Origin
import helpers
from bs4 import BeautifulSoup

from tagger import Tagger

# Filters:
# - Location: Remote
# - Categories: Engineering, Data Science, Developer Tools & Infrastructure, UX Writing
# - Type: all

class SpotifySearcher():
   
   apiUrl = 'https://api-dot-new-spotifyjobs-com.nw.r.appspot.com/wp-json/animal/v1/job/search?l=remote&c=engineering%2Cdata-research-insights'
   jobs: List[Job] = []

   def loadTags(self, job: Job):
      
      print("Carregando TAGS de um emprego do Spotify: " + job.name)
      
      request = requests.get(job.url)
      soup = BeautifulSoup(request.content, 'html.parser')
      
      tagger = Tagger()
      
      for ul in soup.find_all('ul', attrs={ 'class': ['line-150', 'size-6', 'size-7-mobile'] }):
         
         for li in ul:
            
            tags = tagger.generateTags(helpers.removeHtmlTags(li.encode_contents().decode("utf-8")))
            
            for tag in tags:
               if tag not in job.tags:
                  job.tags.append(tag)
   
      helpers.waitRandom()
      
   def search(self) -> None:
      
      print("Buscando empregos da empresa Spotify...")
      
      request = requests.get(self.apiUrl)

      data = json.loads(request.content)

      for jobData in data['result']:

         job = Job()
         job.company = 'Spotify'
         job.department = jobData['main_category']['name']
         job.name = jobData['text']
         job.remote = ('yes' if jobData['is_remote'] else 'no') + ((' (' + jobData['remote_name']['name'] + ')') if jobData['is_remote'] else '')
         job.url = 'https://www.lifeatspotify.com/jobs/' + jobData['id']
         job.workplace = jobData['location']['location']
         job.type = jobData['job_type']['name']
         job.tags = []
         job.origin = Origin.SPOTIFY
         
         self.jobs.append(job)
      
      helpers.waitRandom()
