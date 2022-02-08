import json
from typing import List
import requests
from job import Job, Origin
import helpers
from tagger import Tagger

class AmazonSearcher():
   
   jobs: List[Job] = []

   baseUrl = 'https://www.amazon.jobs/pt/search.json?facets%5B%5D=location&facets%5B%5D=business_category&facets%5B%5D=category&facets%5B%5D=employee_class&facets%5B%5D=normalized_location&sort=relevant&latitude&longitude&loc_group_id&loc_query=Brasil&base_query&city&country=BRA&region&county&query_options&result_limit=100&offset='

   categoriesToProcess = [
      'Solutions Architect',
      'Software Development',
      'Project/Program/Product Management--Technical',
      'Operations, IT, & Support Engineering',
      'Systems, Quality, & Security Engineering'
   ]
   
   def search(self):
      
      print("Buscando empregos da empresa Amazon...")

      offset = 600
      tagger = Tagger()

      while True:
         
         print(" -> Offset " + str(offset))
         
         url = self.baseUrl + str(offset)
         
         headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36'
         }
         
         request = requests.get(url, headers=headers)
         
         data = json.loads(request.content)
         
         if len(data['jobs']) == 0:
            break
         
         for jobData in data['jobs']:

            if jobData['job_category'] not in self.categoriesToProcess:
               continue
            
            job = Job()
            job.company = 'Amazon'
            job.department = jobData['job_category']
            job.name = jobData['title']
            job.remote = '-'
            job.url = 'https://www.amazon.jobs' + jobData['job_path']
            job.workplace = jobData['normalized_location']
            job.type = ""
            job.origin = Origin.AMAZON
            
            job.tags = tagger.generateTags(jobData['basic_qualifications'])
            
            # job.differentialTags = tagger.generateTags(jobData['preferred_qualifications'])
            
            job.differentialTags = []
            for tag in tagger.generateTags(jobData['preferred_qualifications']):
               if tag not in job.tags:
                  job.differentialTags.append(tag)
            
            self.jobs.append(job)
         
         offset += 100
         helpers.waitRandom()
      