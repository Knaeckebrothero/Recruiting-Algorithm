import csv
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
batch_size = 1000  # Number of rows to insert in each batch

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

create_table_relationships = '''CREATE TABLE Fact_EmployeeSkills (
    EmployeeID INT,
    SkillID INT,
    FOREIGN KEY (EmployeeID) REFERENCES DWH2.DIM_TJB_Employee(EmployeeID),
    FOREIGN KEY (SkillID) REFERENCES DWH2.DIM_TJB_Skills(SkillID)
); '''

cursor = mydb.cursor()

# #Uncomment to create tables if neccesary
# try:
#     cursor.execute(create_table_relationships)
#     mydb.commit()
# except:
#     print('Error Occured while creating Table!')

with open(file_name, newline='\n') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    header = next(csvreader)

    # Identify skill columns
    non_skill_columns = ['Age', 'EdLevel', 'Employment', 'Gender', 'MainBranch', 'YearsCode', 'Country', 'PreviousSalary', 'ComputerSkills', 'Employed']
    skill_columns = [col for col in header if col not in non_skill_columns]

    # Insert skill names into DIM_TJB_Skills if not exists
    skill_ids = {}
    for skill in skill_columns:
        cursor.execute('SELECT SkillID FROM DWH2.DIM_TJB_Skills WHERE SkillName = %s', (skill,))
        result = cursor.fetchone()
        if result is None:
            cursor.execute('INSERT INTO DWH2.DIM_TJB_Skills (SkillName) VALUES (%s)', (skill,))
            mydb.commit()
            skill_id = cursor.lastrowid
        else:
            skill_id = result[0]
        skill_ids[skill] = skill_id

    # Batch processing
    batch_data_employee = []
    batch_data_skills = []
    row_number = 0
    for row in csvreader:
        row_number += 1
        if len(row) < len(header):
            print(f"Skipping row {row_number}: insufficient columns")
            continue

        try:
            # Assume EmployeeID is provided in the CSV (adjust the index if necessary)
            EmployeeID = int(row[0])
            Age = row[1]
            EdLevel = row[2]
            Employment = row[3]
            Gender = row[4]
            MainBranch = row[5]
            YearsCode = row[6]
            Country = row[7]
            PreviousSalary = float(row[8])
            ComputerSkills = row[9]
            Employed = bool(int(row[10]))

            # Add employee data to batch
            batch_data_employee.append((EmployeeID, Age, EdLevel, Employment, Gender, MainBranch, YearsCode, Country, PreviousSalary, ComputerSkills, Employed))

            # Handle skills as columns with binary values
            for i, skill in enumerate(skill_columns, start=len(non_skill_columns) + 1):
                if row[i] == '1':  # Employee knows this skill
                    skill_id = skill_ids[skill]
                    batch_data_skills.append((EmployeeID, skill_id))

            if len(batch_data_employee) >= batch_size:
                sql_query_employee = "REPLACE INTO DWH2.DIM_TJB_Employee (EmployeeID, Age, EdLevel, Employment, Gender, MainBranch, YearsCode, Country, PreviousSalary, ComputerSkills, Employed) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.executemany(sql_query_employee, batch_data_employee)
                mydb.commit()
                batch_data_employee = []

            if len(batch_data_skills) >= batch_size:
                sql_query_skills = "INSERT IGNORE INTO DWH2.Fact_TJB_EmployeeSkills (EmployeeID, SkillID) VALUES (%s, %s)"
                cursor.executemany(sql_query_skills, batch_data_skills)
                mydb.commit()
                batch_data_skills = []

        except IndexError as e:
            print(f"Error processing row {row_number}: {e}")
            continue

    # Insert any remaining data
    if batch_data_employee:
        sql_query_employee = "REPLACE INTO DWH2.DIM_TJB_Employee (EmployeeID, Age, EdLevel, Employment, Gender, MainBranch, YearsCode, Country, PreviousSalary, ComputerSkills, Employed) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.executemany(sql_query_employee, batch_data_employee)
        mydb.commit()

    if batch_data_skills:
        sql_query_skills = "INSERT IGNORE INTO DWH2.Fact_TJB_EmployeeSkills (EmployeeID, SkillID) VALUES (%s, %s)"
        cursor.executemany(sql_query_skills, batch_data_skills)
        mydb.commit()

mydb.close()
