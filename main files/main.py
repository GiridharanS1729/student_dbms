import personalinfo as per
import academic as aca
while True:
    print("(1) Personal Details")
    print("(2) Academic Details")
    print("(3) Display all details ")
    s=input("Enter any one Option : ")
    if s=='1':
        per.choose()
    elif s=='2':
        aca.fin()
    elif s=='3':
        per.show_all()
        aca.display_all_records()
    else:
        print("Please Enter a valid Input.")