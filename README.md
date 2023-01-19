# Page analyser

#### [Page Analyzer](https://python-project-83-production-fd23.up.railway.app/) is a website that analyzes the specified pages for SEO suitability.

### Hexlet tests and linter status:
[![Actions Status](https://github.com/Alexey-Shepelev/python-project-83/workflows/hexlet-check/badge.svg)](https://github.com/Alexey-Shepelev/python-project-83/actions)
[![ci-tests](https://github.com/Alexey-Shepelev/python-project-83/actions/workflows/ci-tests.yml/badge.svg)](https://github.com/Alexey-Shepelev/python-project-83/actions/workflows/ci-tests.yml)

#### How to install and use
```commandline
git clone git@github.com:Alexey-Shepelev/python-project-83.git # clone repo

cd python-project-83

# create .env file with following variables:
DATABASE_URL = postgresql://{provider}://{user}:{password}@{host}:{port}/{db}
SECRET_KEY = '{your secret key}'

# run
psql {yourdb} < database.sql

make install # install dependancies

make dev # for local use and dev
make start # star command for deploy
```