import psycopg2
from datetime import date, timedelta, datetime

#establishing connection with database server
con = psycopg2.connect(
    database="finalproject",
    user="postgres",
    password="postgres",
    host="localhost",
    port= '5432'
    )

cursor_obj = con.cursor()

# MEMBER FUNCTIONS
# updating member attributes
def manage_profile(member_id):
    choice = 0
    while (choice != 4):
        print("\n1. Update name",
              "\n2. Update fitness goals",
              "\n3. Update health metrics",
              "\n4. Return to member menu")
        choice = input("Select (1/2/3/4/5): ")

        # updating member name
        if choice == '1':
            first_name = input("Enter updated first name: ")
            last_name = input("Enter updated last name: ")
            cursor_obj.execute("UPDATE members SET first_name = %s WHERE member_id = %s", (first_name, member_id))
            con.commit()
            cursor_obj.execute("UPDATE members SET last_name = %s WHERE member_id = %s", (last_name, member_id))
            con.commit()
            print("Name sucessfully updated.")

        # updating member fitness goals
        elif choice == '2':
            weight_goal = input("Enter weight goal: ")
            time_goal = input("Enter time goal: ")
            cursor_obj.execute("UPDATE members SET weight_goal = %s WHERE member_id = %s", (weight_goal, member_id))
            con.commit()
            cursor_obj.execute("UPDATE members SET time_goal = %s WHERE member_id = %s", (time_goal, member_id))
            con.commit()
            print("Fitness goals successfully updated.")

        # updating member health metrics
        elif choice == '3':
            current_weight = input("Enter current weight: ")
            current_height = input("Enter current height: ")

            cursor_obj.execute("UPDATE members SET weight = %s WHERE member_id = %s;", (current_weight, member_id))
            con.commit()
            cursor_obj.execute("UPDATE members SET height = %s WHERE member_id = %s;", (current_height, member_id))
            con.commit()
            print("Health metrics successfully updated.")

        # return to member menu
        elif choice == '4':
            print("Returning to menu.")
            return

# member registration for classes INC
def class_register(member_id):

    class_id = input("Enter class id to register: ")

    # check if free for that class 
    # get start time for class id 
    # if start time != to anything in schedule 
        # register for class
    # else start time == to something in schedule 
        # time not free

    cursor_obj.execute("INSERT INTO schedule (members) VALUES (ARRAY[%s]) WHERE class_id = %s", (member_id, class_id))
    con.commit()
    print("Class added to schedule")

# display member dashboard
def display_member_dashboard(member_id):
    cursor_obj.execute("SELECT * FROM members WHERE member_id = %s", (member_id))
    member = cursor_obj.fetchall()
    columns = ['Member ID', 'First name', 'Last name', 'Weight goal', 'Time goal', 'Weight', 'Height', 'Payment due date']
    for i in range(len(member)):
        for j in range(len(columns)):
            print('%s: %s' % (columns[j], member[i][j]))

# display member schedule
def display_member_schedule(member_id):
    cursor_obj.execute("SELECT class_id, room_number, class_type, start_time, end_time, trainer FROM schedule WHERE %s = ANY(members) ORDER BY start_time ASC;", (member_id))
    member_schedule = cursor_obj.fetchall()

    print("Room   Type      Start Time     End Time    Trainer")
    for i in member_schedule:
        start = i[3].strftime('%H:%M:%S')
        end = i[4].strftime('%H:%M:%S')

        print(f"{i[1]:<6}{i[2]:<10}{start:<15}{end:<15}{i[5]:<20}")


# display member menu
def member_menu(member_id):
    choice = 0
    while(choice != 5):
        print("\n1. Manage profile",
            "\n2. Register for classes",
            "\n3. Display dashboard",
            "\n4. Display personal schedule",
            "\n5. Log out and return to main menu")
        choice = input("Select (1/2/3/4/5): ")
        if choice == '1':
            manage_profile(member_id)

        elif choice == '2':
            class_register(member_id)

        elif choice == '3':
            display_member_dashboard(member_id)

        elif choice == '4':
            display_member_schedule(member_id)

        # returns to main menu
        elif choice == '5':
            print("Returning to main menu.")
            return
# ##############################################
        
# TRAINER FUNCTIONS

# trainer sets times for when theyre available
def set_availability(trainer_id):
    start_time = input("Enter available start time (24 hour clock): ")
    end_time = input("Enter available end time (24 hour clock): ")

    index = int(start_time) - 7
    for i in range(int(end_time) - int(start_time)):
        cursor_obj.execute("UPDATE trainers SET available[%s] = TRUE WHERE trainer_id = %s;", (index, trainer_id))
        index += 1
        con.commit()

# view profile of members 
def view_members():
    first_name = input("Enter member first name to view: ")
    last_name = input("Enter member last name to view: ")

    cursor_obj.execute("SELECT member_id FROM members WHERE first_name = %s AND last_name = %s;", (first_name, last_name))
    member_id = cursor_obj.fetchall()[0]

    display_member_dashboard(member_id)

# display trainer schedule
def display_trainer_schedule(trainer_id):
    cursor_obj.execute("SELECT class_id, room_number, class_type, start_time, end_time, members FROM schedule WHERE trainer = %s ORDER BY start_time ASC;", (trainer_id))
    trainer_schedule = cursor_obj.fetchall()

    print("ClassID  Room   Type    Start Time     End Time    Members")
    for i in trainer_schedule:
        start = i[3].strftime('%H:%M:%S')
        end = i[4].strftime('%H:%M:%S')
        members = i[5]

        print(f"{i[0]:<10}{i[1]:<6}{i[2]:<8}{start:<15}{end:<15}",  members)

# display trainer menu INC
def trainer_menu(trainer_id):
    choice = 0
    while(choice != 4):
        print("\n1. Set availability",
            "\n2. View member profiles",
            "\n3. Display trainer schedule"
            "\n4. Exit")
        choice = input("Select (1/2/3/4): ")
        if choice == '1':
            set_availability(trainer_id) 

        elif choice == '2':
            view_members()

        elif choice == '3':
            display_trainer_schedule(trainer_id)

        # returns to main menu
        elif choice == '4':
            print("Returning to main menu.")
            return

# ##############################################

# ADMIN FUNCTIONS

# booking a room
def book_room():

    cursor_obj.execute("SELECT * from rooms")
    rooms = cursor_obj.fetchall()
    print("Room    Availability")
    print("          8      9      10     11    12     13     14     15    16    17")
    for i in rooms:
        times = i[1]  

        print(f"{i[0]:<7}", times)

    room_num = input("Enter room number: ")
    start_input = input("Enter start time: ")
    end_input = input("Enter end time: ")

    # if available[start_input-7] = TRUE
    cursor_obj.execute("SELECT trainer_id, first_name, last_name FROM trainers WHERE available[%s] = TRUE AND ;", (start_input-7))
    trainers = cursor_obj.fetchall()
    # cursor_obj.execute("SELECT trainer_id FROM trainers WHERE available[%s] = TRUE;", (end_input-7))
    end = cursor_obj.fetchall()


    # cursor_obj.execute("SELECT start_time FROM rooms WHERE number = %s", (room_num))
    # start_time = cursor_obj.fetchall()
    # cursor_obj.execute("SELECT end_time FROM rooms WHERE number = %s", (room_num))
    # end_time = cursor_obj.fetchall()


    # if start_input >= start_time & end_input <= end_time:
        

        # cursor_obj.execute("UPDATE rooms SET start_time = %s WHERE number = %s", (start_time, room_num))
        # how to check if you update start or end time ??????
        con.commit()
    
# signing out equipmement 
# def equipment_maintenance()
    
# updating the schedule
def update_schedule():
    room_num = input("Enter room number: ")
    class_type = input("Enter class type: ")
    start_time = input("Enter start time: ")
    end_time = input("Enter end time: ")
    trainer = input("Enter trainer id: ")

    # if room, times, trainer, etc available

# make a payment
def make_payment(first_name, last_name, payment_amt):
    choice = input("Make a payment for $%s: Y/N? " % payment_amt)
    if (choice == 'Y'):
        # add code to update payment information for member
        return True
    return False

# display admin menu INC
def admin_menu():
    choice = 0
    while(choice != 5):
        print("\n1. Room booking",
              "\n2. Equipment maintenance monitoring",
              "\n3. Update class schedule",
              "\n4. Process payments",
              "\n5. Exit")
        choice = input("Select (1/2/3/4/5): ")
        if choice == '1':
            book_room()

        elif choice == '2':
            equipment_maintenance()

        elif choice == '3':
            update_schedule()

        elif choice == '4':
            process_payment()
            # make_payment(first_name, last_name, payment_amt) ????????
            
        # returns to main menu
        elif choice == '5':
            print("Returning to main menu.")
            return

# ##############################################

# new member registration
def new_user():
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    current_date = date.today()
    if (make_payment(first_name, last_name, 800)) :
        new_date = current_date + timedelta(days=365)
        cursor_obj.execute("INSERT INTO members (first_name, last_name, payment_date) VALUES (%s, %s, %s);", (first_name, last_name, new_date))
        print("Welcome! You are now a member at BuffBuddy.")
    else:
        print("You have to make a payment to register as a member.")

# MAIN MENU 

# repeatedly displays menu till user chooses to exit. displays database operations.
def start_menu():
    choice = 0
    while choice != 5:
        print("LOGIN",
            "\n1. Member",
            "\n2. Trainer",
            "\n3. Admin Staff",
            "\n4. New Member",
            "\n5. Exit")

        choice = input("Select (1/2/3/4/5): ")

        if (choice == '1'):
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            cursor_obj.execute("SELECT first_name, last_name FROM members")
            result = cursor_obj.fetchall()
            exists = False
            for member in result:
                if (first_name in member and last_name in member):
                    exists = True
                    break
            if (exists):
                print("Login successful.")
                cursor_obj.execute("SELECT member_id FROM members WHERE first_name = %s AND last_name = %s",
                                   (first_name, last_name))
                member_id = cursor_obj.fetchall()[0]
                member_menu(member_id)

        elif (choice == '2'):
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            cursor_obj.execute("SELECT first_name, last_name FROM trainers")
            result = cursor_obj.fetchall()
            exists = False
            for trainer in result:
                if (first_name in trainer and last_name in trainer):
                    exists = True
                    break
            if (exists):
                print("Login successful.")
                cursor_obj.execute("SELECT trainer_id FROM trainers WHERE first_name = %s AND last_name = %s",
                                   (first_name, last_name))
                trainer_id = cursor_obj.fetchall()[0]
                trainer_menu(trainer_id)

        elif (choice == '3'):
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            cursor_obj.execute("SELECT first_name, last_name FROM admin_staff")
            result = cursor_obj.fetchall()
            exists = False
            for admin in result:
                if (first_name in admin and last_name in admin):
                    exists = True
                    break
            if (exists):
                print("Login successful.")
                cursor_obj.execute("SELECT admin_id FROM admin_staff WHERE first_name = %s AND last_name = %s",
                                   (first_name, last_name))
                admin_id = cursor_obj.fetchall()[0]
                admin_menu()

        elif (choice == '4'):
            new_user()

        elif (choice == '5'):
            exit()


start_menu()
