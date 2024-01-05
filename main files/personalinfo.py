# studinfo.py
import mysql.connector as mc
from prettytable import PrettyTable

mydb = mc.connect(
    host = "localhost",
    user = "root",
    password = "Giri@1729.S!",
    database = "stu"
    )
cur = mydb.cursor()

table_name = "details"

all_table = PrettyTable()
all_table.field_names = ["Roll Number", "Name", "Gender", "Date Of Birth", "Mobile Number", "Email Id", "Department", "Year of Study"]

one_table = PrettyTable()
one_table.field_names = ["Roll Number", "Name", "Gender", "Date Of Birth", "Mobile Number", "Email Id", "Department", "Year of Study"]


global x
x=1
def option(s):
    match s:
        case '1':
            insert_row()
        case '2':
            print("(1) All Details ")
            print("(2) Particular Details ")
            opt = input('Enter your choice : ')
            if opt == '1':
                show_all()
            elif opt == '2':
                show_particular(input("Enter Roll Number to search : "))
            else:
                print("Invalid choice.")
        case '3':
            update_one(input("Enter Roll number to update : "))
        case '4':
            print("(1) Delete whole table ")
            print("(2) Delete particular Data ")
            ch = input('Enter your choice : ')
            if ch == '1':
                delete_table(table_name)
            elif ch == '2':
                delete_one(input("Enter Roll number to delete : "))
            else:
                print("Invalid choice.")
        case '5':
            print("Exited")
            return

def create_table():
    try:
        # check if tables have present or not
        cre_det_tab = (f"CREATE TABLE IF NOT EXISTS {table_name} (Roll varchar(10) PRIMARY KEY, Name varchar(20), Gender varchar(10), DOB varchar(10), MobileNumber varchar(13), EmailID varchar(50), Department varchar(20), YearOfStudy varchar(10))")
        cur.execute(cre_det_tab)
        mydb.commit()
    except mc.Error as e:
        print("Error in creating a table as : ", e)

def insert_row():
    ins = (f"INSERT INTO {table_name} (Roll, Name, Gender, DOB, MobileNumber, EmailID, Department, YearOfStudy) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
    roll = int(input('Enter Roll Number: '))
    name = input('Enter Name : ')
    gender = input('Enter Gender : ')
    dob = input('Enter Date of Birth : ')
    mob = input('Enter Mobile Number : ')
    email = input('Enter Email ID : ')
    dept = input('Enter Department : ')
    year = input('Enter Year of Study : ')
    val = (roll, name, gender, dob, mob, email, dept, year)
    all_table.add_row(val)
    cur.execute(ins, val)
    mydb.commit()
    print("Successfully inserted.")

def add_to_all():
    try:
        sel = f"SELECT * FROM {table_name}"
        cur.execute(sel)
        rows = cur.fetchall()
        if len(rows) > 0:
            print("\nPersonal Details : \n")
            for row in rows:
                all_table.add_row([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]])
    except mc.Error as e:
        print("Error in add all: ",e)

def show_all():
    try:
        sel = f"SELECT * FROM {table_name}"
        cur.execute(sel)
        rows = cur.fetchall()
        global x
        if len(rows) > 0:
            print("\nPersonal Details : \n")
            if x==1:
                for row in rows:
                    all_table.add_row([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]])
            print(all_table)
        else:
            print("No data found.")
    except:
        print("Table not found.")
    finally:
        x+=1

def show_particular(r):
    try:
        sel = f"SELECT * FROM {table_name} WHERE Roll=%s"
        cur.execute(sel, (r,))
        res = cur.fetchone()
        if res!=None:
            one_table.clear_rows()
            one_table.add_row([res[0], res[1], res[2], res[3], res[4], res[5], res[6], res[7]])
            print(one_table)
        else:
            print("Data not Found.\n")
    except:
        print("Table not found.")

def update_one(roll):
    nme = input('\nEnter New Name : ')
    gndr = input('Enter New Gender : ')
    dOB = input('Enter new DOB : ')
    mblNum = input('Enter New Mobile Number : ')
    emlId = input('Enter New Email Id : ')
    dept = input('Enter New Department : ')
    year = input('Enter New Year of Study : ')
    upd = f"UPDATE {table_name} SET Name=%s, Gender=%s, DOB=%s, MobileNumber=%s, EmailID=%s, Department=%s, YearOfStudy=%s WHERE Roll=%s"
    val = (nme, gndr, dOB, mblNum, emlId, dept, year, roll)
    cur.execute(upd, val)
    mydb.commit()
    print("Successfully Updated.\n")

def delete_table(tab_name):
    a = f"DROP TABLE IF EXISTS {tab_name}"
    cur.execute(a)
    mydb.commit()
    print("Table has been deleted.\n")

def delete_one(roll):
    sel = f"SELECT * FROM {table_name} WHERE Roll={roll}"
    cur.execute(sel)
    rec = cur.fetchone()
    if rec:
        a = f"DELETE FROM {table_name} WHERE Roll=%s"
        cur.execute(a, (roll,))
        mydb.commit()
        print("Deleted Successfully.\n")
    else:
        print("No data found in the Record.\n")
try:
    
    def choose():
        while True:
            create_table()
            print("(1) Insert New Data")
            print("(2) Display")
            print("(3) Update")
            print("(4) Delete")
            print("(5) Exit")
            # print(one_table)
            op = (input("Enter your option: "))
            option(op)
except mc.Error as e:
    print("error in main last : ",e)
# choose()
# print(one_table)
# show_particular(input("E : "))