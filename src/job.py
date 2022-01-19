
from typing import List


class Job():
   
   company: str = ''
   name: str = ''
   url: str = ''
   type: str = ''
   workplace: str = ''
   department: str = ''
   remote: str = ''
   tags: List[str] = []
   inclusionDate = ''

   def toMap(self):
      return {
         'name': self.name,
         'url': self.url,
         'type': self.type,
         'workplace': self.workplace,
         'department': self.department,
         'remote': self.remote,
         'company': self.company,
         'tags': self.tags
      }

   def __str__(self):
      return 'Name: ' + self.name + \
          ' - Url: ' + self.url + \
          ' - Type: ' + self.type + \
          ' - Workplace: ' + self.workplace + \
          ' - Department: ' + self.department + \
          ' - Remote: ' + self.remote + \
          ' - Company: ' + self.company + \
          ' - Tags: ' + ", ".join(self.tags)
