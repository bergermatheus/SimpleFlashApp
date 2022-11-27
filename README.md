## General info
This project is a simple CRUD application in Flash to handle with employees data. The repository contains a source folder "src", the main file is app.py. There is also a file to handle with the database called "db_functions.py".

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Example](#example)

	
## Technologies
Project is created with:
* Flask 2.0.0
* Python 3.9.2
	
## Setup

First setup a virtual environment to isolate the application. If you use Windows:

```
pip install virtualenv
virtualenv virtual-ssys-challenge
.\virtual-ssys-challenge\Scripts\activate
```

If you are using Linux, follow the commands bellow:

```
$ pip install virtualenv
$ virtualenv virtual-ssys-challenge
$ source virtual-ssys-challenge/bin/activate
```

To run this project, install the dependecies using pip:

```
$ pip install -r requirements.txt

```

## Example
That's an example of how to run the API server:

```
$ py .\src\app.py

```

Terminal Output:

```
* Serving Flask app 'SSYS_Employee_Manager' (lazy loading)
* Environment: production
- WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 598-489-118
 * Running on http://localhost:80/ (Press CTRL+C to quit)
```

To check the server you can run a file called "client_routine.py" that simulates the client requests.
