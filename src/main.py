
import json
from typing import List
from amazon import AmazonSearcher
from dell import DellSeacher
from gupy import GupySearcher
from ame_digital import AmeDigitalSearcher
from hotmart import HotmartSearcher
from ibm import IbmSearcher
from ifood import IFoodSearcher
from netflix import NetflixSearcher
from next_bank import NextBankSeacher
from nubank import NubankSearcher
from repository import Repository
from job import Job, Origin
from sap import SapSearcher
from spotify import SpotifySearcher
from tractian import TractianSearcher
from trakstar import TrakstarSearcher
from paypal import PaypalSearcher
from whatsapp import WhatsAppSearcher

def isValidJob(job: Job) -> bool:

   jobName = job.name.upper()
   
   if job.origin == Origin.IFOOD and job.department == "" and len(job.tags) == 0:
      return False
   
   if len(job.tags) > 0:
      return True
   
   if "ENGINEER" in jobName or "SOFTWARE" in jobName or "ANALYST" in jobName or "ENGENH" in jobName or "DESENVOLVEDOR" in jobName:
      return True
   
   if "LAW " in jobName:
      return False
   
   if "MARKET SPECIALIST" in jobName:
      return False

   if "MARKETING " in jobName:
      return False

   if "INTERN " in jobName or jobName.endswith(" INTERN"):
      return False

   if "ESTAGIÁRIO" in jobName or "ESTÁGIO" in jobName:
      return False

   if "TALENT" in jobName:
      return False

   if "ATENDIMENTO" in jobName or "SAC" in jobName or "CRM" in jobName:
      return False

   if "ADMINISTRATIVO" in jobName:
      return False

   if "ANALISTA COMERCIAL" in jobName:
      return False

   if "INCLUSÃO DE PESSOAS" in jobName:
      return False

   if "ANALISTA DE NEGÓCIOS" in jobName:
      return False

   if "POLICY" in jobName:
      return False

   if 'ASSISTENTE TÉCNICO' in jobName:
      return False

   if "COMUNICAÇÃO" in jobName or "SEGUROS DIGITAIS" in jobName or \
      "COMERCIAIS" in jobName or "CUSTOMER SERVICE" in jobName or "ESPECIALISTA | ESG" in jobName:
      return False

   return True

gupySearcher       = GupySearcher()
trakstarSearcher   = TrakstarSearcher()
ameDigitalSearcher = AmeDigitalSearcher()
hotmartSearcher    = HotmartSearcher()
spotifySearcher    = SpotifySearcher()
netflixSearcher    = NetflixSearcher()
nubankSearcher     = NubankSearcher()
sapSearcher        = SapSearcher()
paypalSearcher     = PaypalSearcher()
whatsAppSearcher   = WhatsAppSearcher()
tractianSearcher   = TractianSearcher()
ibmSearcher        = IbmSearcher()
dellSeacher        = DellSeacher()
nextBankSeacher    = NextBankSeacher()
iFoodSearcher      = IFoodSearcher()
amazonSearcher     = AmazonSearcher()

gupySearcher.search(
   'Ambev',
   'https://ambevtech.gupy.io/'
)

for job in gupySearcher.jobs:
   if not job.workplace:
      job.workplace = 'Remote Work'

gupySearcher.search(
   'Sicredi',
   'https://sicredi.gupy.io/',
   [ "Arquitetura Corporativa de TI", "Infraestrutura e operações TI", "Sistemas de TI" ]
)

gupySearcher.search(
   'Randon Digital',
   'https://randondigital.gupy.io/'
)

gupySearcher.search(
   'TOTVS',
   'https://totvs.gupy.io/',
   [ 'Tech | Frame, Engenharia e  Desenvolvimento', 'Tech | Segmentos, Financial e Digital', 'Tech | TI' ]
)

gupySearcher.search(
   'Promob',
   'https://promob.gupy.io/'
)

gupySearcher.search(
   'Picpay',
   'https://picpay.gupy.io/',
   [ 'Tecnologia' ]
)

gupySearcher.search(
   'Grupo Alura',
   'https://grupoalura.gupy.io/',
   [ 'Tecnologia' ]
)

gupySearcher.search(
   'B2W - Americanas',
   'https://b2w.gupy.io/',
   [ 'Dados', 'Desenvolvimento', 'Experiência do Usuário', 'Infraestrutura', 'Segurança da Informação', 'Suporte' ]
)

gupySearcher.search(
   'SiDi',
   'https://sidi.gupy.io/',
)

gupySearcher.search(
   'eSales',
   'https://esales.gupy.io/',
)

trakstarSearcher.search('Globo', 'https://vempraglobo.hire.trakstar.com/?q=&limit=1000')

ameDigitalSearcher.search()

hotmartSearcher.search()

spotifySearcher.search()

netflixSearcher.search()

nubankSearcher.search()

sapSearcher.search()

paypalSearcher.search()

whatsAppSearcher.search()

tractianSearcher.search()

ibmSearcher.search()

dellSeacher.search()

nextBankSeacher.search()

iFoodSearcher.search()

amazonSearcher.search()

allJobs: List[Job] = gupySearcher.jobs + trakstarSearcher.jobs + ameDigitalSearcher.jobs + \
   hotmartSearcher.jobs + spotifySearcher.jobs + netflixSearcher.jobs + nubankSearcher.jobs + \
   sapSearcher.jobs + paypalSearcher.jobs + whatsAppSearcher.jobs + tractianSearcher.jobs + ibmSearcher.jobs + \
   dellSeacher.jobs + nextBankSeacher.jobs + iFoodSearcher.jobs

todayAvailableJobsUrl: List[str] = []

# ------- TODO Companies -------
# Oracle
# Amazon
# Mercado livre
# ebay
# shopify
# microsoft
# adobe
# magalu  -> https://carreiras.magazineluiza.com.br/times/Luizalabs
# google  -> https://careers.google.com/jobs/results/
# Uber
# Focco ERP: https://oportunidadesfocco.kretos.cc/

print("Conectando ao banco de dados...")

repo = Repository()
repo.connectToDb()

print("Processando novos empregos...")

for index, currentJob in enumerate(allJobs):
   
   print(" Processando " + str(index) + " de " + str(len(allJobs)))

   if not isValidJob(currentJob):
      print(" ---> Ignorado")
      continue
   
   todayAvailableJobsUrl.append(currentJob.url)
   
   exists = repo.jobUrlExists(currentJob.url)

   if not exists:
      print("Salvando novo emprego: " + currentJob.name + ' - ' + currentJob.company)
      
      if currentJob.origin == Origin.SPOTIFY:
         spotifySearcher.loadTags(currentJob)
      elif currentJob.origin == Origin.AME_DIGITAL:
         ameDigitalSearcher.loadTags(currentJob)
      elif currentJob.origin == Origin.TRAKSTAR:
         trakstarSearcher.loadTags(currentJob)
      elif currentJob.origin == Origin.GUPY:
         gupySearcher.loadTags(currentJob)
      elif currentJob.origin == Origin.NUBANK:
         nubankSearcher.loadTags(currentJob)
      elif currentJob.origin == Origin.SAP:
         sapSearcher.loadTags(currentJob)
      elif currentJob.origin == Origin.PAYPAL:
         paypalSearcher.loadTags(currentJob)
      elif currentJob.origin == Origin.WHATSAPP:
         whatsAppSearcher.loadDetais(currentJob)
      elif currentJob.origin == Origin.IBM:
         ibmSearcher.loadTags(currentJob)
      elif currentJob.origin == Origin.DELL:
         dellSeacher.loadTags(currentJob)
      elif currentJob.origin == Origin.NEXT:
         nextBankSeacher.loadTags(currentJob)
      elif currentJob.origin == Origin.IFOOD:
         iFoodSearcher.loadTags(currentJob)

      repo.insertJob(currentJob)

print("Processando empregos existentes...")

availableJobsUrls = repo.getAllJobsUrls()

for index, url in enumerate(availableJobsUrls):

   print(" Processando " + str(index) + " de " + str(len(availableJobsUrls)))
   
   if url not in todayAvailableJobsUrl:
      print("Removendo emprego: " + url)
      repo.removeJobByUrl(url)

print("Gerando JSON para o website...")

jobs = repo.getAllJobs()

jsonData = json.dumps(jobs, indent=2, default=vars)

with open("./data/jobs.json", "w") as f:
   f.write(jsonData)

repo.closeDb()
