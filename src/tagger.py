
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
      Tag('Laravel', [ 'LARAVEL' ]),
      Tag('HTML', [ 'HTML', 'HTML5' ]),
      Tag('CSS', [ 'CSS', 'CSS3' ]),
      Tag('SCSS/SASS', [ 'SCSS', 'SASS' ]),
      Tag('JS', [ 'JAVASCRIPT', 'JS' ]),
      Tag('JSX', [ 'JSX' ]),
      Tag('TS', [ 'TYPESCRIPT', 'TS' ]),
      Tag('Eslint', [ 'ESLINT' ]),
      Tag('AngularJS', [ 'ANGULARJS' ]),
      Tag('Angular', [ 'ANGULAR' ]),
      Tag('ReactJS', [ 'REACT', 'REACTJS' ]),
      Tag('Ember', [ 'EMBER' ]),
      Tag('VueJS', [ 'VUE', 'VUEJS', 'VUE.JS' ]),
      Tag('WebSockets', [ 'WEBSOCKETS' ]),
      Tag('Next.js', [ 'NEXT.JS', 'NEXTJS' ]),
      Tag('Express', [ 'EXPRESS' ]),
      Tag('Svelte', [ 'SVELTE' ]),
      Tag('Bootstrap', [ 'BOOTSTRAP' ]),
      Tag('Foundation', [ 'FOUNDATION', 'FOUNDATIONCSS' ]),
      Tag('Tailwind', [ 'TAILWIND' ]),
      Tag('Django ', [ 'DJANGO ' ]),
      Tag('Symfony', [ 'SYMFONY' ]),
      Tag('Webhooks', [ 'WEBHOOKS' ]),
      
      # Apis
      Tag('API', [ 'APIS', 'REST', 'WEB SERVICE', 'WEB SERVICES', 'REST APIs', "API's" ]),
      Tag('Webservice', [ 'WEB SERVICE', 'WEB SERVICES', 'WEBSERVICE', 'WEBSERVICES' ]),
      Tag('Postman', [ 'POSTMAN' ]),
      Tag('SOAP', [ 'SOAP' ]),
      
      # Mobile
      Tag('Flutter', [ 'FLUTTER' ]),
      Tag('Ionic', [ 'IONIC' ]),
      Tag('Android', [ 'ANDROID' ]),
      Tag('Kotlin', [ 'KOTLIN' ]),
      Tag('PWA', [ 'PWA' ]),
      Tag('React Native', [ 'REACT NATIVE' ]),
      Tag('Swift', [ 'SWIFT' ]),
      Tag('SwiftUI', [ 'SWIFTUI' ]),
      Tag('Objective-C', [ 'OBJECTIVE-C', 'OBJECTIVE C' ]),
      Tag('Xamarin', [ 'XAMARIN' ]),

      # Desktop / Scripts
      Tag('C/C++', [ 'C++', 'C/C++' ]),
      Tag('Java', [ 'JAVA' ]),
      Tag('Gradle', [ 'GRADLE' ]),
      Tag('Maven', [ 'MAVEN' ]),
      Tag('Python', [ 'PYTHON', 'PHYTON' ]),
      Tag('PySpark', [ 'PYSPARK' ]),
      Tag('Scala', [ 'SCALA' ]),
      Tag('C# / .NET', [ 'C#', '.NET' ]),
      Tag('Golang', [ 'GO', 'GOLANG' ]),
      Tag('NodeJs', [ 'NODE.JS', 'NODEJS' ]),
      Tag('Npm', [ 'NPM' ]),
      Tag('Ruby', [ 'RUBY' ]),
      Tag('Rust', [ 'RUST' ]),
      Tag('Perl', [ 'PERL' ]),
      Tag('Haskell', [ 'HASKELL' ]),
      Tag('Lua', [ 'LUA' ]),
      Tag('Clojure', [ 'CLOJURE' ]),
      Tag('Elixir', [ 'ELIXIR' ]),
      Tag('Erlang', [ 'ERLANG' ]),
      Tag('Julia', [ 'JULIA' ]),
      Tag('OCaml', [ 'OCAML' ]),
      Tag('R lang', [ 'R' ]),
      Tag('Fiori', [ 'FIORI' ]),
      Tag('ABAP', [ 'ABAP' ]),
      Tag('Shell', [ 'SHELL', 'SH' ]),
      Tag('Springboot', [ 'SPRINGBOOT', 'SPRING BOOT' ]),
      Tag('Spring MVC', [ 'SPRING MVC' ]),
      Tag('Quarkus', [ 'QUARKUS' ]),
      Tag('gRPC', [ 'GRPC' ]),
      Tag('Progress', [ 'PROGRESS' ]),
      
      # Operating Systems
      Tag('Linux', [ 'LINUX' ]),

      # Databases
      Tag('SQL', [ 'BANCO DE DADOS RELACIONAL', 'BANCO DE DADOS RELACIONAIS', 'SQL', 'RELATIONAL DATABASES' ]),
      Tag('NoSQL', [ 'NAO RELACIONAL', 'NOSQL', 'NO-SQL' ]),
      Tag('SqlServer', [ 'SQLSERVER', 'SQL SERVER' ]),
      Tag('Postgres', [ 'POSTGRES', 'POSTGRESQL', 'POSTGREES' ]),
      Tag('MySQL', [ 'MYSQL' ]),
      Tag('Mongo', [ 'MONGODB', 'MONGO' ]),
      Tag('Oracle', [ 'ORACLE' ]),
      Tag('GraphQL', [ 'GRAPHQL' ]),
      Tag('Big Data', [ 'BIG DATA' ]),
      Tag('DynamoDB', [ 'DYNAMODB' ]),
      Tag('Datomic', [ 'DATOMIC' ]),
      Tag('Redis', [ 'REDIS', 'REDISDB' ]),
      Tag('Teradata', [ 'TERADATA' ]),
      Tag('Cassandra', [ 'CASSANDRA' ]),

      # Containers
      Tag('Docker', [ 'DOCKER' ]),
      Tag('Kubernetes', [ 'KUBERNETES' ]),
      
      # Teory
      Tag('Peer Programming.', [ 'PEER PROGRAMMING' ]),
      Tag('Agile Develop.', [ 'AGEIS', 'SCRUM', 'KANBAN', 'METODOLOGIA ÁGIL', 'AGILE METHODOLOGY' ]),
      Tag('Design Patterns', [ 'DESIGN PATTERNS' ]),
      Tag('Clean Code', [ 'CLEAN CODE' ]),
      Tag('Data Structure', [ 'ESTRUTURAS DE DADOS' ]),
      Tag('CI/CD', [ 'CI / CD', 'CI/CD', 'CD / I', 'CONTINUOUS DELIVERY' ]),
      Tag('Project management', [ 'GESTAO DE PROJETOS' ]),
      Tag('Product management', [ 'GESTAO DE PRODUTOS' ]),
      Tag('Requirements analysis', [ 'ANALISE DE REQUISITOS' ]),
      Tag('Quality analysis', [ 'ANALISTA DE QUALIDADE' ]),
      Tag('Dependence analysis', [ 'GERENCIAMENTO DE DEPENDÊNCIAS' ]),
      Tag('Distributed systems', [ 'SISTEMAS DISTRIBUÍDOS' ]),
      Tag('Microservices', [ 'MICROSSERVICOS', 'MICROSSERVIÇOS', 'MICRO SERVIÇOS', 'MICRO-SERVIÇOS' ]),
      
      # Tests
      Tag('Unit testing', [ 'TESTES UNITARIOS' ]),
      Tag('Automated testing', [ 'TESTES AUTOMATIZADOS', 'AUTOMACAO DE TESTES' ]),
      Tag('Tests', [ 'PLANO DE TESTES', 'CENARIOS DE TESTE' ]),
      Tag('Cypress', [ 'CYPRESS' ]),
      Tag('Web tests', [ 'TESTES WEB' ]),
      Tag('API tests', [ 'TESTES DE API' ]),
      Tag('TDD', [ 'TDD', 'TEST-DRIVEN DEVELOPMENT', 'DESENVOLVIMENTO ORIENTADO A TESTES' ]),

      # Security
      Tag('Pentests', [ 'PENETRATION TESTING', 'PENTESTS' ]),
      Tag('Segurança ofensiva', [ 'FERRAMENTAS OFENSIVAS', 'METASPLOIT FRAMEWORK', 'ETTERCAP', 'ACUNETIX', 'NEXPOSE', 'SQLMAP', 'AIRCRACK-NG' ]),
      
      # Others
      Tag('ETL', [ 'TRANSFORMACAO DE DADOS', 'MANIPULACAO DE DADOS', 'ETL' ]),
      Tag('Git', [ 'GIT' ]),
      Tag('Webpack', [ 'WEBPACK' ]),
      Tag('Babel', [ 'BABEL' ]),
      Tag('Front End', [ 'FRONT-END', 'FRONT END', 'FRONTEND' ]),
      Tag('Message broker', [ 'MENSAGERIAS', 'RABBITMQ', 'AZURESERVICEBUS' ]),
      Tag('Azure', [ 'AZURE' ]),
      Tag('SAP', [ 'SAP' ]),
      Tag('Machine learning', [ 'MACHINE LEARNING' ]),
      Tag('Pipelines', [ 'PIPELINES' ]),
      Tag('Azure Datafactory', [ 'AZURE DATAFACTORY' ]),
      Tag('AWS', [ 'AWS' ]),
      Tag('IBM Cloud', [ 'IBM CLOUD' ]),
      Tag('GCP', [ 'GCP', 'GOOGLE CLOUD' ]),
      Tag('i18n', [ 'i18n', 'I18N' ]),
      Tag('ElasticSearch', [ 'ELASTICSEARCH' ]),
      Tag('Power BI', [ 'POWER BI', 'POWERBI' ]),
      Tag('Open-source', [ 'OPEN-SOURCE' ]),
      Tag('Kafka', [ 'KAFKA' ]),
      Tag('VB.NET', [ 'VB.NET' ]),
      Tag('RPA', [ 'RPA' ]),
      Tag('ABAP', [ 'ABAP' ]),
      Tag('OpenShift', [ 'OPENSHIFT' ]),
      Tag('OAUTH', [ 'OAUTH', 'OAUTH2' ]),
      Tag('BI', [ 'POWER BI', 'METABASE', 'BUSINESS INTELLIGENCE', 'LOOKER', 'TABLEAU' ]),

      # UI
      Tag('Figma', [ 'FIGMA' ]),
      Tag('Illustrator', [ 'ILLUSTRATOR' ]),
      Tag('Photoshop', [ 'PHOTOSHOP' ]),

      # Big data
      Tag('Big Data', [ 'BIG DATA' ]),
      Tag('Spark', [ 'SPARK' ]),
      Tag('Hive', [ 'HIVE' ]),
      Tag('Tableau', [ 'TABLEAU' ]),
      Tag('Hadoop', [ 'HADOOP' ]),
      
   ]

   def __init__(self) -> None:
      self.wordRe = re.compile('\\w')
   
   def generateTags(self, text: str) -> List[str]:
      
      # TODO KAFKA tag not found
      # https://boards.greenhouse.io/nubank/jobs/2569175
      
      text = unidecode(text.upper())

      # Remove some terms that messes up the search of the Go tag
      text = text.replace('GO WRONG', '')
      text = text.replace('GO TO MARKET', '')
      text = text.replace('GO-TO-MARKET', '')
      text = text.replace('GO THROUGH', '')
      
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
               
               if index + len(word) < len(text) and self.wordRe.match(text[index + len(word)]) is not None:
                  continue
               
               hasTag = True
               break
         
            if hasTag:
               break
         
         if hasTag:
            tags.append(tag.name)
      
      # TODO Check for english level
      
      return tags
      
