import personalinfo as per
import academic as aca
while True:
    print("(1) Personal Details")
    print("(2) Academic Details")
    print("(3) Display all details")
    print("(4) Display report for single data \n")
    s=input("Enter any one Option : ")
    print("\n")
    if s=='1':
        per.choose()
    elif s=='2':
        aca.fin()
    elif s=='3':
        per.show_all()
        aca.display_all_records()
    elif s=='4':
        r=input("Enter Roll number to search : ")
        per.show_particular(r)
        aca.display_data1(r)
    else:
        print("Please Enter a valid Input.")