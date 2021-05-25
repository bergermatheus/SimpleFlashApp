import sqlite3
import os
import datetime
from datetime import datetime
from dateutil.relativedelta import relativedelta




class Database:

    def __init__(self):
        # Database name
        self.db_name = "SYSS_database.db"

        # if dataset does not exist, then create one
        if os.path.exists(str(os.getcwd() +"\\"+ self.db_name)) != True:
            self.contact(self.db_name,"""CREATE TABLE IF NOT EXISTS Database(id INTEGER NOT NULL, Name VARCHAR(100) NOT NULL, 
                Email VARCHAR(50) NOT NULL, Department VARCHAR(50) NOT NULL, Salary INTEGER NOT NULL, Birth_Date DATE NOT NULL)""")
            print("Database created successfully")

    
    def contact(self, database_name , database_command):
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()
        result = cursor.execute(database_command)
        conn.commit()
        return(result)

    
    def create(self, employee_details):
        

        id = employee_details["id"]
        name = employee_details["name"]
        email = employee_details["email"]
        department = employee_details["department"]
        salary = employee_details["salary"]
        birth_date = employee_details["birth_date"]

        result = self.contact(self.db_name, "Select * From Database Where id = '{0}';".format(id))

        if len(result.fetchall()) != 0:
            return 'Employee ID already exists'


        self.contact(self.db_name,"INSERT INTO Database VALUES('{0}','{1}','{2}','{3}','{4}', '{5}');"
        .format(id , name , email , department , salary , birth_date ))
        return("Data created successfully")

    
    def update(self, employee_details, ID):

        result = self.contact(self.db_name, "Select * From Database Where id = '{0}';".format(ID))

        if len(result.fetchall()) == 0:
            return 'Employee ID does not exist'

        name = employee_details['name']
        email = employee_details['email']
        department = employee_details['department']
        salary = employee_details['salary']
        birth_date = employee_details['birth_date']

        self.contact(self.db_name, "UPDATE Database SET Name = '{0}', Email = '{1}', Department = '{2}',Salary = '{3}', Birth_Date = '{4}' WHERE id = '{5}';"
            .format(name , email , department , salary , birth_date , ID ))
        return("Updated successfully")
        
    
    def delete( self, _id ):
        result = self.contact(self.db_name, "Select * From Database Where id = '{0}';".format(_id))
            
        if len(result.fetchall()) == 0:
            return 'Employee ID does not exist'

        self.contact(self.db_name , "DELETE FROM Database WHERE id = '{0}';".format( _id ))
        return("Deleted successfully")

    
    def show_employees_details( self, _id = None):
    
        # if ID number is not NONE, show details from one specific employee
        if _id != None:
            result = self.contact(self.db_name, "Select * From Database Where id = '{0}';".format(_id))

            if len(result.fetchall()) == 0:
                return 'Employee ID does not exist'

            result = self.contact(self.db_name, "Select * From Database Where id = '{0}';".format(_id))
            result = result.fetchall()[0]
            

            # Converting to a dictionary
            employees_list = [self.data_to_dictionary(result)]
            return employees_list
        
        # else show list of all employees
        else:
            result = self.contact(self.db_name,"Select * From Database")
            result = result.fetchall()

        if len(result) == 0:
            return 'Database is empty.'

        # Converting to a dictionary
        employees_list = []
        for row in result:
            employees_list.append(self.data_to_dictionary(row))
        return employees_list

    
    def salary_report(self):
        
        # Check if dataset is empty
        result = self.contact(self.db_name,"Select * From Database")
        
        if len(result.fetchall()) == 0:
            return 'Database is empty.'

        # Getting the highest salary details
        result = self.contact(self.db_name,'SELECT * FROM Database WHERE Salary = (SELECT MAX(Salary) FROM Database)')
        result = result.fetchall()[0]
            
        highest_salary_employee = self.data_to_dictionary(result)
        highest_salary = highest_salary_employee['salary']

        # Getting the lowest employee details
        result = self.contact(self.db_name,'SELECT * FROM Database WHERE Salary = (SELECT MIN(Salary) FROM Database)')
        result = result.fetchall()[0]
            
        lowest_salary_employee = self.data_to_dictionary(result)
        lowest_salary = lowest_salary_employee['salary']

        average = (lowest_salary + highest_salary)/2

        return {'lowest': lowest_salary_employee, 'highest' : highest_salary_employee, 'average': average}

    def age_report(self):
        
        # Check if dataset is empty
        result = self.contact(self.db_name,"Select * From Database")
        
        if len(result.fetchall()) == 0:
            return 'Database is empty.'

        # Getting the younger employee details
        result = self.contact(self.db_name,'SELECT * FROM Database WHERE Birth_Date = (SELECT MAX(Birth_Date) FROM Database)')
        result = result.fetchall()[0]

        # converting output data
        younger_employee = self.data_to_dictionary(result)
        
        birth_date = younger_employee['birth_date']
        date_time_obj = datetime.strptime(birth_date,"%d-%m-%Y")
        time_difference1 = relativedelta(datetime.now(), date_time_obj).years

        # Getting the older employee details
        result = self.contact(self.db_name,'SELECT * FROM Database WHERE Birth_Date = (SELECT MIN(Birth_Date) FROM Database)')
        result = result.fetchall()[0]
        
        # converting output data
        older_employee = self.data_to_dictionary(result)

        birth_date = older_employee['birth_date']
        date_time_obj = datetime.strptime(birth_date,"%d-%m-%Y")
        time_difference2 = relativedelta(datetime.now(), date_time_obj).years

        average = (time_difference1 + time_difference2)/2
        
        return {'younger': younger_employee, 'older' : older_employee, 'average' : average }
    
    # converting output of dataset to dictionary
    def data_to_dictionary(self, input):
        output = {"id": list(input)[0] , "name" : list(input)[1] , "email": list(input)[2] ,
            "department": list(input)[3] , "salary": list(input)[4] , "birth_date": list(input)[5]}
        return output
