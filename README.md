# MOVIE EXPLORER

Django + React movie app.

## START APPLICATION

make up


make populate

Frontend: http://localhost:3000


API: http://localhost:8000/api


## VIEW SWAGGER DOCS


1. http://127.0.0.1:8000/api/schema/


2. http://127.0.0.1:8000/api/docs/swagger/


3. http://127.0.0.1:8000/api/docs/redoc/



## COMMANDS

make up - start containers


make populate - load sample data


make logs - view logs


make down - stop


make rebuild - restart


make test-backend - python tests


make test-frontend - react tests

make test - run both backend & frontend tests



## How It Works


Data comes from backend/movies/management/commands/movies.py. When you run make populate it loads sample movies into the database.


Docker runs two services - backend on 8000 and frontend on 3000. Both are configured in docker-compose.yml.


The Makefile just has shortcuts so you don't have to type long docker commands.

How to use it:

1. Run "make up" to start everything


2. Run "make populate" to load movies


3. Go to http://localhost:3000 and use the app


## NOTE

Code is shipped with default "db.sqlite"


