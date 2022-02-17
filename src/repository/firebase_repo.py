from time import time
from typing import List
import os
import firebase_admin
from firebase_admin import credentials
from base_repo import Repository
from job import Job
from firebase_admin import db

class FirebaseRepository(Repository):

   def parseUrlToKey(self, url: str):
      return url.replace("/", "").replace("&", "").replace("?", "").replace("=", "").replace("%", "").replace(":", "")

   def dictToJob(self, jobDict: dict) -> Job:
      
      job = Job()
      
      job.url = jobDict['url']
      job.name = jobDict['name']
      job.type = jobDict['type']
      job.workplace = jobDict['workplace']
      job.department = jobDict['department']
      job.remote = jobDict['remote']
      job.company = jobDict['company']
      job.inclusionDate = jobDict['inclusionDate']
      job.tags = jobDict['tags'].split("|")
      job.differentialTags = jobDict['diferTags'].split("|")
      
      return job
    
   def connectToDb(self) -> None:
      
      certPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../certificates/firebase-adminsdk.json")

      cred = credentials.Certificate(certPath)
      firebase_admin.initialize_app(cred, {'databaseURL': 'https://jobs-188f0-default-rtdb.firebaseio.com/'})

   def closeDb(self) -> None:
      pass
   
   def jobUrlExists(self, jobUrl: str) -> bool:
      
      jobs = db.reference('/jobs').order_by_child('urlKey').equal_to(self.parseUrlToKey(jobUrl)).get()

      if len(jobs) == 0:
         return False

      return True
      

   def getAllJobs(self) -> List[Job]:
      
      snapshot = db.reference('/jobs').order_by_child('url').get()
      jobs: List[Job] = []

      for key, val in snapshot.items():
         job = self.dictToJob(val)
         job.id = key
         jobs.append(job)

      return jobs

   def getAllJobsByCompany(self, company: str) -> List[Job]:
      
      snapshot = db.reference('/jobs').order_by_child('company').equal_to(company).get()
      jobs: List[Job] = []

      for key, val in snapshot.items():
         job = self.dictToJob(val)
         job.id = key
         jobs.append(job)

      return jobs
    
   def removeJobByUrl(self, jobUrl: str) -> None:
      
      jobs = db.reference('/jobs').order_by_child('urlKey').equal_to(self.parseUrlToKey(jobUrl)).get()

      for key, value in jobs.items():
         db.reference('/jobs').child(key).delete()

   def insertJob(self, job: Job) -> None:
      job.inclusionDate = time()
      
      data = job.toMap()
      data['urlKey'] = self.parseUrlToKey(job.url)
      
      db.reference('/jobs').push().set(data)

   def saveUniqueTags(self, tags: List[dict]) -> None:
      
      ref = db.reference('/tags')
      ref.delete()
      
      db.reference('/tags').set(tags)
      
   def saveUniqueCompanies(self, companies: List[dict]) -> None:
      
      ref = db.reference('/companies')
      ref.delete()
      
      db.reference('/companies').set(companies)