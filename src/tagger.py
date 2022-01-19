
import re
from typing import List
from unidecode import unidecode

class Tag:
   
   def __init__(self, name: str, words: List[str]):
      self.name = name
      self.words = words

class Tagger:
   
   tags = [
      
      # Web
      Tag('PHP', [ 'PHP' ]),
      Tag('HTML', [ 'HTML', 'HTML5' ]),
      Tag('CSS', [ 'CSS', 'CSS3' ]),
      Tag('JS', [ 'JAVASCRIPT' ]),
      Tag('TS', [ 'TYPESCRIPT' ]),
      
      # Frameworks Web
      Tag('AngularJS', [ 'ANGULARJS' ]),
      Tag('Angular', [ 'ANGULAR' ]),
      Tag('ReactJS', [ 'REACT', 'REACTJS' ]),
      Tag('Ember', [ 'EMBER' ]),
      Tag('VueJS', [ 'VUE', 'VUEJS' ]),
      Tag('NodeJs', [ 'NODE.JS', 'NODEJS' ]),
      
      # Apis
      Tag('API', [ 'APIS', 'REST', 'WEB SERVICE', 'WEB SERVICES', 'REST APIs' ]),
      Tag('Webservice', [ 'WEB SERVICE', 'WEB SERVICES', 'WEBSERVICE', 'WEBSERVICES' ]),
      Tag('Postman', [ 'POSTMAN' ]),
      
      # Mobile
      Tag('Mobile', [ 'MOBILE', 'ANDROID', 'FLUTTER' ]),
      Tag('Android', [ 'ANDROID' ]),
      Tag('Kotlin', [ 'KOTLIN' ]),
      Tag('PWA', [ 'PWA' ]),
      Tag('React Native', [ 'REACT NATIVE' ]),
      Tag('Swift', [ 'SWIFT' ]),
      Tag('Objective-C', [ 'OBJECTIVE-C', 'OBJECTIVE C' ]),
      
      # Desktop
      Tag('Java', [ 'JAVA' ]),
      Tag('Gradle', [ 'GRADLE' ]),
      Tag('Python', [ 'PYTHON' ]),
      Tag('C# / .NET', [ 'C#', '.NET' ]),
      Tag('Golang', [ 'GO', 'GOLANG' ]),
      
      # Operating Systems
      Tag('Linux', [ 'LINUX' ]),

      # Databases
      Tag('SQL', [ 'BANCO DE DADOS RELACIONAL', 'SQL' ]),
      Tag('NoSQL', [ 'NAO RELACIONAL', 'NOSQL' ]),
      Tag('SqlServer', [ 'SQLSERVER' ]),
      Tag('Postgres', [ 'POSTGRES', 'POSTGRESQL' ]),
      Tag('Mongo', [ 'MONGODB', 'MONGO' ]),
      Tag('Oracle', [ 'ORACLE' ]),

      # Containers
      Tag('Docker', [ 'DOCKER' ]),
      Tag('Kubernetes', [ 'KUBERNETES' ]),
      
      # Teory
      Tag('Agile Develop.', [ 'AGEIS', 'SCRUM', 'KANBAN' ]),
      Tag('Design Patterns', [ 'DESIGN PATTERNS' ]),
      Tag('Clean Code', [ 'CLEAN CODE' ]),
      Tag('Data Structure', [ 'ESTRUTURAS DE DADOS' ]),
      Tag('CI/CD', [ 'CI / CD', 'CI/CD' ]),
      Tag('Project management', [ 'GESTAO DE PROJETOS' ]),
      Tag('Product management', [ 'GESTAO DE PRODUTOS' ]),
      Tag('Securiry', [ 'SEGURANCA' ]),
      Tag('Requirements analysis', [ 'ANALISE DE REQUISITOS' ]),
      Tag('Quality analysis', [ 'ANALISTA DE QUALIDADE' ]),
      Tag('Dependence analysis', [ 'GERENCIAMENTO DE DEPENDÊNCIAS' ]),
      Tag('Distributed systems', [ 'SISTEMAS DISTRIBUÍDOS' ]),
      Tag('Microservices', [ 'MICROSSERVIÇOS', 'MICRO SERVIÇOS' ]),
      
      # Tests
      Tag('Unit testing', [ 'TESTES UNITARIOS' ]),
      Tag('Automated testing', [ 'TESTES AUTOMATIZADOS', 'AUTOMACAO DE TESTES' ]),
      Tag('Tests', [ 'PLANO DE TESTES', 'CENARIOS DE TESTE' ]),
      Tag('Cypress', [ 'CYPRESS' ]),
      Tag('Web tests', [ 'TESTES WEB' ]),
      Tag('API tests', [ 'TESTES DE API' ]),
      
      # Others
      Tag('ETL', [ 'TRANSFORMACAO DE DADOS', 'MANIPULACAO DE DADOS' ]),
      Tag('Git', [ 'GIT', 'GITHUB' ]),
      Tag('Bundlers', [ 'BUNDLERS', 'WEBPACK', 'BABEL' ]),
      Tag('Front End', [ 'FRONT-END', 'FRONT END', 'FRONTEND' ]),
      Tag('Message broker', [ 'MENSAGERIAS', 'RABBITMQ', 'AZURESERVICEBUS' ]),
      Tag('Azure', [ 'AZURE' ]),
      Tag('SAP', [ 'SAP' ]),
      Tag('Machine learning', [ 'MACHINE LEARNING' ]),
      Tag('Pipelines', [ 'PIPELINES' ]),
      Tag('Azure Datafactory', [ 'AZURE DATAFACTORY' ]),
      Tag('AWS', [ 'AWS' ]),
      Tag('ElasticSearch', [ 'ELASTICSEARCH' ]),
      Tag('Power BI', [ 'POWER BI' ]),

      # UI
      Tag('Figma', [ 'FIGMA' ]),
      Tag('Illustrator', [ 'ILLUSTRATOR' ]),
      
   ]

   def __init__(self) -> None:
      self.wordRe = re.compile('\\w')
   
   def generateTags(self, text: str) -> List[str]:
      
      text = unidecode(text.upper())
      
      tags: List[str] = []
      
      for tag in self.tags:
         
         hasTag = False
         
         for word in tag.words:
            
            startIndex = 0
            
            while True:
               
               index = text.find(word, startIndex)
               
               if index == -1:
                  break
               
               startIndex = index + 1
               
               if index > 0 and self.wordRe.match(text[index - 1]) is not None:
                  continue
               
               if index < text.__len__() and self.wordRe.match(text[index + word.__len__()]) is not None:
                  continue
               
               hasTag = True
               break
         
            if hasTag:
               break
         
         if hasTag:
            tags.append(tag.name)
      
      # TODO Check for english level
      
      return tags
      
