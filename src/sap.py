
class SapSearcher():

   departments = [
      'Software-Design+and+Development',
      'Software-Development+Operations',
      'Software-User+Experience'
   ]

   baseUrl = 'https://jobs.sap.com/search/?optionsFacetsDD_country=BR&optionsFacetsDD_department='

   def search(self):
      pass


if __name__ == '__main__':
   
   sap = SapSearcher()
   sap.search()
   