
import json
from typing import Any, List
import helpers
from repository.firebase_repo import Repository as FirebaseRepository
from job import Job, Origin
from searcher import Searcher
from base_repo import Repository

from searchers.amazon import AmazonSearcher
from searchers.dell import DellSearcher
from searchers.gupy import GupySearcher
from searchers.ame_digital import AmeDigitalSearcher
from searchers.hotmart import HotmartSearcher
from searchers.ibm import IbmSearcher
from searchers.ifood import IFoodSearcher
from searchers.netflix import NetflixSearcher
from searchers.next_bank import NextBankSearcher
from searchers.nubank import NubankSearcher
from searchers.sap import SapSearcher
from searchers.spotify import SpotifySearcher
from searchers.tractian import TractianSearcher
from searchers.globo import GloboSearcher
from searchers.paypal import PaypalSearcher
from searchers.whatsapp import WhatsAppSearcher
from searchers.docker import DockerSearcher

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

def processJobs(companyName: str, allJobs: List[Job], searcher: Searcher, repo: Repository):
   
   jobs = [ job for job in allJobs if isValidJob(job) ]
   
   print("- Found " + str(len(jobs)) + " jobs after filter (Original count: " + str(len(allJobs)) + ")")
   helpers.waitRandom()
   
   availableJobsUrl = []
   jobsToInsert = []
   
   for currentJob in jobs:
      
      availableJobsUrl.append(currentJob.url)
      
      if repo.jobUrlExists(currentJob.url):
         continue

      try:
         print("Loading tags for job: " + currentJob.name)
         searcher.loadDetails(currentJob)
         helpers.waitRandom()
      except Exception as e:
         print("Error: " + str(e))
         return

      jobsToInsert.append(currentJob)
      
   if len(jobsToInsert) == 0:
      print("- No new jobs")
   else:
      print("- Inserting " + str(len(jobsToInsert)) + " new jobs")
   
   for job in jobsToInsert:
      repo.insertJob(job)

   jobUrlsInDb = [ job.url for job in repo.getAllJobsByCompany(companyName) ]

   print("- Checking and deleting jobs that are not available anymore")
   deletedCount = 0
   
   for jobUrl in jobUrlsInDb:

      if jobUrl in availableJobsUrl:
         continue

      deletedCount += 1
      repo.removeJobByUrl(jobUrl)

   if deletedCount > 0:
      print("- Deleted " + str(deletedCount) + " jobs")

def loadGupyJobs(repo: Repository):

   gupyCompanies: List[List[Any]] = [
      [ 'Ambev', 'https://ambevtech.gupy.io/', 'Remote Work' ],
      [ 'Sicredi', 'https://sicredi.gupy.io/', None, [ "Arquitetura Corporativa de TI", "Infraestrutura e operações TI", "Sistemas de TI" ] ],
      [ 'Randon Digital', 'https://randondigital.gupy.io/' ],
      [ 'TOTVS', 'https://totvs.gupy.io/', None, [ 'Tech | Frame, Engenharia e  Desenvolvimento', 'Tech | Segmentos, Financial e Digital', 'Tech | TI' ] ],
      [ 'Promob', 'https://promob.gupy.io/' ],
      [ 'Picpay', 'https://picpay.gupy.io/', None, [ 'Tecnologia' ] ],
      [ 'Grupo Alura', 'https://grupoalura.gupy.io/', None, [ 'Tecnologia' ] ],
      [ 'B2W - Americanas', 'https://b2w.gupy.io/', None, [ 'Dados', 'Desenvolvimento', 'Experiência do Usuário', 'Infraestrutura', 'Segurança da Informação', 'Suporte' ] ],
      [ 'SiDi', 'https://sidi.gupy.io/' ],
      [ 'eSales', 'https://esales.gupy.io/' ],
   ]

   searcher = GupySearcher()
   
   for comp in gupyCompanies:
      
      companyName       = comp[0]
      companyUrl        = comp[1]
      defaultWorkplace  = comp[2] if len(comp) > 2 else None
      departments       = comp[3] if len(comp) > 3 else []
      workplaces        = comp[4] if len(comp) > 4 else []
      
      print()
      print("Loading jobs from Gupy: " + companyName + ' - ' + companyUrl)

      try:
         jobs = searcher.searchWithParams(companyName, companyUrl, departments, workplaces)
      except Exception as e:
         print("Error: " + str(e))
         continue

      if defaultWorkplace is not None:
         for job in jobs:
            if not job.workplace:
               job.workplace = defaultWorkplace
      
      processJobs(companyName, jobs, searcher, repo)
      

def loadOtherJobs(repo: Repository):

   searchers: List[Searcher] = [
      AmazonSearcher(),
      GloboSearcher(),
      AmeDigitalSearcher(),
      HotmartSearcher(),
      SpotifySearcher(),
      NetflixSearcher(),
      NubankSearcher(),
      SapSearcher(),
      PaypalSearcher(),
      WhatsAppSearcher(),
      TractianSearcher(),
      IbmSearcher(),
      DellSearcher(),
      NextBankSearcher(),
      IFoodSearcher(),
      DockerSearcher()
   ]
   
   for searcher in searchers:

      companyName = searcher.getCompanyName()
      
      print()
      print("Loading jobs from " + companyName)
      
      try:
         allJobs = searcher.search()
      except Exception as e:
         print("Error: " + str(e))
         continue

      processJobs(companyName, allJobs, searcher, repo)
      

def generateJson(repo: Repository):

   print("Gerando JSON para o website...")

   jobs = repo.getAllJobs()

   jsonData = json.dumps(jobs, indent=2, default=vars)

   with open("./data/jobs.json", "w") as f:
      f.write(jsonData)


def main():

   # ------- TODO Companies -------
   # Oracle          -> https://oracle.taleo.net/careersection/2/jobsearch.ftl?f=LOCATION(362940031553)
   # Mercado livre
   #  -> Remote:     https://mercadolibre.eightfold.ai/api/apply/v2/jobs?domain=mercadolibre.com&start=0&num=1000&location=remote&department=IT&pid=10296687&domain=mercadolibre.com&triggerGoButton=false
   #  -> not remote: https://mercadolibre.eightfold.ai/api/apply/v2/jobs?domain=mercadolibre.com&start=0&num=1000&location=Brasil&department=IT&pid=10296687&domain=mercadolibre.com&triggerGoButton=false
   # microsoft
   # adobe
   # magalu  -> https://carreiras.magazineluiza.com.br/times/Luizalabs
   # google  -> https://careers.google.com/jobs/results/
   # Uber
   # Focco ERP: https://oportunidadesfocco.kretos.cc/

   print("Connection to database...")
   repo = FirebaseRepository()
   repo.connectToDb()

   loadGupyJobs(repo)
   
   loadOtherJobs(repo)

   generateJson(repo)

   repo.closeDb()
   

if __name__ == "__main__":
   main()
