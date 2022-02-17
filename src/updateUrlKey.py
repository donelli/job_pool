
from repository.firebase_repo import FirebaseRepository

print("Connection to database...")
repo = FirebaseRepository()
repo.connectToDb()

jobs = repo.getAllJobs()

for job in jobs:
   repo.updateUrlKey(job)
