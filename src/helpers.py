import random
import time
import regex
import unicodedata
import datetime
import re

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
  return re.sub(CLEANR, '', s)

def toOneLineString(s: str):
  return re.sub(SPACESR, ' ', s.replace('\n', ' '))

def removeParamsFromLink(link: str):
  return link.split("?")[0] if link.index("?") >= 0 else link

def waitRandom():
  time.sleep(random.randint(1, 5))