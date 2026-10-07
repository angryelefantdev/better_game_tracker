This is a better game tracker made by me 
FILES TO CHANGE:
  Dockerfile.example {
  rename it to Dockerfile
  }
  compose.yaml.example {
  rename it to compose.yaml
  change the database to your database name
  change the password to your database password
  }
  env.example {
  rename it to .env
  edit the rawg io token to your own token
  edit the database password to your own password
  }

A game tracker with user and game system where it saves users and saves games using the RAWG.IO API 
to access it run it with docker and PowerShell
type in PowerShell with Docker app turned on: docker compose build web
and then after its done type: docker compose up
and done!
Access the website with localhost:8000/docs 
