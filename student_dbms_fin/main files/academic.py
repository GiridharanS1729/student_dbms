
import mysql.connector
from prettytable import PrettyTable
from tabulate import tabulate

try:
    mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Giri@1729.S!",
            database="stu"
        )
    cursor = mydb.cursor()
except mysql.connector.Error as err:
    print(f"Error in connection: {err}")
def create_table():
    cursor.execute("""
        create table if not exists marks (
            Roll_Number INT PRIMARY KEY,
            Name VARCHAR(255),Subject_1 VARCHAR(50),
            Subject_2 VARCHAR(50),Subject_3 VARCHAR(50),
            Subject_4 VARCHAR(50),Subject_5 VARCHAR(50),
            Subject_6 VARCHAR(50),Total_Credits INT,
            GPA FLOAT,CGPA FLOAT,Outcome VARCHAR(10))
                """)

def calculate_gpa(subjects,total_cre):
    total_credits = 0
    mrks = 0
    for credit_grade in subjects:
        credit, grade = credit_grade.split(',')
        try:
            total_credits += int(credit)
            mrks += int(credit) * get_grade_value(grade)
        except ValueError:
            print(f"Invalid grade value: {grade}.")
    if total_credits == 0:
        return 0 
    elif total_credits!=total_cre:
        return -1
    gpa = mrks / total_credits
    return round(gpa, 2)

def get_grade_value(grade):
    grade_values = {'O': 10, 'A+': 9, 'A': 8, 'B+': 7, 'B': 6, 'C': 5, 'U': 0}
    return grade_values.get(grade.upper(), 0)

def calculate_cgpa( roll_number, current_gpa):
    try:
        cursor.execute("SELECT CGPA FROM marks WHERE Roll_Number=%s", (roll_number,))
        previous_cgpa = cursor.fetchone()
        if previous_cgpa:
            new_cgpa = (current_gpa + previous_cgpa[0]) / 2
        else:
            new_cgpa = current_gpa
        return round(new_cgpa, 2)
    except mysql.connector.Error as err:
        print(f"Error in cgpa calc: {err}")
        return None

def calculate_pf(subjects):
    pass_gra = {'O': 100, 'A+': 90, 'A': 80, 'B+': 70, 'B': 60, 'C': 50, 'U': 0}
    if any(grade.split(',')[1].upper() == 'U' for grade in subjects):
        return "Arrear"
    else:
        valid_subjects = [grade for grade in subjects if grade.split(',')[1].upper() != 'U']
        mrks = sum(pass_gra[grade.split(',')[1].upper()] * int(grade.split(',')[0]) for grade in valid_subjects)
        total_credits = sum(int(grade.split(',')[0]) for grade in valid_subjects)
        average_score = mrks / total_credits
        return "Pass" if average_score >= 50 else "Arrear"

def insert_data():
    try:
        roll_number = int(input("Enter Roll Number: "))
        name = input("Enter Name: ")
        subjects = []
        total_credits = int(input("Enter Total Number of Credits: "))
        for i in range(1, 7):
            subject_input = input(f"Enter marks for Subject {i} (format: credit,grade): ")
            subjects.append(subject_input)
        gpa = calculate_gpa(subjects,total_credits)
        cgpa = calculate_cgpa( roll_number, gpa)
        pf = calculate_pf(subjects)
        cursor.execute("""
            INSERT INTO marks (
                Roll_Number, Name, Subject_1, Subject_2, Subject_3,
                Subject_4, Subject_5, Subject_6, Total_Credits, GPA, CGPA, Outcome
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (roll_number, name,) + tuple(subjects) + (total_credits, gpa, cgpa, pf))
        print("Data inserted successfully!")
    except mysql.connector.Error as err:
        print(f"Error in insert: {err}")

def update_data():
    try:
        roll_number = int(input("Enter Roll Number: "))
        # name=input("Enter Your Name: ")
        subjects = []
        cursor.execute("SELECT * FROM marks WHERE Roll_Number=%s", (roll_number, ))
        existing_record = cursor.fetchone()
        if existing_record:
            total_credits = int(input("Enter Total Number of Credits: "))
            for i in range(1, 7):
                subject_input = input(f"Enter updated marks for Subject {i} (format: credit,grade): ")
                subjects.append(subject_input)
            gpa = calculate_gpa(subjects,total_credits)
            if gpa!=-1:
                cgpa = calculate_cgpa( roll_number, gpa)
                pf = calculate_pf(subjects)
                cursor.execute("""
                    UPDATE marks
                    SET Subject_1=%s, Subject_2=%s, Subject_3=%s,
                        Subject_4=%s, Subject_5=%s, Subject_6=%s,
                        Total_Credits=%s, GPA=%s, CGPA=%s, Outcome=%s
                    WHERE Roll_Number=%s 
                """, tuple(subjects) + (total_credits, gpa, cgpa, pf, roll_number))
                print("Data updated successfully!")
            else:
                print("Number of credits not matching.")
        else:
            print("Name or Roll Number not matching. No data updated.")
    except mysql.connector.Error as err:
        print(f"Error in update: {err}")

def display_data( roll_number):#using tabulate package
    try:
        cursor.execute("""
            SELECT * FROM marks
            WHERE Roll_Number=%s
        """, (roll_number,))
        data = cursor.fetchone()
        if data:
            table_data = [
                ["Roll Number", data[0]],
                ["Name", data[1]],
                ["Total Credits", data[8]],
                ["Subject 1", data[2]],
                ["Subject 2", data[3]],
                ["Subject 3", data[4]],
                ["Subject 4", data[5]],
                ["Subject 5", data[6]],
                ["Subject 6", data[7]],
                ["Current Semester GPA", data[9]],
                ["CGPA up to Current Semester", data[10]],
                ["Pass/Fail", data[11]],
            ]
            table = tabulate(table_data, tablefmt="grid")
            print(table)
        else:
            print("No data found for the given roll number and name.")
    except mysql.connector.Error as err:
        print(f"Error in display: {err}")

def display_data1( roll_number):#using tabulate package
    try:
        cursor.execute("""
            SELECT * FROM marks
            WHERE Roll_Number=%s
        """, (roll_number,))
        data = cursor.fetchone()
        if data:
            table_data = [
                ["Total Credits", data[8]],
                ["Subject 1", data[2]],
                ["Subject 2", data[3]],
                ["Subject 3", data[4]],
                ["Subject 4", data[5]],
                ["Subject 5", data[6]],
                ["Subject 6", data[7]],
                ["Current Semester GPA", data[9]],
                ["CGPA up to Current Semester", data[10]],
                ["Pass/Fail", data[11]],
            ]
            table = tabulate(table_data, tablefmt="grid")
            print(table)
        else:
            print("No data found for the given roll number and name.")
    except mysql.connector.Error as err:
        print(f"Error in display: {err}")

def display_all_records():
    try:
        cursor.execute("SELECT * FROM marks")
        data = cursor.fetchall()
        if data:
            print("Academic Details : ")
            table = PrettyTable()
            table.field_names = ["Roll Number", "Name", "Subject 1", "Subject 2", "Subject 3", "Subject 4", "Subject 5", "Subject 6", "Total Credits", "GPA", "CGPA", "Outcome"]
            for row in data:
                table.add_row(row)
            print(table)
        else:
            print("No records found.")
    except mysql.connector.Error as err:
        print(f"Error in display_all_records: {err}")

def delete_data():
    try:
        roll_number = int(input("Enter Roll Number to delete: "))
        cursor.execute("SELECT * FROM marks WHERE Roll_Number=%s", (roll_number,))
        existing_record = cursor.fetchone()
        if existing_record:
            cursor.execute("DELETE FROM marks WHERE Roll_Number=%s", (roll_number,))
            print(f"Record for Roll Number {roll_number} deleted successfully!")
        else:
            print(f"No record found for Roll Number {roll_number}.")
    except mysql.connector.Error as err:
        print(f"Error in delete: {err}")

def choose():
    print("\n\n(1) Insert New Data")
    print("(2) Update Existing Data")
    print("(3) Display Particular Record")
    print("(4) Display all Records")
    print("(5) Delete Record by Roll Number")
    print("(6) Exit")

def fin():
    try:
        create_table()
        while True:
            choose()
            option = input("\nEnter any one option: ")
            match option:
                case '1':
                    insert_data()
                case '2':
                    update_data()
                case '3':
                    roll_number = int(input("Enter Roll Number: "))
                    display_data(roll_number)
                case '4':
                    display_all_records()
                case '5':
                    delete_data()
                case '6':
                    print("Exited")
                    break
                case _:
                    print("Invalid option. Please choose a valid option.")
            mydb.commit()
    except mysql.connector.Error as err:
        print(f"Error in main: {err}")

# fin()