
import json
import sys
from typing import Any, List
import helpers
from repository.firebase_repo import FirebaseRepository
from repository.sqlite_repo import SqliteRepository
from job import Job, Origin
from searcher import Searcher
from base_repo import Repository

from searchers.amazon import AmazonSearcher
from searchers.clear_sale import ClearSaleSearcher
from searchers.dell import DellSearcher
from searchers.gupy import GupySearcher
from searchers.ame_digital import AmeDigitalSearcher
from searchers.hotmart import HotmartSearcher
from searchers.ibm import IbmSearcher
from searchers.ifood import IFoodSearcher
from searchers.kenoby import KenobySearcher
from searchers.luizalabs import LuizaLabsSearcher
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

runOnlyCompanyName = ''
saveData = True

def isValidJob(job: Job) -> bool:

   jobName = " " + job.name.upper() + " "
   
   if "ESTAGIO" in jobName or 'ESTÁGIO' in jobName:
      return False

   if "BANCO" in jobName and "TALENTOS" in jobName:
      return False
   
   if job.origin == Origin.IFOOD and job.department == "" and len(job.tags) == 0:
      return False
   
   if job.origin == Origin.IBM and "APPLICATION DEVELOPER-SALESFORCE" in jobName:
      return False
   
   if len(job.tags) > 0 or len(job.differentialTags) > 0:
      return True
   
   if "ENGINEER" in jobName or "SOFTWARE" in jobName or "ENGENH" in jobName or "DESENV" in jobName or "DEVEL" in jobName or "DEV" in jobName:
      return True
   
   if "STACK" in jobName or "SATCK" in jobName or "FRONT" in jobName or "BACK" in jobName:
      return True

   if "DADOS" in jobName or "DATA" in jobName:
      return True
   
   if "WEB" in jobName:
      return True
   
   if "DBA" in jobName or "DATABASE" in jobName or "DBRE" in jobName:
      return True

   if " TI " in jobName:
      return True
   
   if "EX" in jobName:
      return True

   if "ANALISTA DE BI" in jobName:
      return True

   if "CLOUD" in jobName or "DEVOPS" in jobName:
      return True
   
   if "ENGENHEIRO DE SUPORTE" in jobName or "PROFISSIONAL DE SUPORTE TÉCNICO" in jobName:
      return False

   if "ANALISTA DE RECURSOS HUMANOS" in jobName:
      return False
   
   if "INTRAEMPREENDEDOR(A) DE NOVOS NEGÓCIOS/PRODUTOS" in jobName:
      return False

   return False

def processJobs(companyName: str, allJobs: List[Job], searcher: Searcher, repo: Repository):
   
   global saveData
   
   jobs = [ job for job in allJobs if isValidJob(job) ]
   
   if not saveData:
      
      print("---------------------------------------")
      print(companyName + " - Found " + str(len(jobs)) + " jobs after filter (Original count: " + str(len(allJobs)) + ")")
      print("---------------------------------------")
      
      for job in allJobs:
         print( ("YES - " if (isValidJob(job)) else "NO  - "), job)
      
      return
   
   print("- Found " + str(len(jobs)) + " jobs after filter (Original count: " + str(len(allJobs)) + ")")
   helpers.waitRandom()
   
   availableJobsUrl: List[str] = []
   jobsToInsert: List[Job] = []
   
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
   
   if saveData:
      for job in jobsToInsert:
         try:
            repo.insertJob(job)
         except Exception as e:
            print("Error: " + str(e))
            return

   jobUrlsInDb = [ job.url for job in repo.getAllJobsByCompany(companyName) ]

   print("- Checking and deleting jobs that are not available anymore")
   deletedCount = 0
   
   if saveData:
      for jobUrl in jobUrlsInDb:

         if jobUrl in availableJobsUrl:
            continue

         deletedCount += 1
         repo.removeJobByUrl(jobUrl)

      if deletedCount > 0:
         print("- Deleted " + str(deletedCount) + " jobs")

def loadKenobyJobs(repo: Repository):
   
   global runOnlyCompanyName

   kenobyCompanies = [
      [ 'DB1 Group', 'https://jobs.kenoby.com/vagas-db1-group/position?search=&utm_source=website', [ 'Desenvolvimento', 'Tech' ], True ],
      [ 'Kabum', 'https://jobs.kenoby.com/kabum/position?search=&utm_source=website', [ 'TI' ], True ]
   ]
   
   searcher = KenobySearcher()

   for comp in kenobyCompanies:

      companyName: str = comp[0]
      htmlUrl: str = comp[1]
      segmentsToFilter: List[str] = comp[2]
      onlyRemote: bool = comp[3]

      if len(runOnlyCompanyName) > 0 and companyName.lower() != runOnlyCompanyName.lower():
         continue
      
      print()
      print("Loading jobs from Gupy: " + companyName + ' - ' + htmlUrl)

      try:
         jobs = searcher.searchWithParams(companyName, htmlUrl, segmentsToFilter, onlyRemote)
      except Exception as e:
         print("Error: " + str(e))
         continue
   
      processJobs(companyName, jobs, searcher, repo)


def loadGupyJobs(repo: Repository):

   global runOnlyCompanyName

   gupyCompanies: List[List[Any]] = [
      [ 'Ambev', 'https://ambevtech.gupy.io/', 'Remote Work' ],
      [ 'Sicredi', 'https://sicredi.gupy.io/', None, [ "Arquitetura Corporativa de TI", "Infraestrutura e operações TI", "Sistemas de TI" ] ],
      [ 'Randon Digital', 'https://randondigital.gupy.io/' ],
      # [ 'TOTVS', 'https://totvs.gupy.io/', None, [ 'Tech | Frame, Engenharia e  Desenvolvimento', 'Tech | Segmentos, Financial e Digital', 'Tech | TI' ] ],
      [ 'Promob', 'https://promob.gupy.io/' ],
      [ 'Picpay', 'https://picpay.gupy.io/', None, [ 'Tecnologia' ] ],
      [ 'Grupo Alura', 'https://grupoalura.gupy.io/', None, [ 'Tecnologia' ] ],
      [ 'B2W - Americanas', 'https://b2w.gupy.io/', None, [ 'Dados', 'Desenvolvimento', 'Experiência do Usuário', 'Infraestrutura', 'Segurança da Informação', 'Suporte' ] ],
      [ 'SiDi', 'https://sidi.gupy.io/' ],
      [ 'eSales', 'https://esales.gupy.io/' ],
      [ 'Linx', 'https://linx.gupy.io/', None, [], [], True ],
      [ 'Webmotors', 'https://webmotors.gupy.io/', None, [ 'Tecnologia' ], [], True ],
      [ 'Gupy', 'https://tech-career.gupy.io/' ],
      [ 'Caju Benefícios', 'https://caju.gupy.io/', None, [ 'Tecnologia' ], [], True ],
   ]

   searcher = GupySearcher()
   
   for comp in gupyCompanies:
      
      companyName       = comp[0]
      companyUrl        = comp[1]
      defaultWorkplace  = comp[2] if len(comp) > 2 else None
      departments       = comp[3] if len(comp) > 3 else []
      workplaces        = comp[4] if len(comp) > 4 else []
      onlyRemote        = comp[5] if len(comp) > 5 else False
      
      if len(runOnlyCompanyName) > 0 and companyName.lower() != runOnlyCompanyName.lower():
         continue
      
      print()
      print("Loading jobs from Gupy: " + companyName + ' - ' + companyUrl)

      try:
         jobs = searcher.searchWithParams(companyName, companyUrl, departments, workplaces, onlyRemote)
      except Exception as e:
         print("Error: " + str(e))
         continue

      if defaultWorkplace is not None:
         for job in jobs:
            if not job.workplace:
               job.workplace = defaultWorkplace
      
      processJobs(companyName, jobs, searcher, repo)
      

def loadOtherJobs(repo: Repository):

   global runOnlyCompanyName

   searchers: List[Searcher] = [
      ClearSaleSearcher(),
      LuizaLabsSearcher(),
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

      if len(runOnlyCompanyName) > 0 and companyName.lower() != runOnlyCompanyName.lower():
         continue
      
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


def saveUniqueCompaniesAndTags(repo: Repository):
   
   print("Looking for unique companies and tags")
   
   jobs = repo.getAllJobs()
   tags = []
   companies = []
   
   for job in jobs:

      foundCompany = False

      for index, comp in enumerate(companies):
         if comp['name'] == job.company:
            companies[index]['jobCount'] += 1
            foundCompany = True
            break
      
      if not foundCompany:
         companies.append({
            "name": job.company,
            "jobCount": 1
         })
      
      for jobTag in job.tags:

         foundTag = False

         for index, tag in enumerate(tags):
            if tag['name'] == jobTag:
               tags[index]['jobCount'] += 1
               foundTag = True
               break

         if not foundTag:
            tags.append({
               "name": jobTag,
               "jobCount": 1
            })
      
   print("Saving unique companies")
   companies.sort(key=lambda comp: comp['name'])
   repo.saveUniqueCompanies(companies)

   print("Saving unique tags")
   tags.sort(key=lambda tag: tag['name'])
   repo.saveUniqueTags(tags)
      
def main():

   global runOnlyCompanyName, saveData
   
   if len(sys.argv) > 1:
      
      if sys.argv[1] == '-h' or sys.argv[1] == '--help':
         print("Usage: python3 src/main.py [-c <company name>] [--no-save]")
         sys.exit(1)
      
      i = 1
      while i < len(sys.argv):
         
         if sys.argv[i] == "--no-save":
            saveData = False
            i += 1
            continue
         
         if sys.argv[i] == "-c":
            
            if len(sys.argv) == i + 1:
               print("Error: company name not informed")
               sys.exit(1)
            
            i += 1
            runOnlyCompanyName = sys.argv[i]

            i += 1
            continue

         print("Unknown argument: " + sys.argv[i])
         sys.exit(1)
      
   print("Connection to database...")
   repo = FirebaseRepository()
   repo.connectToDb()

   loadGupyJobs(repo)

   loadKenobyJobs(repo)
   
   loadOtherJobs(repo)
   
   if saveData:
      saveUniqueCompaniesAndTags(repo)

   repo.closeDb()
   

if __name__ == "__main__":
   main()
