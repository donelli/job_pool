import abc
from typing import List
from job import Job

class Repository(metaclass=abc.ABCMeta):
  
   @abc.abstractmethod
   def connectToDb(self) -> None:
      pass
   
   @abc.abstractmethod
   def closeDb(self) -> None:
      pass
   
   @abc.abstractmethod
   def jobUrlExists(self, jobUrl: str) -> bool:
      pass

   @abc.abstractmethod
   def getAllJobs(self) -> List[Job]:
      pass

   @abc.abstractmethod
   def getAllJobsByCompany(self, company: str) -> List[Job]:
      pass
    
   @abc.abstractmethod
   def removeJobByUrl(self, jobUrl: str) -> None:
      pass

   @abc.abstractmethod
   def insertJob(self, job: Job) -> None:
      pass

   @abc.abstractmethod
   def saveUniqueTags(self, tags: List[dict]) -> None:
      pass

   @abc.abstractmethod
   def saveUniqueCompanies(self, companies: List[dict]) -> None:
      pass