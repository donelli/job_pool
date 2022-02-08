
from enum import Enum, auto
from typing import List

class Origin(Enum):
   AME_DIGITAL = auto()
   GUPY = auto()
   HOTMART = auto()
   SPOTIFY = auto()
   TRAKSTAR = auto()
   NETFLIX = auto()
   NUBANK = auto()
   SAP = auto()
   PAYPAL = auto()
   WHATSAPP = auto()
   TRACTIAN = auto()
   IBM = auto()
   DELL = auto()
   NEXT = auto()

class Job():
   
   company: str = ''
   name: str = ''
   url: str = ''
   type: str = ''
   workplace: str = ''
   department: str = ''
   remote: str = ''
   tags: List[str] = []
   differentialTags: List[str] = []
   inclusionDate = ''
   origin: Origin

   def toMap(self):
      return {
         'name': self.name,
         'url': self.url,
         'type': self.type,
         'workplace': self.workplace,
         'department': self.department,
         'remote': self.remote,
         'company': self.company,
         'tags': self.tags,
         'diferTags': self.differentialTags
      }

   def __str__(self):
      return 'Name: ' + self.name + \
          ' - Url: ' + self.url + \
          ' - Type: ' + self.type + \
          ' - Workplace: ' + self.workplace + \
          ' - Department: ' + self.department + \
          ' - Remote: ' + self.remote + \
          ' - Company: ' + self.company + \
          ' - Tags: ' + ", ".join(self.tags) + \
         ' - Differential Tags: ' + ", ".join(self.differentialTags)
