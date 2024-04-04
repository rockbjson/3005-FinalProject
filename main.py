import psycopg2
from datetime import date, timedelta, datetime, time

#establishing connection with database server
con = psycopg2.connect(
    database="finalproject",
    user="postgres",
    password="37293",
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
            weight_goal = input("Enter weight goal (in lbs): ")
            running_goal = input("Enter running goal (in kilometres): ")
            cursor_obj.execute("UPDATE members SET weight_goal = %s WHERE member_id = %s", (weight_goal, member_id))
            con.commit()
            cursor_obj.execute("UPDATE members SET running_goal = %s WHERE member_id = %s", (running_goal, member_id))
            con.commit()
            print("Fitness goals successfully updated.")

        # updating member health metrics
        elif choice == '3':
            current_weight = input("Enter current weight (in lbs): ")
            current_height = input("Enter current height (in cm): ")

            cursor_obj.execute("UPDATE members SET weight = %s WHERE member_id = %s;", (current_weight, member_id))
            con.commit()
            cursor_obj.execute("UPDATE members SET height = %s WHERE member_id = %s;", (current_height, member_id))
            con.commit()
            print("Health metrics successfully updated.")

        # return to member menu
        elif choice == '4':
            print("Returning to menu.")
            return

# member registration for classes
def class_register(member_id):
    #display classes
    cursor_obj.execute("SELECT class_id, room_number, schedule.class_type, start_time, end_time, first_name FROM schedule JOIN trainers ON schedule.trainer = trainers.trainer_id ORDER BY class_id ASC;", (member_id))
    classes = cursor_obj.fetchall()

    print("ClassID   Room      Type        Start Time     End Time      Trainer")
    for i in classes:
        start = i[3].strftime('%H:%M:%S')
        end = i[4].strftime('%H:%M:%S')

        print(f"{i[0]:<10}{i[1]:<10}{i[2]:<12}{start:<15}{end:<14}{i[5]:<20}")

    class_request = input("Enter class id to register: ")

    cursor_obj.execute("SELECT start_time FROM schedule WHERE class_id = %s", (class_request))
    start_input = cursor_obj.fetchall()
    cursor_obj.execute("SELECT end_time FROM schedule WHERE class_id = %s", (class_request))
    end_input = cursor_obj.fetchall()

    if not start_input:
        print("Class does not exist")
        return

    cursor_obj.execute("SELECT start_time, end_time FROM schedule WHERE %s = ANY(members)", (member_id))
    member_schedule = cursor_obj.fetchall()

    cursor_obj.execute("SELECT class_id FROM schedule WHERE %s = ANY(members)", (member_id))
    class_id_sched = cursor_obj.fetchall()

    registered = False
    for class_id in class_id_sched:
        for id in class_id:
            if int(class_request) == int(id):
                registered = True
                break

    conflict = False
    for start_time in member_schedule:
        for time in start_time:
            for hours in start_input:
                if hours == time:
                    conflict = True
                    break

    if registered == True:
        print("Already registerd in this class")

    elif conflict == False and registered == False:
        cursor_obj.execute("UPDATE schedule SET members = array_append(members, %s) WHERE class_id = %s;", (member_id, class_request))
        con.commit()
        print("Class added to schedule")

    else:
        print("Requested class conflicts with your schedule")

# member registration for private session
def session_register(member_id):

    # show trainer schedules??? 
    # or some schedule???? idk

    first_name = input("Enter requested trainer's first name: ")
    last_name = input("Enter requested trainer's last name: ")

    cursor_obj.execute("SELECT trainer_id FROM trainers WHERE first_name = %s AND last_name = %s", (first_name, last_name))
    trainer_request = cursor_obj.fetchall()

    if not trainer_request:
        print("Trainer does not exist")
        return
    else:
        trainer_request = trainer_request[0]
    
    # show specific trainers schedule?

    start_time = input("Enter start time with trainer (24 hour clock, on the hour only): ")
    end_time = input("Enter end time with trainer (24 hour clock, on the hour only): ")

    if int(start_time) < 8 or int(end_time) < 8:
        print("Times are outside of BuffBuddy hours or incorrect format.")
        return

    start_index = int(start_time)-8
    end_index = int(end_time)-8

    cursor_obj.execute("SELECT available FROM trainers WHERE trainer_id = %s", (trainer_request))
    trainer_times = cursor_obj.fetchall()

    cursor_obj.execute("SELECT EXTRACT(HOUR FROM start_time) FROM schedule WHERE %s = ANY(members)", (member_id))
    member_times = cursor_obj.fetchall()

    open_trainer = True
    for available in trainer_times:
        for availability in available:
            for times in availability[start_index:end_index]:
                if times == False:
                    open_trainer = False
                    break
    
    open_member = True
    for start in member_times:
        for time in start:
            if int(start_time) == int(time):
                open_member = False
                break

    if open_trainer == True and open_member == True:
        cursor_obj.execute("SELECT first_name, last_name FROM members WHERE member_id = %s", (member_id))
        names = cursor_obj.fetchall()
        make_payment(names[0][0], names[0][1], 80)

        cursor_obj.execute(("SELECT times FROM rooms;"))
        rooms = cursor_obj.fetchall()

        room_number = 0

        index1 = 1
        for times in rooms:
            for available in times:
                for open in available[start_index:end_index]:
                    if open == True:
                        room_number = index1
                    index1 += 1

        j = int(start_time) - 7
        for i in range(int(end_time) - int(start_time)):
            cursor_obj.execute("UPDATE rooms SET times[%s] = FALSE WHERE number = %s;", (j, room_number))
            j += 1
            con.commit()

        index2 = int(start_time) - 7
        for i in range(int(end_time) - int(start_time)):
            cursor_obj.execute("UPDATE trainers SET available[%s] = FALSE WHERE trainer_id = %s;", (index2,
                                                                                                    trainer_request))
            index2 += 1
            con.commit()
        print("Personal session added to schedule")

    elif open_trainer == False and open_member == True: 
        print("%s %s is not free at these times" % (first_name, last_name))

    elif open_trainer == True and open_member == False: 
        print("You have another class or session at this time")

    else: 
        print("You and %s %s are both not free at this time" % (first_name, last_name))

# display member dashboard
def display_member_dashboard(member_id):
    cursor_obj.execute("SELECT * FROM members WHERE member_id = %s", (member_id))
    member = cursor_obj.fetchall()
    print("First name      Last name       Weight goal      Running goal        Weight      Height      Payment due ")
    for i in member:
        first_name = i[1] if i[1] is not None else "None"
        last_name = i[2] if i[2] is not None else "None"
        weight_goal = i[3] if i[3] is not None else "None"
        running_goal = i[4] if i[4] is not None else "None"
        weight = i[5] if i[5] is not None else "None"
        height = i[6] if i[6] is not None else "None"
        date = i[7].strftime('%Y-%m-%d') if i[7] is not None else "None"
        print(f"{first_name:<16}{last_name:<15}{weight_goal:<0} lbs {running_goal:>17} km {weight:>8} lbs"
              f" {height:>14} cm {date:<14}")

# display member schedule
def display_member_schedule(member_id):
    cursor_obj.execute("SELECT class_id, room_number, schedule.class_type, start_time, end_time, first_name FROM schedule JOIN trainers ON schedule.trainer = trainers.trainer_id WHERE %s = ANY(members) ORDER BY start_time ASC;", (member_id))
    member_schedule = cursor_obj.fetchall()

    print("Room    Type        Start Time     End Time      Trainer")
    for i in member_schedule:
        start = i[3].strftime('%H:%M:%S')
        end = i[4].strftime('%H:%M:%S')

        print(f"{i[1]:<8}{i[2]:<12}{start:<15}{end:<15}{i[5]:<14}")

def renew_membership(member_id):
    cursor_obj.execute("SELECT payment_date FROM members WHERE member_id = %s", (member_id))
    #print(cursor_obj.fetchall()[0][2])
    payment_date = cursor_obj.fetchall()[0][0]
    formatDate = payment_date.strftime('%Y-%m-%d')
    print("Your current payment due date is: %s"% (formatDate))
    cursor_obj.execute("SELECT first_name FROM members WHERE member_id = %s", (member_id))
    first_name = cursor_obj.fetchall()[0][0]
    cursor_obj.execute("SELECT last_name FROM members WHERE member_id = %s", (member_id))
    last_name = cursor_obj.fetchall()[0][0]
    make_payment(first_name, last_name, 800)

# display member menu
def member_menu(member_id):
    choice = 0
    while(choice != 5):
        print("\n1. Manage profile",
            "\n2. Register for classes",
            "\n3. Register for personal session",
            "\n4. Display dashboard",
            "\n5. Display personal schedule",
            "\n6. Renew membership"
            "\n7. Log out and return to main menu")
        choice = input("Select (1/2/3/4/5): ")
        if choice == '1':
            manage_profile(member_id)

        elif choice == '2':
            class_register(member_id)

        elif choice == '3':
            session_register(member_id)
            
        elif choice == '4':
            display_member_dashboard(member_id)

        elif choice == '5':
            display_member_schedule(member_id)

        elif choice == '6':
            renew_membership(member_id)

        # returns to main menu
        elif choice == '7':
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

    if len(cursor_obj.fetchall()) == 0:
        print("Invalid first or last name.")
        return

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

# display trainer menu 
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
    print("          8      9     10    11    12    13    14    15    16")
    for i in rooms:
        times = i[1]

        print(f"{i[0]:<7}", times)

    start_input = input("Enter start time: ")
    end_input = input("Enter end time: ")
    
    cursor_obj.execute(("SELECT times FROM rooms;"))
    rooms = cursor_obj.fetchall()

    start_index = int(start_input)-8
    end_index = int(end_input)-8
    
    open_rooms = []

    index = 1
    for times in rooms:
        for available in times:
            for open in available[start_index:end_index]:
                if open == True: 
                    open_rooms.append(int(index))
                index+=1

    if not open_rooms:
        print("No rooms available for this times")
        return
    
    first_name = input("Enter requested trainer's first name: ")
    last_name = input("Enter requested trainer's last name: ")

    cursor_obj.execute("SELECT trainer_id FROM trainers WHERE first_name = %s AND last_name = %s", (first_name, last_name))
    trainer_request = cursor_obj.fetchall()

    if not trainer_request:
        print("Trainer does not exist")
        return
    else:
        trainer_request = trainer_request[0]

    cursor_obj.execute("SELECT available FROM trainers WHERE trainer_id = %s", (trainer_request))
    trainer_times = cursor_obj.fetchall()

    open_trainer = True
    for available in trainer_times:
        for availability in available:
            for times in availability[start_index:end_index]:
                if times == False:
                    open_trainer = False
                    break

    if open_trainer == False:
        print("Trainer is not available at this time")
        return 
    
    print("Available rooms: ", open_rooms)

    choice = input("Enter room number: ")

    if int(choice) not in open_rooms:
        print("Room %s is not available at this time", choice)
        return
    
    start_string = time(int(start_input), 0, 0)
    end_string = time(int(end_input), 0, 0)

    cursor_obj.execute("SELECT class_type FROM trainers WHERE trainer_id = %s", (trainer_request))
    class_type = cursor_obj.fetchall()[0]

    cursor_obj.execute("INSERT INTO schedule (room_number, class_type, start_time, end_time, trainer) VALUES (%s, %s, %s, %s, %s);", (choice, class_type, start_string, end_string, trainer_request))
    con.commit()

    index = int(start_input) - 7
    for i in range(int(end_input) - int(start_input)):
        cursor_obj.execute("UPDATE trainers SET available[%s] = FALSE WHERE trainer_id = %s;", (index, trainer_request))
        index += 1
        con.commit()

    j = int(start_input) - 7
    for i in range(int(end_input) - int(start_input)):
        cursor_obj.execute("UPDATE rooms SET times[%s] = FALSE WHERE number = %s;", (j, choice))
        j += 1
        con.commit()

def equipment_maintenance():
    cursor_obj.execute("SELECT * FROM equipment;")
    equipment = cursor_obj.fetchall()

    print("EquipmentID    Type              Quantity   Class")
    for i in equipment:
        print(f"{i[0]:<15}{i[1]:<15}{i[2]:<8}{i[3]:<6}")


# make a payment
def make_payment(first_name, last_name, payment_amt):
    choice = input("Make a payment for $%s: Y/N? " % payment_amt)
    if (choice == 'Y'):
        # add code to update payment information for member
        payment_date = date.today()
        cursor_obj.execute("INSERT INTO payment_history (first_name, last_name, payment_date, payment_amount) "
                           "VALUES (%s, %s, %s, %s);", (first_name, last_name, payment_date, payment_amt))
        return True
    return False

def payment_history():
    cursor_obj.execute("SELECT * FROM payment_history;")
    history = cursor_obj.fetchall()
    print("First name  Last name    Payment date   Payment amount")
    for i in history:
        formatDate = i[2].strftime('%Y-%m-%d')
        print(f"{i[0]:<12}{i[1]:<13}{formatDate:<14} ${i[3]:<8}")

# display admin menu INC
def admin_menu():
    choice = 0
    while(choice != 5):
        print("\n1. Room booking",
              "\n2. Equipment maintenance monitoring",
              "\n3. Show payment history",
              "\n4. Exit")
        choice = input("Select (1/2/3/4): ")
        if choice == '1':
            book_room()

        elif choice == '2':
            equipment_maintenance()

        elif choice == '3':
            payment_history()
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
        print("LOGIN TO BUFFBUDDY",
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
