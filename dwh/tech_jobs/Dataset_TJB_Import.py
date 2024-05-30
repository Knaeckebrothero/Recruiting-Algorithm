import csv
import mysql.connector
import pymysql

#Conncetion with DW
ssl_config = {
    'ca': './Datasets/ca.pem',
    'cert': './Datasets/client-cert.pem',
    'key': './Datasets/client-key.pem'
}

mydb = pymysql.connect(
    host='',
    port=,
    user='',
    password='',
    database='',
    ssl_ca = ssl_config['ca'],
    ssl_cert = ssl_config['cert'],
    ssl_key = ssl_config['key'])

#File to upload
file_name = './Datasets/techjobs_skill.csv'

#Create TAble Employees
create_table_employees = '''CREATE TABLE IF NOT EXISTS DIM_TJB_Employee (
    EmployeeID INT PRIMARY KEY,
    Age VARCHAR(5),
    EdLevel VARCHAR(100),
    Employment INT,
    Gender VARCHAR(50),
    MainBranch VARCHAR(10),
    YearsCode INT,
    Country VARCHAR(100),
    PreviousSalary VARCHAR(50),
    ComputerSkills INT,
    Employed INT
); '''

create_table_skills = '''CREATE TABLE DIM_TJB_Skills (
    SkillID INT AUTO_INCREMENT PRIMARY KEY,
    SkillName VARCHAR(100) UNIQUE
); '''

create_table_relationships = ''' CREATE TABLE Fact_EmployeeSkills (
    EmployeeID INT,
    SkillID INT,
    FOREIGN KEY (EmployeeID) REFERENCES DIM_TJB_Employee(EmployeeID),
    FOREIGN KEY (SkillID) REFERENCES DIM_TJB_Skills(SkillID)
); '''

cursor = mydb.cursor()

#Uncomment to create tables if neccesary
# try:
#     cursor.execute(create_table_employees)
#     mydb.commit()
# except:
#     print('Error Occured while creating Table!')

#Insert data into DW
with open(file_name, newline='\n') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    header = next(csvreader)

    #Create list with all skills
    non_skill_columns = ['Age', 'EdLevel', 'Employment', 'Gender', 'MainBranch', 'YearsCode', 'Country',
                         'PreviousSalary', 'ComputerSkills', 'Employed']
    skill_columns = [col for col in header if col not in non_skill_columns]

    #Upload all skills into DIM_TJB_Skill table
    skill_ids = {}
    for skill in skill_columns:
        cursor.execute('SELECT SkillID FROM DIM_TJB_Skills WHERE SkillName = %s', (skill,))
        result = cursor.fetchone()
        if result is None:
            cursor.execute('INSERT INTO DIM_TJB_Skills (SkillName) VALUES (%s)', (skill,))
            mydb.commit()
            skill_id = cursor.lastrowid
        else:
            skill_id = result[0]
        skill_ids[skill] = skill_id

    #Loop to check all rows to be uploaded
    for row in csvreader:

        print('\n')
        print(row)
        print('Started Inserting......')

        #Uncomment to populate DIM_TJB_Employees table
        # EmployeeID = row[0]
        # Age = row[1]
        # EdLevel = row[2]
        # Employment = row[3]
        # Gender = row[4]
        # MainBranch = row[5]
        # YearsCode = row[6]
        # Country = row[7]
        # PreviousSalary = row[8]
        # ComputerSkills = row[9]
        # Employed = row[10]
        #
        # sql_query = "INSERT INTO DWH1.DIM_TJB_Employee (EmployeeID, Age, EdLevel, Employment, Gender, MainBranch, YearsCode, Country, PreviousSalary, ComputerSkills, Employed) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (
        #     EmployeeID, Age, EdLevel, Employment, Gender, MainBranch, YearsCode, Country, PreviousSalary, ComputerSkills, Employed)
        # try:
        #     cursor.execute(sql_query)
        #     mydb.commit()
        # except:
        #     print('Error: Unable to Insert The Data!')

        # Assume EmployeeID is provided in the CSV
        EmployeeID = row[0]

        # Handle skills as columns with binary values [0 = Doesnt know the skill, 1= Do know the skill]
        for i, skill in enumerate(skill_columns, start=len(non_skill_columns)):
            if row[i] == '1':  # Employee knows this skill
                skill_id = skill_ids[skill]

                # Insert into Fact_EmployeeSkills with ID
                sql_query = "INSERT INTO FACT_TJB_EmployeeSkills (EmployeeID, SkillID) VALUES (%s, %s)"

                try:
                    cursor.execute(sql_query, (EmployeeID, skill_id))
                    mydb.commit()
                except mysql.connector.Error as err:
                    print(f'Error: Unable to Insert The Data! {err}')

mydb.close()
