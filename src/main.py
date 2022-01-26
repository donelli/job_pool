
import json
from time import sleep, time
from traceback import print_tb
from typing import List
from gupy import GupySearcher
from ame_digital import AmeDigitalSearcher
from hotmart import HotmartSearcher
from netflix import NetflixSearcher
from nubank import NubankSearcher
from repository import Repository
from job import Job, Origin
from sap import SapSearcher
from spotify import SpotifySearcher
from trakstar import TrakstarSearcher
from paypal import PaypalSearcher

gupySearcher       = GupySearcher()
trakstarSearcher   = TrakstarSearcher()
ameDigitalSearcher = AmeDigitalSearcher()
hotmartSearcher    = HotmartSearcher()
spotifySearcher    = SpotifySearcher()
netflixSearcher    = NetflixSearcher()
nubankSearcher     = NubankSearcher()
sapSearcher        = SapSearcher()
paypalSearcher     = PaypalSearcher()

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
   'https://totvs.gupy.io/'
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

trakstarSearcher.search('Globo', 'https://vempraglobo.hire.trakstar.com/?q=&limit=1000')

ameDigitalSearcher.search()

hotmartSearcher.search()

spotifySearcher.search()

netflixSearcher.search()

nubankSearcher.search()

sapSearcher.search()

paypalSearcher.search()

allJobs: List[Job] = gupySearcher.jobs + trakstarSearcher.jobs + ameDigitalSearcher.jobs + \
   hotmartSearcher.jobs + spotifySearcher.jobs + netflixSearcher.jobs + nubankSearcher.jobs + \
   sapSearcher.jobs + paypalSearcher.jobs

# TODO magalu  -> https://carreiras.magazineluiza.com.br/times/Luizalabs

# TODO google  -> https://careers.google.com/jobs/results/

# TODO Uber ?

# Focco ERP: https://oportunidadesfocco.kretos.cc/

print("Conectando ao banco de dados...")

repo = Repository()
repo.connectToDb()

print("Processando novos empregos...")

for index, currentJob in enumerate(allJobs):
   
   print(" Processando " + str(index) + " de " + str(len(allJobs)))
   
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

      repo.insertJob(currentJob)

print("Processando empregos existentes...")

availableJobsUrls = repo.getAllJobsUrls()

for index, url in enumerate(availableJobsUrls):

   print(" Processando " + str(index) + " de " + str(len(allJobs)))
   
   isAvailable = False

   if url in availableJobsUrls:
      isAvailable = True

   if not isAvailable:
      print("Removendo emprego: " + url)
      repo.removeJobByUrl(url)

print("Gerando JSON para o website...")

jobs = repo.getAllJobs()

jsonData = json.dumps(jobs, indent=2, default=vars)

with open("./data/jobs.json", "w") as f:
   f.write(jsonData)

repo.closeDb()
