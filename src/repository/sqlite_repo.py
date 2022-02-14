import sqlite3
from sqlite3 import Connection
from typing import List
from base_repo import Repository
from job import Job
import time

class SqliteRepository(Repository):
  
   conn: Connection
  
   def connectToDb(self) -> None:
      
      self.conn = sqlite3.connect('./data/jobs.db')
      
      cursor = self.conn.cursor()
      
      cursor.execute("""
         CREATE TABLE IF NOT EXISTS job (
         url TEXT,
         name TEXT,
         type TEXT,
         workplace TEXT,
         department TEXT,
         remote TEXT,
         company TEXT,
         inclusionDate FLOAT,
         tags TEXT,
         differential_tags TEXT
         )
      """)

      cursor.close()
   
   def closeDb(self) -> None:
      self.conn.close()
   
   def jobUrlExists(self, jobUrl: str) -> bool:
      
      cursor = self.conn.cursor()
      
      res = cursor.execute("""
         SELECT * FROM job WHERE url = ?
      """, [ jobUrl ])
      
      records = res.fetchall()
      cursor.close()
      
      if len(records) <= 0:
         return False

      return True

   def tupleToJob(self, tuple:tuple) -> Job:
      
      job = Job()
      
      job.url = tuple[0]
      job.name = tuple[1]
      job.type = tuple[2]
      job.workplace = tuple[3]
      job.department = tuple[4]
      job.remote = tuple[5]
      job.company = tuple[6]
      job.inclusionDate = tuple[7]
      job.tags = tuple[8].split("|")
      job.differentialTags = tuple[9].split("|") if tuple[9] != "" else []
      
      return job
    
   def getAllJobs(self) -> List[Job]:
      
      cursor = self.conn.cursor()
      res = cursor.execute("SELECT * FROM job")
      
      response = [ self.tupleToJob(row) for row in res.fetchall() ]
      cursor.close()

      return response

   def getAllJobsByCompany(self, company: str) -> List[Job]:
      
      cursor = self.conn.cursor()
      res = cursor.execute("SELECT * FROM job where company = ?", [ company ])
      
      response = [ self.tupleToJob(row) for row in res.fetchall() ]
      cursor.close()

      return response
    
   def removeJobByUrl(self, jobUrl: str) -> None:
      
      cursor = self.conn.cursor()
      
      cursor.execute('DELETE FROM job WHERE url = :url', { "url": jobUrl })
      self.conn.commit()
      cursor.close()

   def insertJob(self, job: Job) -> None:
      
      cursor = self.conn.cursor()
      
      tagsStr =  "|".join(job.tags)
      differTagsStr =  "|".join(job.differentialTags)
      
      cursor.execute("""
         INSERT INTO job(url, name, type, workplace, department, remote, company, inclusionDate, tags, differential_tags)
         VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
         """, ( job.url, job.name, job.type, job.workplace, job.department, job.remote, job.company, time.time(), tagsStr, differTagsStr ))
      
      self.conn.commit()
      cursor.close()
    