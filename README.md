# Page analyser

#### [Page Analyzer](https://python-project-83-production-fd23.up.railway.app/) is a website that analyzes the specified pages for SEO suitability.

### Hexlet tests and linter status:
[![Actions Status](https://github.com/Alexey-Shepelev/python-project-83/workflows/hexlet-check/badge.svg)](https://github.com/Alexey-Shepelev/python-project-83/actions)
[![ci-tests](https://github.com/Alexey-Shepelev/python-project-83/actions/workflows/ci-tests.yml/badge.svg)](https://github.com/Alexey-Shepelev/python-project-83/actions/workflows/ci-tests.yml)

### How to install and use
#### Clone the repo
```commandline
git clone git@github.com:Alexey-Shepelev/python-project-83.git
```
##### Install PostgreSQL:

```commandline
# Macos
brew install postgresql

# Ubuntu, Windows
sudo apt install postgresql
```
#### Create database user:
```commandline
whoami
{yourusername}
sudo -u postgres createuser --createdb {yourusername}
```
#### Create database:
```commandline
createdb {yourdb}
```
#### Change directory to:
```commandline
cd python-project-83
```
#### run
```commandline
psql {yourdb} < database.sql
```
#### Rename .env.sample file to .env and add with following variables:
```commandline
DATABASE_URL = postgresql://{yourusername}:{password}@{host}:{port}/{yourdb}
SECRET_KEY = '{your secret key}'
```
#### Install dependencies:
```commandline
make install 
```
#### For local use and dev:
```commandline
make dev 
```
#### Start command for deploy:
```commandline
make start 
```


#### Screenshots:
<img src=https://user-images.githubusercontent.com/103209789/213551279-a92e4f9c-c027-4f14-b930-fccad63bdc16.png width="500">

<img src=https://user-images.githubusercontent.com/103209789/213551750-fa024d62-6c76-4cc8-8d06-3f9b659fd004.png width="500">

<img src=https://user-images.githubusercontent.com/103209789/213551797-e0bfb05b-2763-4526-b72c-4e0608d3aae9.png width="500">
