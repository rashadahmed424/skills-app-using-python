import sqlite3
db=sqlite3.connect("app.db")
cr=db.cursor()
cr.execute("create table if not exists skills (Name text,Progress integer, User_ID integer)")
cr.execute("create table if not exists login (User_ID,Pass )")
def another_operation():
    print("DO You Want Another Operation ? ")
    op_test=input("For Yes Enter y For No Enter n : ").strip().lower()
    if op_test=="y":
        operation()
    else:
        print("It's Ok , GOODBYE ")
        commit_close()   
def operation():
    input_message=""" What do you want ?
                        "s" To Show Skills 
                        "a" To Add a Skill
                        "d" To Delete a Skill
                        "u" To Update a Skill Progress
                """
    input_text=input(input_message).strip().lower()
    if input_text=="s":
        show_skills()
    if input_text=="a":
        add_skill()
    if input_text=="d":
        delete_skill()
    if input_text=="u":
        update_skill()    

def commit_close():
    db.commit()
    db.close()
    print("Data Base Is Closed")

def show_skills():

    cr.execute(f"select * from skills where User_ID='{uid}' ")
    result=cr.fetchall()
    if result[0][0]==None:
        print("There Is No Skill To Show  ")
    else:  
        print("Showing Skills With Progress")  
        for row in result:
            print(f"Skill Name Is => {row[0]} ",end=" ")
            print(f"And Its Progress Is => {row[1]}%")
    another_operation()

def add_skill():

    sk=input("Write The Skill Name : ").strip().capitalize()
    cr.execute(f"select * from skills where Name='{sk}' and User_ID='{uid}'")
    check=cr.fetchone()
    if check == None:
        prog=int(input("Write The Skill Progress : "))
        cr.execute(f"select * from skills where Name is NULL and User_ID='{uid}'")
        empty_check=cr.fetchone()
        if empty_check==None:
            cr.execute(f"insert into skills values('{sk}','{prog}','{uid}') ")
        else:
            cr.execute(f"update skills set Name='{sk}',Progress='{prog}' where User_ID='{uid}'")
        print("Your Skill Is Added ")
    else:
        print("This Skill Is Already Exists , Do You Want To Update Its Progress ? ")
        yn=input("For Yes Enter y For No Enter n : ").strip().lower() 
        if yn=="y":
            prog=input("Write The New Skill Progress : ") 
            cr.execute(f"update skills set Progress='{prog}' where Name='{sk}' and User_ID='{uid}'")   
        elif yn=="n":
            print("Thanks For Answer ")     
        else:
            print("Not Acceptable Answer , Please Try Again ")
    db.commit()        
    another_operation()        
    

def delete_skill():

    sk=input("Write The Skill Name ").strip().capitalize()
    cr.execute(f"delete from skills where Name='{sk}' and User_ID='{uid}'")
    print(f"Skill '{sk} Is Deleted ")
    db.commit()
    another_operation()
    

def update_skill():
    
    sk=input("Write The Skill Name ").strip().capitalize()
    cr.execute(f"select * from skills where Name='{sk}' and User_ID='{uid}' ")
    chk=cr.fetchone()
    if chk=None:
        print("This Skill Is Not Found")
        another_operation()
    else:
        prog=input("Write The New Skill Progress : ") 
        cr.execute(f"update skills set Progress='{prog}' where Name='{sk}' and User_ID='{uid}'")
        print("Your Skill Is Updated")
        db.commit()
        another_operation()


print("Hello ")
print("Log-in or Sign-up ? ")
log=input("Press 'l' For Log-in or 's' For Sign-up ").strip().lower()
if log =="s":
    id=int(input("Enter Your ID : "))
    cr.execute(f"select User_ID from login where User_ID='{id}'")
    id_test=cr.fetchone()
    if id_test== None:
        pas=input("Enter Your Password : ")
        cr.execute(f"insert into login values('{id}','{pas}')")
        cr.execute(f"insert into skills (User_ID) values('{id}')")
        print("Your Sign-up Is Done ")
        db.commit()
        uid=id
        another_operation()
    else:
        print("There Is User With Same Id , Do You Want to Show His Skills ? ")
        syn=input("Enter 'y' For Yes or 'n' For NO : ").strip().lower()
        if syn=="y":  
            show_skills()
            
        else:
            another_operation()
elif log=="l":

   
     count=5
     for i in range(count):
          id=int(input("Enter Your ID : "))
          pas=input("enter your password ").strip()
          cr.execute(f"select * from login where Pass='{pas}' and User_ID='{id}'")
          test=cr.fetchone()
          if test==None:
            print("Your ID or Password Is Wrong , Try Again")
            print(f"You Have {count-1} Tries Left")
            count-=1
          else:
                uid=id
                operation()
                break
          if count==0:
              print("Try Again Later")
              commit_close()
    
        
else:
    print("Not Acceptable Answer")
        









