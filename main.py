import studinfo
import acad
print("(1) Personal Details")
print("(2) Academic Details")
print("(3) Display all details ")
s=input("Enter any one Option : ")
if s=='1':
    studinfo.choose()
elif s=='2':
    acad.fin()
elif s=='3':
    studinfo.show_all()
    acad.display_all_records()
else:
    print("Please Enter a valid Input.")