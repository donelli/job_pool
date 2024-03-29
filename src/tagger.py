
import re
from typing import List
from unidecode import unidecode

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Tag:
   
   def __init__(self, name: str, words: List[str]):
      self.name = name
      self.words = words

tagsToSearch = [
   
   # Programing languages / markup languages
   Tag('PHP', [ 'PHP', 'PHP7', 'PHP7+', 'PHP8' ]),
   Tag('HTML', [ 'HTML', 'HTML5' ]),
   Tag('CSS', [ 'CSS', 'CSS3' ]),
   Tag('JS', [ 'JAVASCRIPT', 'JS' ]),
   Tag('Kotlin', [ 'KOTLIN' ]),
   Tag('Swift', [ 'SWIFT' ]),
   Tag('Objective-C', [ 'OBJECTIVE-C', 'OBJECTIVE C' ]),
   Tag('C/C++', [ 'C++', 'C/C++' ]),
   Tag('Java', [ 'JAVA' ]),
   Tag('Python', [ 'PYTHON', 'PHYTON' ]),
   Tag('Scala', [ 'SCALA' ]),
   Tag('C# / .NET', [ 'C#', '.NET' ]),
   Tag('Golang', [ 'GO', 'GOLANG' ]),
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
   Tag('ABAP', [ 'ABAP' ]),
   Tag('Shell', [ 'SHELL', 'SH' ]),
   Tag('Progress', [ 'PROGRESS' ]),
   Tag('Cobol', [ 'COBOL' ]),
   Tag('VBA', [ 'VBA', 'Visual Basic' ]),
   Tag('VB.NET', [ 'VB.NET' ]),
   Tag('Recital', [ 'RECITAL' ]),
   Tag('FoxPro', [ 'FOXPRO' ]),
   Tag('Clipper', [ 'CLIPPER' ]),
   Tag('ActionScript', [ 'ACTIONSCRIPT' ]),
   
   # Frameworks
   Tag('Laravel', [ 'LARAVEL' ]),
   Tag('PHPUnit', [ 'PHPUNIT' ]),
   Tag('JSX', [ 'JSX' ]),
   Tag('AngularJS', [ 'ANGULARJS' ]),
   Tag('Angular', [ 'ANGULAR' ]),
   Tag('ReactJS', [ 'REACT', 'REACTJS', 'REACT.JS' ]),
   Tag('Ember', [ 'EMBER' ]),
   Tag('VueJS', [ 'VUE', 'VUEJS', 'VUE.JS' ]),
   Tag('Next.js', [ 'NEXT.JS', 'NEXTJS' ]),
   Tag('Express', [ 'EXPRESS' ]),
   Tag('Svelte', [ 'SVELTE' ]),
   Tag('Bootstrap', [ 'BOOTSTRAP', 'BOODSTRAP' ]),
   Tag('Tailwind', [ 'TAILWIND' ]),
   Tag('Material Design', [ 'MATERIAL DESIGN' ]),
   Tag('Django ', [ 'DJANGO ' ]),
   Tag('Symfony', [ 'SYMFONY' ]),
   Tag('Flutter', [ 'FLUTTER' ]),
   Tag('Ionic', [ 'IONIC' ]),
   Tag('React Native', [ 'REACT NATIVE' ]),
   Tag('Xamarin', [ 'XAMARIN' ]),
   Tag('Flask', [ 'FLASK' ]),
   Tag('Springboot', [ 'SPRINGBOOT', 'SPRING BOOT' ]),
   Tag('Spring MVC', [ 'SPRING MVC' ]),
   Tag('Quarkus', [ 'QUARKUS' ]),
   Tag('Stencil', [ 'STENCIL' ]),
   Tag('WordPress', [ 'WORDPRESS' ]),
   Tag('Handlebars', [ 'HANDLEBARS' ]),
   Tag('RequireJS', [ 'REQUIREJS' ]),
   Tag('Backbone.js', [ 'BACKBONE.JS' ]),
   Tag('jQuery', [ 'JQUERY' ]),
   Tag('Micronaut', [ 'MICRONAUT' ]),
   
   # Preprocessors
   Tag('SCSS/SASS', [ 'SCSS', 'SASS' ]),
   Tag('TS', [ 'TYPESCRIPT', 'TS' ]),
   
   # Tools
   Tag('Eslint', [ 'ESLINT' ]),
   Tag('Postman', [ 'POSTMAN' ]),
   Tag('Gradle', [ 'GRADLE' ]),
   Tag('Maven', [ 'MAVEN' ]),
   Tag('NodeJs', [ 'NODE.JS', 'NODEJS', 'NODE' ]),
   Tag('Npm', [ 'NPM' ]),
   Tag('Fiori', [ 'FIORI' ]),
   Tag('Docker', [ 'DOCKER' ]),
   Tag('Kubernetes', [ 'KUBERNETES', 'KUBERNETS' ]),
   Tag('Big Data', [ 'BIG DATA' ]),
   Tag('Spark', [ 'SPARK' ]),
   Tag('Hive', [ 'HIVE' ]),
   Tag('Tableau', [ 'TABLEAU' ]),
   Tag('Hadoop', [ 'HADOOP' ]),
   Tag('Webpack', [ 'WEBPACK' ]),
   Tag('Babel', [ 'BABEL' ]),
   Tag('CI/CD', [ 'CI / CD', 'CI/CD', 'CD / I', 'CONTINUOUS DELIVERY' ]),
   Tag('SAP', [ 'SAP' ]),
   Tag('Jenkins', [ 'JENKINS' ]),
   Tag('Travis', [ 'TRAVIS' ]),
   Tag('PowerShell', [ 'POWERSHELL' ]),
   Tag('Composer (PHP)', [ 'COMPOSER' ]),
   Tag('Grafana', [ 'GRAFANA' ]),
   Tag('SonarQube', [ 'SONARQUBE' ]),
   Tag('Styled Components', [ 'STYLED COMPONENTS', 'STYLED-COMPONENTS' ]),
   
   # Tecnologies
   Tag('WebSockets', [ 'WEBSOCKETS' ]),
   Tag('Webhooks', [ 'WEBHOOKS' ]),
   Tag('SOAP', [ 'SOAP' ]),
   Tag('PWA', [ 'PWA', 'PROGRESSIVE WEB APPS' ]),
   Tag('gRPC', [ 'GRPC' ]),
   Tag('Git', [ 'GIT', 'GITHUB', 'GITLAB', 'GITFLOW' ]),
   Tag('OAUTH', [ 'OAUTH', 'OAUTH2' ]),
   Tag('RPA', [ 'RPA' ]),
   Tag('JWT', [ 'JSON WEB TOKEN', 'JWT' ]),
   Tag('BI', [ 'POWER BI', 'METABASE', 'BUSINESS INTELLIGENCE', 'LOOKER', 'TABLEAU' ]),
   Tag('SPA', [ 'SPA', 'SPAS' ]),
   Tag('Hybrid Apps', [ 'HYBRID APPS', 'APPS HÍBRIDOS' ]),
   Tag('Offline-first', [ 'OFFLINE-FIRST', 'OFFLINE FIRST' ]),
   
   # Programming Terms
   Tag('API', [ 'APIS', 'REST', 'WEB SERVICE', 'WEB SERVICES', 'REST APIS', "API'S", 'RESTFULL API' ]),
   Tag('Webservice', [ 'WEB SERVICE', 'WEB SERVICES', 'WEBSERVICE', 'WEBSERVICES' ]),
   Tag('SQL', [ 'BANCO DE DADOS RELACIONAL', 'BANCO DE DADOS RELACIONAIS', 'SQL', 'RELATIONAL DATABASES' ]),
   Tag('NoSQL', [ 'NAO RELACIONAL', 'NÃO RELACIONAIS', 'NOSQL', 'NO-SQL' ]),
   Tag('Big Data', [ 'BIG DATA' ]),
   Tag('Front End', [ 'FRONT-END', 'FRONT END', 'FRONTEND' ]),
   Tag('Back End', [ 'BACK-END', 'BACK END', 'BACKEND' ]),
   Tag('Full Stack', [ 'FULL STACK', 'FULL-STACK' ]),
   Tag('ETL', [ 'TRANSFORMACAO DE DADOS', 'MANIPULACAO DE DADOS', 'ETL' ]),
   Tag('Message broker', [ 'MENSAGERIAS', 'RABBITMQ', 'AZURESERVICEBUS' ]),
   Tag('Peer Programming.', [ 'PEER PROGRAMMING' ]),
   Tag('Agile Develop.', [ 'AGEIS', 'SCRUM', 'KANBAN', 'METODOLOGIA ÁGIL', 'AGILE METHODOLOGY', 'METODOLOGIA AGIL', 'AGILE PROJECTS' ]),
   Tag('Design Patterns', [ 'DESIGN PATTERNS' ]),
   Tag('Clean Code', [ 'CLEAN CODE' ]),
   Tag('Data Structure', [ 'ESTRUTURAS DE DADOS' ]),
   Tag('Project management', [ 'GESTAO DE PROJETOS' ]),
   Tag('Product management', [ 'GESTAO DE PRODUTOS' ]),
   Tag('Requirements analysis', [ 'ANALISE DE REQUISITOS' ]),
   Tag('Quality analysis', [ 'ANALISTA DE QUALIDADE' ]),
   Tag('Dependence analysis', [ 'GERENCIAMENTO DE DEPENDÊNCIAS' ]),
   Tag('Distributed systems', [ 'SISTEMAS DISTRIBUÍDOS', 'DISTRIBUTED ARCHITECTURE' ]),
   Tag('Microservices', [ 'MICROSSERVICOS', 'MICROSSERVIÇOS', 'MICRO SERVIÇOS', 'MICRO-SERVIÇOS' ]),
   Tag('Open-source', [ 'OPEN-SOURCE' ]),
   Tag('Serverless', [ 'SERVERLESS' ]),
   Tag('Devops', [ 'DEVOPS' ]),
   Tag('SRE', [ 'SRE', 'SITE RELIABILITY ENGINEERING' ]),

   # Operating Systems
   Tag('Android', [ 'ANDROID' ]),
   Tag('Linux', [ 'LINUX' ]),
   Tag('AIX', [ 'AIX' ]),
   Tag('iOS', [ 'IOS' ]),
   
   # Library
   Tag('SwiftUI', [ 'SWIFTUI' ]),
   Tag('PySpark', [ 'PYSPARK' ]),
   Tag('RxJS', [ 'RXJS' ]),
   Tag('Redux', [ 'REDUX' ]),
   Tag('Ngxs', [ 'NGXS' ]),

   # Tests
   Tag('Pentests', [ 'PENETRATION TESTING', 'PENTESTS' ]),
   Tag('Segurança ofensiva', [ 'FERRAMENTAS OFENSIVAS', 'METASPLOIT FRAMEWORK', 'ETTERCAP', 'ACUNETIX', 'NEXPOSE', 'SQLMAP', 'AIRCRACK-NG' ]),
   Tag('Unit testing', [ 'TESTES UNITARIOS' ]),
   Tag('Automated testing', [ 'TESTES AUTOMATIZADOS', 'AUTOMACAO DE TESTES' ]),
   Tag('Tests', [ 'PLANO DE TESTES', 'CENARIOS DE TESTE' ]),
   Tag('Cypress', [ 'CYPRESS' ]),
   Tag('Puppet', [ 'PUPPET' ]),
   Tag('Selenium', [ 'SELENIUM' ]),
   Tag('Ansible', [ 'ANSIBLE' ]),
   Tag('Web tests', [ 'TESTES WEB' ]),
   Tag('API tests', [ 'TESTES DE API' ]),
   Tag('TDD', [ 'TDD', 'TEST-DRIVEN DEVELOPMENT', 'TEST DRIVEN DEVELOPMENT', 'DESENVOLVIMENTO ORIENTADO A TESTES' ]),
   Tag('jUnit', [ 'JUNIT' ]),
   Tag('Mocha', [ 'MOCHA' ]),
   Tag('Chai', [ 'CHAI' ]),
   Tag('Jasmine', [ 'JASMINE' ]),
   Tag('Jest', [ 'JEST' ]),
   Tag('Qtest', [ 'QTEST' ]),

   # Databases
   Tag('SqlServer', [ 'SQLSERVER', 'SQL SERVER' ]),
   Tag('Postgres', [ 'POSTGRES', 'POSTGRESQL', 'POSTGREES', 'PGSQL' ]),
   Tag('MySQL', [ 'MYSQL' ]),
   Tag('Mongo', [ 'MONGODB', 'MONGO' ]),
   Tag('Oracle', [ 'ORACLE' ]),
   Tag('GraphQL', [ 'GRAPHQL' ]),
   Tag('DynamoDB', [ 'DYNAMODB' ]),
   Tag('Datomic', [ 'DATOMIC' ]),
   Tag('Redis', [ 'REDIS', 'REDISDB' ]),
   Tag('Teradata', [ 'TERADATA' ]),
   Tag('Cassandra', [ 'CASSANDRA' ]),
   Tag('CouchDB', [ 'COUCHDB' ]),
   Tag('DB2', [ 'DB2' ]),
   Tag('Firebase', [ 'FIREBASE' ]),
   Tag('Appwrite', [ 'APPWRITE' ]),
   Tag('Windows Server', [ 'WINDOWS SERVER' ]),
   Tag('Debezium', [ 'DEBEZIUM' ]),

   # Products
   Tag('Machine learning', [ 'MACHINE LEARNING' ]),
   Tag('Pipelines', [ 'PIPELINES' ]),
   Tag('i18n', [ 'i18n', 'I18N' ]),
   Tag('ElasticSearch', [ 'ELASTICSEARCH', 'STACK ELK' ]),
   Tag('Power BI', [ 'POWER BI', 'POWERBI' ]),
   Tag('Kafka', [ 'KAFKA' ]),
   Tag('ABAP', [ 'ABAP' ]),
   Tag('OpenShift', [ 'OPENSHIFT' ]),
   Tag('VMware', [ 'VMWARE' ]),
   Tag('Hyper-V', [ 'HYPER-V' ]),
   Tag('Oracle VM', [ 'ORACLE VM' ]),
   Tag('Figma', [ 'FIGMA' ]),
   Tag('Illustrator', [ 'ILLUSTRATOR' ]),
   Tag('Photoshop', [ 'PHOTOSHOP' ]),
   Tag('Jira', [ 'JIRA' ]),

   # Cloud
   Tag('Terraform', [ 'TERRAFORM' ]),
   Tag('Pulumi', [ 'PULUMI' ]),
   Tag('Azure', [ 'AZURE' ]),
   Tag('Azure Datafactory', [ 'AZURE DATAFACTORY' ]),
   Tag('AWS', [ 'AWS' ]),
   Tag('IBM Cloud', [ 'IBM CLOUD' ]),
   Tag('GCP', [ 'GCP', 'GOOGLE CLOUD' ]),
   
]

class Tagger(metaclass=Singleton):
   
   def __init__(self) -> None:
      self.wordRe = re.compile('\\w')
   
   def generateTags(self, text: str) -> List[str]:
      
      text = '|' + unidecode(text.upper()) + '|'

      # Remove some terms that messes up the search of the Go tag
      text = text.replace('GO WRONG', '')
      text = text.replace('GO TO', '')
      text = text.replace('GO-TO-MARKET', '')
      text = text.replace('GO THROUGH', '')
      
      text = text.replace('JAVA SCRIPT', 'JAVASCRIPT')
      
      tags: List[str] = []
      
      for tag in tagsToSearch:
         
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
      
