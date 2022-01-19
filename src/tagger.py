
import re
from unidecode import unidecode

class Tag:
   
   def __init__(self, name, words):
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
      Tag('Api', [ 'APIS', 'REST', 'WEB SERVICE', 'WEB SERVICES', 'REST APIs' ]),
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

      # Banco de dados
      Tag('DBs Relacionais', [ 'BANCO DE DADOS RELACIONAL', 'SQL' ]),
      Tag('DBs não relacionais', [ 'NAO RELACIONAL' ]),
      Tag('SqlServer', [ 'SQLSERVER' ]),
      Tag('Postgres', [ 'POSTGRES', 'POSTGRESQL' ]),
      Tag('Mongo', [ 'MONGODB', 'MONGO' ]),
      Tag('Oracle', [ 'ORACLE' ]),

      # Containers
      Tag('Docker', [ 'DOCKER' ]),
      Tag('Kubernetes', [ 'KUBERNETES' ]),
      
      # Teoria
      Tag('Metod. Ágeis', [ 'AGEIS', 'SCRUM', 'KANBAN' ]),
      Tag('Design Patterns', [ 'DESIGN PATTERNS' ]),
      Tag('Clean Code', [ 'CLEAN CODE' ]),
      Tag('Estruturas de dados', [ 'ESTRUTURAS DE DADOS' ]),
      Tag('CI/CD', [ 'CI / CD', 'CI/CD' ]),
      Tag('Gestão de Projetos', [ 'GESTAO DE PROJETOS' ]),
      Tag('Gestão de Produtos', [ 'GESTAO DE PRODUTOS' ]),
      Tag('Segurança', [ 'SEGURANCA' ]),
      Tag('Regras de negócio', [ 'REGRAS DE NEGOCIO' ]),
      Tag('Análise de requisitos', [ 'ANALISE DE REQUISITOS' ]),
      Tag('Analista de Qualidade', [ 'ANALISTA DE QUALIDADE' ]),
      Tag('Gerenc. dependências', [ 'GERENCIAMENTO DE DEPENDÊNCIAS' ]),
      Tag('Sistemas Distribuídos', [ 'SISTEMAS DISTRIBUÍDOS' ]),
      Tag('Microsserviços', [ 'MICROSSERVIÇOS', 'MICRO SERVIÇOS' ]),
      
      # Testes
      Tag('Testes Unitários', [ 'TESTES UNITARIOS' ]),
      Tag('Testes Automatizados', [ 'TESTES AUTOMATIZADOS', 'AUTOMACAO DE TESTES' ]),
      Tag('Testes', [ 'PLANO DE TESTES', 'CENARIOS DE TESTE' ]),
      Tag('Cypress', [ 'CYPRESS' ]),
      Tag('Testes Web', [ 'TESTES WEB' ]),
      Tag('Testes API', [ 'TESTES DE API' ]),
      
      # Data science
      Tag('Transformação de dados', [ 'TRANSFORMACAO DE DADOS', 'MANIPULACAO DE DADOS' ]),
      
      # Outros
      Tag('Git', [ 'GIT', 'GITHUB' ]),
      Tag('Bundlers', [ 'BUNDLERS', 'WEBPACK', 'BABEL' ]),
      Tag('Front End', [ 'FRONT-END', 'FRONT END', 'FRONTEND' ]),
      Tag('Mensagerias', [ 'MENSAGERIAS', 'RABBITMQ', 'AZURESERVICEBUS' ]),
      Tag('Azure', [ 'AZURE' ]),
      Tag('SAP', [ 'SAP' ]),
      Tag('Machine Learning', [ 'MACHINE LEARNING' ]),
      Tag('Pipelines', [ 'PIPELINES' ]),
      Tag('Azure Datafactory', [ 'AZURE DATAFACTORY' ]),
      Tag('AWS', [ 'AWS' ]),
      Tag('ElasticSearch', [ 'ELASTICSEARCH' ]),
      Tag('Power BI', [ 'POWER BI' ]),

      # UI
      Tag('Figma', [ 'FIGMA' ]),
      Tag('Illustrator', [ 'ILLUSTRATOR' ]),
      
   ]

   def __init__(self):
      self.wordRe = re.compile('\\w')
   
   def generateTags(self, text: str):
      
      text = unidecode(text.upper())
      
      tags = []
      
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
      
