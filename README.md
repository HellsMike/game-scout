# Game Scout

# Installed Packages
Python 3.9.7

Django 4.0.4

Pillow 8.3.2

django4-background-tasks 1.2.7

***
# Getting Started

In your project directory create your virtual environment and install required packages:
```
pipenv install
```
Then activate the virtual environment:
```
pipenv shell
```
Start server:
```
python manage.py runserver
```
Start tasks in a new console:
```
python manage.py process_tasks
```
Open the browser and go to url localhost:8000

Create a text file called 'email_host_data.txt' in game-scout/gs with e-mail account password for e-mail notifications
or
Change e-mail account data for e-mail notifications sender

If you sign up with username Admin, you will be granted the rights to access to Add Product page to add new product and to Django Admin page to manage your database