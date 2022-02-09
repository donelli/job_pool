
from requests import Response

class UnexpectedStatusCodeException(Exception):
   
   """
   Unexpected status code exception
   """
   
   def __init__(self, response: Response):
      self.response = response

   def __str__(self):
      return f'Unexpected status code: {self.response.status_code} - Url: {self.response.url}\n\nContent: {self.response.content}'
