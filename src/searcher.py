import abc
from typing import List
from job import Job

class Searcher(metaclass=abc.ABCMeta):
   
   @abc.abstractmethod
   def search(self) -> List[Job]:
      return []
      
   @abc.abstractmethod
   def loadDetails(self, job: Job) -> None:
      return
      
   @abc.abstractmethod
   def getCompanyName(self) -> str:
      return ''
      