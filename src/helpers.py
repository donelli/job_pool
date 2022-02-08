import random
import sys
import time
from typing import List
import regex
import unicodedata
import datetime
import re
import pyuser_agent
import shlex
import subprocess

CLEANR = re.compile('<.*?>') 
SPACESR = re.compile("\s{2,}")

def isToday(date: datetime.datetime):
  now = datetime.datetime.today()
  return date.year == now.year and date.month == now.month and date.day == now.day

def remove_accent_chars(x: str):
  return regex.sub(r'\p{Mn}', '', unicodedata.normalize('NFKD', x))

def removeSpacesAndNewLines(s: str):
  return s.replace('\n', '').strip()

def removeHtmlTags(s: str):
  return re.sub(CLEANR, ' ', s)

def toOneLineString(s: str):
  return re.sub(SPACESR, ' ', s.replace('\n', ' '))

def removeParamsFromLink(link: str):
  return link.split("?")[0] if link.index("?") >= 0 else link

def waitRandom():
  time.sleep(random.randint(5, 15))

def getRandomRequestHeaders():
  
  ua = pyuser_agent.UA()

  headers = {
    "User-Agent" : ua.random
  }

  return headers

def performGetCurl(url: str):
  
  # Make sure that cURL has Silent mode (--silent) activated
  # otherwise we receive progress data inside err message later
  cURL = r"""curl """ + url

  lCmd = shlex.split(cURL) # Splits cURL into an array

  p = subprocess.Popen(lCmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  out, err = p.communicate() # Get the output and the err message

  json_data = out.decode("utf-8")

  return json_data

def capitalizeWords(string: str) -> str:
  list_of_words = string.split(" ")

  for index, word in enumerate(list_of_words):
    
    if word == 'e' or word == 'a':
      list_of_words[index] = word
    else:
      list_of_words[index] = word.capitalize()

  return " ".join(list_of_words)

def reportGenerationError(message: List[str], fatal: bool = False):
  
  print("\n".join(message))
  
  if fatal:
    sys.exit(1)
