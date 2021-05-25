# importing the requests library
import requests
from requests.auth import HTTPBasicAuth
import time

is_inproduction = False


base_path = "http://ip172-18-0-38-c2m622lmrepg008vkg7g-80.direct.labs.play-with-docker.com/"
base_localpath = "http://localhost:80/"
URL = ''
if is_inproduction == True:
    URL = base_path
else:
    URL = base_localpath

# login and get token
payload = {'username': 'user', 'password': 'password'}
r = requests.get(url = URL + 'login', auth = HTTPBasicAuth('user', 'password'))

data  = r.json()
token = data['token']
print('Auth token: ',token)
print()


## get employees list

r = requests.get(url = URL + 'employees/', headers = {"Authorization":"Bearer " + token} )

data  = r.json()
print('Employee list:')
print(data)
print()

# post data at the Database
employee_array = [{
"id": "1",
"name": "Anakin Skywalker",
"email": "skywalker@ssys.com.br",
"department": "Architecture",
"salary": "4000.00",
"birth_date": "01-01-1983"},
{
"id": "2",
"name": "Obi-Wan Kenobi",
"email": "kenobi@ssys.com.br",
"department": "Back-End",
"salary": "3000.00",
"birth_date": "01-01-1977"},
{
"id": "3",
"name": "Leia Organa",
"email": "organa@ssys.com.br",
"department": "DevOps",
"salary": "5000.00",
"birth_date": "01-01-1980"}]

for mydata in employee_array:
    r = requests.post(url = URL + 'employees/', headers = {"Authorization":"Bearer " + token} , json = mydata)

    response  = r.text
    print(response)
print()

## employee ID to get specific details
employee_ID = '1'

r = requests.get(url = URL + 'employees/' + employee_ID , headers = {"Authorization":"Bearer " + token})

data  = r.json()
print('Employee ID ' + employee_ID + ' details:')
print(data)
print()


## get employees salary report


r = requests.get(url = URL + 'reports/employees/salary/', headers = {"Authorization":"Bearer " + token} )

data  = r.json()
print('Employee Salary report:')
print(data)
print()

## get employees age report


r = requests.get(url = URL + 'reports/employees/age/', headers = {"Authorization":"Bearer " + token} )

data  = r.json()
print('Employee Age report:')
print(data)
print()



## employee ID to update specific details
employee_ID = '3'
new_data = {
"id": "3",
"name": "Matheus Berger",
"email": "berger@ssys.com.br",
"department": "DevOps",
"salary": "5000.00",
"birth_date": "01-01-1995"
}
r = requests.put(url = URL + 'employees/' + employee_ID , headers = {"Authorization":"Bearer " + token}, json = new_data)

data  = r.json()
print('Employee ID ' + employee_ID + ' update:')
print(data)
print()

## delete employee by ID 
employee_ID = '3'
r = requests.delete(url = URL + 'employees/' + employee_ID , headers = {"Authorization":"Bearer " + token})

data  = r.json()
print(data)
print()