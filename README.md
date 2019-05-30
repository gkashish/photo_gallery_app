# CodeChef Photo Gallery
Backend of photo gallery app made for CodeChef Summer Internship 2019.
## The application is hosted at [link](https://gkashish.github.io/photo-gallery-app-frontend/). The backend is hosted on heroku, frontend is hosted as github pages, and the storage service used is Google Firebase storage.

## How to Run the Code?
This section describes how the app can be viewed in action.

* Step 1: Clone the repository, open terminal inside the folder and install the requirements by using:

* Step 2: Install the requirements
```
pip install requirements.txt
```
* Step 3: Run the server
```
python manage.py runserver
```
Once the application is running, go to [link](http://127.0.0.1:8000/admin/).
All the functions can be performed using Django's Admin Portal.

The admin username and password is  
```
Username: cchef
Password: hello
```
Using token based authentication.

## After running this, go to [link](https://github.com/gkashish/photo-gallery-app-frontend) to launch the frontend.

The deletion is cascaded, if a user is deleted, all their albums are deleted and if an album is deleted all its photos are deleted.
