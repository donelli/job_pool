
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
      Tag('JS', [ 'JAVASCRIPT', 'JS' ]),
      Tag('TS', [ 'TYPESCRIPT', 'TS' ]),
      Tag('Eslint', [ 'ESLINT' ]),
      Tag('AngularJS', [ 'ANGULARJS' ]),
      Tag('Angular', [ 'ANGULAR' ]),
      Tag('ReactJS', [ 'REACT', 'REACTJS' ]),
      Tag('Ember', [ 'EMBER' ]),
      Tag('VueJS', [ 'VUE', 'VUEJS' ]),
      Tag('WebSockets', [ 'WEBSOCKETS' ]),
      Tag('Next.js', [ 'NEXT.JS', 'NEXTJS' ]),
      Tag('Express', [ 'EXPRESS' ]),
      
      # Apis
      Tag('API', [ 'APIS', 'REST', 'WEB SERVICE', 'WEB SERVICES', 'REST APIs', "API's" ]),
      Tag('Webservice', [ 'WEB SERVICE', 'WEB SERVICES', 'WEBSERVICE', 'WEBSERVICES' ]),
      Tag('Postman', [ 'POSTMAN' ]),
      
      # Mobile
      Tag('Flutter', [ 'FLUTTER' ]),
      Tag('Ionic', [ 'IONIC' ]),
      Tag('Android', [ 'ANDROID' ]),
      Tag('Kotlin', [ 'KOTLIN' ]),
      Tag('PWA', [ 'PWA' ]),
      Tag('React Native', [ 'REACT NATIVE' ]),
      Tag('Swift', [ 'SWIFT' ]),
      Tag('Objective-C', [ 'OBJECTIVE-C', 'OBJECTIVE C' ]),
      Tag('Xamarin', [ 'XAMARIN' ]),

      # Desktop / Scripts
      Tag('C/C++', [ 'C++', 'C/C++' ]),
      Tag('Java', [ 'JAVA' ]),
      Tag('Gradle', [ 'GRADLE' ]),
      Tag('Maven', [ 'MAVEN' ]),
      Tag('Python', [ 'PYTHON' ]),
      Tag('Scala', [ 'SCALA' ]),
      Tag('C# / .NET', [ 'C#', '.NET' ]),
      Tag('Golang', [ 'GO', 'GOLANG' ]),
      Tag('NodeJs', [ 'NODE.JS', 'NODEJS' ]),
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
            
      # Operating Systems
      Tag('Linux', [ 'LINUX' ]),

      # Databases
      Tag('SQL', [ 'BANCO DE DADOS RELACIONAL', 'SQL' ]),
      Tag('NoSQL', [ 'NAO RELACIONAL', 'NOSQL', 'NO-SQL' ]),
      Tag('SqlServer', [ 'SQLSERVER', 'SQL SERVER' ]),
      Tag('Postgres', [ 'POSTGRES', 'POSTGRESQL' ]),
      Tag('Mongo', [ 'MONGODB', 'MONGO' ]),
      Tag('Oracle', [ 'ORACLE' ]),
      Tag('GraphQL', [ 'GRAPHQL' ]),
      Tag('Big Data', [ 'BIG DATA' ]),

      # Containers
      Tag('Docker', [ 'DOCKER' ]),
      Tag('Kubernetes', [ 'KUBERNETES' ]),
      
      # Teory
      Tag('Agile Develop.', [ 'AGEIS', 'SCRUM', 'KANBAN', 'METODOLOGIA ÁGIL' ]),
      Tag('Design Patterns', [ 'DESIGN PATTERNS' ]),
      Tag('Clean Code', [ 'CLEAN CODE' ]),
      Tag('Data Structure', [ 'ESTRUTURAS DE DADOS' ]),
      Tag('CI/CD', [ 'CI / CD', 'CI/CD' ]),
      Tag('Project management', [ 'GESTAO DE PROJETOS' ]),
      Tag('Product management', [ 'GESTAO DE PRODUTOS' ]),
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
      Tag('TDD', [ 'TDD', 'TEST-DRIVEN DEVELOPMENT' ]),

      # Security
      Tag('Pentests', [ 'PENETRATION TESTING', 'PENTESTS' ]),
      Tag('Segurança ofensiva', [ 'FERRAMENTAS OFENSIVAS', 'METASPLOIT FRAMEWORK', 'ETTERCAP', 'ACUNETIX', 'NEXPOSE', 'SQLMAP', 'AIRCRACK-NG' ]),
      
      # Others
      Tag('ETL', [ 'TRANSFORMACAO DE DADOS', 'MANIPULACAO DE DADOS' ]),
      Tag('Git', [ 'GIT', 'GITHUB' ]),
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
      Tag('ElasticSearch', [ 'ELASTICSEARCH' ]),
      Tag('Power BI', [ 'POWER BI' ]),
      Tag('Open-source', [ 'OPEN-SOURCE' ]),

      # UI
      Tag('Figma', [ 'FIGMA' ]),
      Tag('Illustrator', [ 'ILLUSTRATOR' ]),
      Tag('Photoshop', [ 'PHOTOSHOP' ]),
      
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
      
