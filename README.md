# blogging-with-django

#### Installation
1. install and start mysql:
```
sudo apt-get install mysql-server
sudo apt-get install libmysqlclient-dev
systemctl start mysql
```
then config the db according to /blog/settings.py

2. install virtualenv: `sudo apt-get install python3-venv`
3. create a new venv, start it and return to project folder
4. install all requirements
5. `python manage.py migrate`
6. `python manage.py runserver [+port]` http://localhost:8000/
7. deploy: set environment variables SECRET_KEY and DEBUG (in /blog/.env)

#### TODO:
1. refactor existing unit tests and write new tests for other features
2. build a custom image slider
3. add a gallery tab
