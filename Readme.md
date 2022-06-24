# Test task to Back-End School 2022   
![coverage](./coverage.svg)

### Technologies used:  
* _Python_
* _Django_
* _Django Rest Framework_
* _PostgreSQL_
* _PyTest_     


## _Some commands for comfortable run:_  
### • To test:  
#### To run tests [pytest]:  
1. Activate venv
2. `pip install -r requirements.txt`  
3. `coverage run -m pytest`  
4. `coverage report` or `coverage html` (for generating report in HTML)
5. Remove `coverage-badge.svg` file and run `coverage-badge -o coverage.svg`  

#### To run tests [unittest from task-source]:   
1. `pip install -r requirements.txt` 
2. Run server in Docker (see below how to run in docker) or in usual way ()
3. `python unit_test.py`

### • To launch:
#### To run application locally [no Docker] (you must have PostgreSQL installed and set up):  
1. Activate venv
2. `pip install -r requirements.txt`
3. Change `DOCKER` field in `config.json` to `false`  
4. `python manage.py makemigrations`  
5. `python manage.py migrate`  
6. `python manage.py runserver 0.0.0.0:80` (or other port, for example)  

#### To run application locally [with Docker] (build & run)
1. `(sudo) docker-compose up -d --build`
2. `(sudo) docker-compose exec web python manage.py makemigrations --noinput`  
3. `(sudo) docker-compose exec web python manage.py migrate --noinput`  
4. [optional] `(sudo) docker-compose exec web python manage.py createsuperuser`
5. `(sudo) docker-compose up`

### • To deploy:
#### To set up remote machine:
1. Set `docker` field to `true`/`false` (depending on if you're going to run in Docker)
2. Push changes to GitHub repository `git add <...>`, `git commit -m <...>`, `git push`
3. Connect to remote machine (via SSH) `ssh login@ip`. Following actions are done from remote machine
4. `git clone <this_repo_url>`  
5. `cd rest-api-test-task` 
6. For non-Docker run:
   1. `python3 -m venv venv`  
   2. `source venv/bin/activate`  
   3. `pip3 install -r requirements.txt`  
   4. `python3 manage.py makemigrations`  
   5. `python3 manage.py migrate`
7. For Docker-run:
   1. `docker-compose up -d --build`
   2. `docker-compose exec web python manage.py makemigrations --noinput`  
   3. `docker-compose exec web python manage.py migrate --noinput`  
   4. [optional] `docker-compose exec web python manage.py createsuperuser`
8. [Auto running:](https://winitpro.ru/index.php/2019/10/11/avtozagruzka-servisov-i-skriptov-v-linux/)  
9. `sudo touch /etc/systemd/system/test-script.service` 
10. `sudo chmod 664 /etc/systemd/system/test-script.service`
11. `sudo nano /etc/systemd/system/test-script.service`
12. Write file 
13. Write entry-point SH executor  (for running with or without Docker)
14. `sudo systemctl enable test-script.service`
&nbsp;  



### Some demo:  
##### GitHub Actions demo:  
![GitHub Actions output](github-actions-demo.PNG)
##### Local tests pass results:  
![Import, Nodes, Sales, Delete](local_test_results.PNG)  

&nbsp;  



###### Copyright © 2022