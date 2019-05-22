# CodeChef Photo Gallery
Backend of photo gallery app made for CodeChef Summer Internship 2019.

## How to Run the Code?
This section describes how the app can be viewed in action.

* Step 1: Download the virtual environment virenv.tar.xz present in the repository.

* Step 2: Go to folder containing the extracted file and activate the environment by using
```
source virenv/Scripts/activate
```
* Step 3: Install other requirements
```
pip3 install django-extra-fields
pip3 install django-cors-headers
pip3 install -U django-oauth-toolkit
```
* Step 4: Run the server
```
python3 manage.py runserver
```
Once the application is running, go to [link](http://127.0.0.1:8000/admin/).
All the functions can be performed using Django's Admin Portal.

The dummy account's username and password is  
```
Username: cchef
Password: l
```
Using OAuth tokens for Authentication.

I started creating the frontend in React, but couldn't complete it due to my Semester Exams.
After running this, go to [link](https://github.com/gkashish/photo_gallery_app_front_end) to start the front-end (which is yet to be completed).

## API Table
This section describes the API made for and utilized by this app.

### Albums
| HTTP Verb | CRUD   | PARAMS(JSON) | RETURNS(JSON)  | ENDPOINT   |
|-----------|--------|--------------|----------------| -----------|
| GET       | Read   |              | List of Albums | /album     |
| PUT       | Update | Album ID     |                | /album     |
| POST      | Create | Album Object |                | /album     |
| DELETE    | Delete | Album ID     |                | /album     |

### Photo 
| HTTP Verb | CRUD   | PARAMS(JSON) | RETURNS(JSON)  | ENDPOINT                 |
|-----------|--------|--------------|----------------| -------------------------|
| GET       | Read   |              | List of Photos | albums/<int:pk>/photos/  |
| PUT       | Update | Photo ID     |                | albums/<int:pk>/addphoto/|
| POST      | Create | Photo Object |                | albums/<int:pk>/photos/  |
| DELETE    | Delete | Photo ID     |                | albums/<int:pk>/photos/  |


