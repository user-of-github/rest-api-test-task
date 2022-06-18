# Test task to Yandex Back-End School 2022   


### Technologies used:  
* _Python_
* _Django_
* _Django Rest Framework_
* _PostgreSQL_
* _Docker_   


## Some commands for comfortable run:  

#### To build Docker-image from scratch:    
`pip freeze > requirements.txt`  
`docker-compose up -d --build`  
`docker-compose exec web python manage.py makemigrations --noinput`  
`docker-compose exec web python manage.py migrate --noinput`  
`docker-compose exec web python manage.py createsuperuser`  
_// optional (check db)_  
`docker-compose exec db psql --username=<username> --dbname=<databasename>`   
`\l` , `\dt`  




###### Copyright © 2022