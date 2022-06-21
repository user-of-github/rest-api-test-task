# Test task to Back-End School 2022   
![coverage](./coverage.svg)

### Technologies used:  
* _Python_
* _Django_
* _Django Rest Framework_
* _PostgreSQL_
* _Docker_   


## Some commands for comfortable run:  

#### To run tests (pytest)  
1. `pip install -r requirements.txt`  
2. `coverage run -m pytest`  
3. `coverage report` or `coverage html` (for generating report in HTML)
4. `coverage-badge -o coverage.svg`
&nbsp;   

#### To run application locally:  
1. `pip install -r requirements.txt`
2. Change `DOCKER` field in `config.json` to `false`  
3. `python manage.py makemigrations`  
4. `python manage.py migrate`  
5. `python manage.py runserver localhost:80` (or other port)  

&nbsp;  
#### To build and run in Docker-container from scratch:   
1. Change `DOCKER` field in `config.json` to `true`  
2. `pip freeze > requirements.txt`  
3. `docker-compose up -d --build`  
4. `docker-compose exec web python manage.py makemigrations --noinput`  
5. `docker-compose exec web python manage.py migrate --noinput`  
6. `docker-compose exec web python manage.py createsuperuser`  
_// optional (check db)_  
7. `docker-compose exec db psql --username=<username> --dbname=<databasename>`   
8. `\l` , `\dt`   


### Some demo:  
##### Local tests pass results:  
![Import, Nodes, Sales, Delete](local_test_results.PNG)  

&nbsp;  



###### Copyright © 2022