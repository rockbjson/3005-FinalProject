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
        print("\nMANAGE PROFILE",
              "\n1. Update name",
              "\n2. Update fitness goals",
              "\n3. Update health metrics",
              "\n4. Return to member menu")
        choice = input("\nSelect (1/2/3/4/5): ")

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
            print("Returning to main menu.")
            return

        else:
            print("Invalid selection.")

# member registration for classes
def class_register(member_id):
    #display classes
    cursor_obj.execute("SELECT class_id, room_number, schedule.class_type, start_time, end_time, first_name FROM schedule JOIN trainers ON schedule.trainer = trainers.trainer_id ORDER BY class_id ASC;", (member_id))
    classes = cursor_obj.fetchall()

    print("\nClassID   Room      Type        Start Time     End Time      Trainer")
    print("--------------------------------------------------------------------")
    for i in classes:
        start = i[3].strftime('%H:%M:%S')
        end = i[4].strftime('%H:%M:%S')

        print(f"{i[0]:<10}{i[1]:<10}{i[2]:<12}{start:<15}{end:<14}{i[5]:<20}")

    class_request = input("Enter class ID to register: ")

    cursor_obj.execute("SELECT start_time FROM schedule WHERE class_id = %s", (class_request))
    start_input = cursor_obj.fetchall()
    cursor_obj.execute("SELECT end_time FROM schedule WHERE class_id = %s", (class_request))
    end_input = cursor_obj.fetchall()

    if not start_input:
        print("Class does not exist.")
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
        print("Already registerd in this class.")

    elif conflict == False and registered == False:
        cursor_obj.execute("UPDATE schedule SET members = array_append(members, %s) WHERE class_id = %s;", (member_id, class_request))
        con.commit()
        print("Class added to schedule.")

    else:
        print("Requested class conflicts with your schedule.")

# drop a class
def drop_class(member_id):
    # display classes
    cursor_obj.execute(
        "SELECT class_id, room_number, schedule.class_type, start_time, end_time, first_name FROM schedule JOIN trainers ON schedule.trainer = trainers.trainer_id ORDER BY class_id ASC;",
        (member_id))
    classes = cursor_obj.fetchall()

    print("\nClassID   Room      Type        Start Time     End Time      Trainer")
    print("--------------------------------------------------------------------")
    for i in classes:
        start = i[3].strftime('%H:%M:%S')
        end = i[4].strftime('%H:%M:%S')

        print(f"{i[0]:<10}{i[1]:<10}{i[2]:<12}{start:<15}{end:<14}{i[5]:<20}")

    class_request = input("Enter class ID to drop: ")

    cursor_obj.execute("SELECT start_time FROM schedule WHERE class_id = %s", (class_request))
    start_input = cursor_obj.fetchall()

    if not start_input:
        print("Class does not exist.")
        return

    # !!! remove class here !!!
    cursor_obj.execute("UPDATE schedule SET members = array_remove(members, %s) WHERE class_id = %s;",
                       (member_id, class_request))
    con.commit()
    print("Class dropped from schedule.")

# cancel a private session
def cancel_session(member_id):
    # display all sessions
    cursor_obj.execute("SELECT session_id, room_number, priv_sessions.class_type, start_time, end_time, first_name "
                       "FROM "
                       "priv_sessions JOIN "
                       "trainers ON priv_sessions.trainer = trainers.trainer_id WHERE member = %s ORDER BY "
                       "start_time ASC;", (member_id))

    sessions = cursor_obj.fetchall()
    print("\nPERSONAL SESSIONS")
    print("Session ID   Room    Type        Start Time     End Time      Trainer")
    print("---------------------------------------------------------------------")
    for i in sessions:
        start = i[3].strftime('%H:%M:%S')
        end = i[4].strftime('%H:%M:%S')

        print(f"{i[0]:<13}{i[1]:<8}{i[2]:<12}{start:<15}{end:<14}{i[5]:<15}")

    session_request = input("Enter session ID to drop: ")

    cursor_obj.execute("SELECT start_time FROM schedule WHERE class_id = %s", (session_request))
    start_input = cursor_obj.fetchall()

    if not start_input:
        print("Session does not exist.")
        return

    cursor_obj.execute("SELECT start_time FROM priv_sessions WHERE session_id = %s" % (session_request))
    start_time = cursor_obj.fetchall()[0][0]
    start_hour = start_time.hour

    cursor_obj.execute("SELECT end_time FROM priv_sessions WHERE session_id = %s" % (session_request))
    end_time = cursor_obj.fetchall()[0][0]
    end_hour = end_time.hour

    cursor_obj.execute("SELECT room_number FROM priv_sessions WHERE session_id = %s" % session_request)
    room_number = cursor_obj.fetchall()[0][0]

    cursor_obj.execute(("SELECT trainer FROM priv_sessions WHERE session_id = %s") % session_request)
    trainer_id = cursor_obj.fetchall()[0][0]

    j = int(start_hour) - 7
    for i in range(int(end_hour) - int(start_hour)):
        cursor_obj.execute("UPDATE rooms SET times[%s] = TRUE WHERE number = %s;", (j, room_number))
        j += 1
        con.commit()

    k = int(start_hour) - 7
    for i in range(int(end_hour) - int(start_hour)):
        cursor_obj.execute("UPDATE trainers SET available[%s] = TRUE WHERE trainer_id = %s;", (k,
                                                                                                trainer_id))
        k += 1
        con.commit()

    # !!! remove session here !!!
    cursor_obj.execute("DELETE FROM priv_sessions WHERE session_id = %s;",
                       (session_request))
    con.commit()
    print("Session canceled.")


# member registration for private session
def session_register(member_id):
    first_name = input("\nEnter requested trainer's first name: ")
    last_name = input("Enter requested trainer's last name: ")

    cursor_obj.execute("SELECT trainer_id FROM trainers WHERE first_name = %s AND last_name = %s", (first_name, last_name))
    trainer_request = cursor_obj.fetchall()

    if not trainer_request:
        print("Trainer does not exist.")
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

        cursor_obj.execute("SELECT class_type FROM trainers WHERE trainer_id = %s", (trainer_request))
        class_type = cursor_obj.fetchall()[0][0]

        start_time = (start_time + ":00:00") if int(start_time) > 9 else ("0" + start_time + ":00:00")
        end_time = (end_time + ":00:00") if int(end_time) > 9 else ("0" + end_time + ":00:00")

        trainer_request = trainer_request[0]
        member_id = member_id[0]

        cursor_obj.execute("INSERT INTO priv_sessions (room_number, class_type, start_time, end_time, trainer, member) VALUES (%s, '%s', '%s', '%s', %s, %s);" % (room_number, class_type, start_time,end_time,
                                                                 trainer_request, member_id))
        con.commit()
        print("Personal session added to schedule.")

    elif open_trainer == False and open_member == True:
        print("%s %s is not free at these times." % (first_name, last_name))

    elif open_trainer == True and open_member == False:
        print("You have another class or session at this time.")

    else:
        print("You and %s %s are both not free at this time." % (first_name, last_name))

# display member dashboard
def display_member_dashboard(member_id):
    cursor_obj.execute("SELECT * FROM members WHERE member_id = %s", (member_id))
    member = cursor_obj.fetchall()
    print("\nFirst name      Last name       Weight goal      Running goal      Weight      Height      Payment due ")
    print("--------------------------------------------------------------------------------------------------------")
    for i in member:
        first_name = i[1] if i[1] is not None else "None"
        last_name = i[2] if i[2] is not None else "None"
        weight_goal = i[3] if i[3] is not None else "None"
        running_goal = i[4] if i[4] is not None else "None"
        weight = i[5] if i[5] is not None else "None"
        height = i[6] if i[6] is not None else "None"
        date = i[7].strftime('%Y-%m-%d') if i[7] is not None else "None"
        print(f"{first_name:<16}{last_name:<16}{weight_goal:<0} lbs {running_goal:>12} km {weight:>14} lbs"
              f" {height:>7} cm {date:>14}")

# display member schedule
def display_member_schedule(member_id):
    cursor_obj.execute("SELECT class_id, room_number, schedule.class_type, start_time, end_time, first_name FROM schedule JOIN trainers ON schedule.trainer = trainers.trainer_id WHERE %s = ANY(members) ORDER BY start_time ASC;", (member_id))
    member_schedule = cursor_obj.fetchall()

    print("\nREGULAR CLASSES")
    print("Room    Type        Start Time     End Time      Trainer")
    print("--------------------------------------------------------")
    for i in member_schedule:
        start = i[3].strftime('%H:%M:%S')
        end = i[4].strftime('%H:%M:%S')

        print(f"{i[1]:<8}{i[2]:<12}{start:<15}{end:<15}{i[5]:<14}")

    cursor_obj.execute("SELECT room_number, priv_sessions.class_type, start_time, end_time, first_name FROM "
                       "priv_sessions JOIN "
                       "trainers ON priv_sessions.trainer = trainers.trainer_id WHERE member = %s ORDER BY "
                       "start_time ASC;", (member_id))

    sessions = cursor_obj.fetchall()
    print("\nPERSONAL SESSIONS")
    print("Room    Type        Start Time     End Time      Trainer")
    print("--------------------------------------------------------")
    for i in sessions:
        start = i[2].strftime('%H:%M:%S')
        end = i[3].strftime('%H:%M:%S')

        print(f"{i[0]:<8}{i[1]:<12}{start:<15}{end:<15}{i[4]:<14}")

def renew_membership(member_id):
    cursor_obj.execute("SELECT payment_date FROM members WHERE member_id = %s", (member_id))
    payment_date = cursor_obj.fetchall()[0][0]
    formatDate = payment_date.strftime('%Y-%m-%d')
    print("\nYour current payment due date is: %s"% (formatDate))
    cursor_obj.execute("SELECT first_name FROM members WHERE member_id = %s", (member_id))
    first_name = cursor_obj.fetchall()[0][0]
    cursor_obj.execute("SELECT last_name FROM members WHERE member_id = %s", (member_id))
    last_name = cursor_obj.fetchall()[0][0]
    if (make_payment(first_name, last_name, 800)):
        new_date = payment_date + timedelta(days=365)
        cursor_obj.execute("UPDATE members SET payment_date = %s WHERE member_id = %s", (new_date, member_id))
        con.commit()

def cancel_membership(member_id):
    print("\nAre you sure? Your membership is non-refundable. You will lose access to all classes and sessions "
          "immediately.")
    choice = input("Cancel membership? Y/N: ")
    if (choice == 'Y'):
        member = member_id[0]
        cursor_obj.execute("DELETE FROM members WHERE member_id = %s" % (member))
        con.commit()
        cursor_obj.execute("DELETE FROM priv_sessions WHERE member = %s;" % member)
        con.commit()
        cursor_obj.execute("UPDATE schedule SET members = array_remove(members, %s) WHERE %s = ANY("
                           "members);" % (member, member))
        start_menu()
    elif (choice == 'N'):
        print("Membership cancellation failed.")
        return
    else:
        print("Invalid selection.")

def manage_classes(member_id):
    choice = 0
    while(choice != 3):
        print("\n1. Register for a new class"
              "\n2. Drop a class"
              "\n3. Exit")
        choice = input("\nSelect 1/2/3: ")
        if (choice == '1'):
            class_register(member_id)
        elif (choice == '2'):
            drop_class(member_id)
        elif (choice == '3'):
            return
        else:
            print("Invalid selection.")

def manage_sessions(member_id):
    choice = 0
    while (choice != 3):
        print("\n1. Register for a new session"
              "\n2. Cancel a session"
              "\n3. Exit")
        choice = input("\nSelect 1/2/3: ")
        if (choice == '1'):
            session_register(member_id)
        elif (choice == '2'):
            cancel_session(member_id)
        elif (choice == '3'):
            return
        else:
            print("Invalid selection.")

# mange membership menu
def manage_membership(member_id):
    choice = 0
    while (choice != 3):
        print("\n1. Renew membership"
              "\n2. Cancel membership"
              "\n3. Exit")
        choice = input("\nSelect 1/2/3: ")
        if (choice == '1'):
            renew_membership(member_id)
        elif (choice == '2'):
            cancel_membership(member_id)
        elif (choice == '3'):
            return
        else:
            print("Invalid selection.")
# display member menu
def member_menu(member_id):
    choice = 0
    while(choice != 5):
        print("\nMEMBER MENU"
            "\n1. Manage profile",
            "\n2. Add/drop a class",
            "\n3. Book/cancel a personal session",
            "\n4. Display dashboard",
            "\n5. Display personal schedule",
            "\n6. Manage membership"
            "\n7. Log out and return to main menu")
        choice = input("\nSelect (1/2/3/4/5): ")
        if choice == '1':
            manage_profile(member_id)

        elif choice == '2':
            manage_classes(member_id)

        elif choice == '3':
            manage_sessions(member_id)
            
        elif choice == '4':
            display_member_dashboard(member_id)

        elif choice == '5':
            display_member_schedule(member_id)

        elif choice == '6':
            manage_membership(member_id)

        # returns to main menu
        elif choice == '7':
            print("Returning to main menu.")
            return

        else:
            print("Invalid selection.")

# ##############################################
        
# TRAINER FUNCTIONS

# trainer sets times for when they're available
def set_availability(trainer_id):
    start_time = input("\nEnter available start time (24 hour clock): ")
    end_time = input("Enter available end time (24 hour clock): ")

    if int(start_time) < 8 or int(end_time) < 8:
        print("Times are outside of BuffBuddy hours or incorrect format.")
        return

    index = int(start_time) - 7
    for i in range(int(end_time) - int(start_time)):
        cursor_obj.execute("UPDATE trainers SET available[%s] = TRUE WHERE trainer_id = %s;", (index, trainer_id))
        index += 1
        con.commit()

# view member profiles
def view_members():
    first_name = input("\nEnter member first name to view: ")
    last_name = input("Enter member last name to view: ")

    cursor_obj.execute("SELECT member_id FROM members WHERE first_name = %s AND last_name = %s;", (first_name,
                                                                                                     last_name))
    member = cursor_obj.fetchall()

    if len(member) == 0:
        print("Invalid first or last name.")
        return

    member_id = member[0]

    display_member_dashboard(member_id)

# display trainer schedule
def display_trainer_schedule(trainer_id):
    cursor_obj.execute("SELECT class_id, room_number, class_type, start_time, end_time, members FROM schedule WHERE "
                       "trainer = %s ORDER BY start_time ASC;", (trainer_id))
    trainer_schedule = cursor_obj.fetchall()
    print("\nREGULAR CLASSES")
    print("Room   Type    Start Time     End Time    Members")
    print("----------------------------------------------------------")
    for i in trainer_schedule:
        start = i[3].strftime('%H:%M:%S')
        end = i[4].strftime('%H:%M:%S')
        members = i[5]

        print(f"{i[1]:<7}{i[2]:<8}{start:<15}{end:<11}",  members)

    cursor_obj.execute("SELECT room_number, priv_sessions.class_type, start_time, end_time, member FROM "
                       "priv_sessions JOIN "
                       "trainers ON priv_sessions.trainer = trainers.trainer_id WHERE trainer = %s ORDER BY "
                       "start_time ASC;", (trainer_id))
    sessions = cursor_obj.fetchall()
    print("\nPERSONAL SESSIONS")
    print("Room    Type        Start Time     End Time      Member")
    print("--------------------------------------------------------")
    for i in sessions:
        start = i[2].strftime('%H:%M:%S')
        end = i[3].strftime('%H:%M:%S')

        print(f"{i[0]:<8}{i[1]:<12}{start:<15}{end:<14}{i[4]:<14}")

# display trainer menu 
def trainer_menu(trainer_id):
    choice = 0
    while(choice != 4):
        print("\nTRAINER MENU"
            "\n1. Set availability",
            "\n2. View member profiles",
            "\n3. Display trainer schedule"
            "\n4. Log out and return to main menu")
        choice = input("\nSelect (1/2/3/4): ")
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

        else:
            print("Invalid selection.")

# ##############################################

# ADMIN FUNCTIONS

# booking a room
def book_room():
    print("\nTrue - available, False - not available\n")
    cursor_obj.execute("SELECT * from rooms")
    rooms = cursor_obj.fetchall()
    print("Room                         Availability")
    print("         08:00 09:00 10:00 11:00 12:00 13:00 14:00 15:00 16:00")
    print("--------------------------------------------------------------")
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
        print("No rooms available for this times.")
        return
    
    first_name = input("Enter requested trainer's first name: ")
    last_name = input("Enter requested trainer's last name: ")

    cursor_obj.execute("SELECT trainer_id FROM trainers WHERE first_name = %s AND last_name = %s", (first_name, last_name))
    trainer_request = cursor_obj.fetchall()

    if not trainer_request:
        print("Trainer does not exist.")
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
        print("Room %s is not available at this time.", choice)
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
    cursor_obj.execute("SELECT * FROM equipment ORDER BY equipment_id ASC;")
    equipment = cursor_obj.fetchall()

    print("\nEquipmentID    Type            Quantity   Class")
    print("-----------------------------------------------")
    for i in equipment:
        print(f"{i[0]:<15}{i[1]:<16}{i[2]:<11}{i[3]:<6}")

    eq_id = input("\nEnter EquipmentID to change quantity: ")
    cursor_obj.execute("SELECT quantity FROM equipment where equipment_id = %s;", (eq_id))

    if len(cursor_obj.fetchall()) == 0:
        print("Invalid EquipmentID.")
        return

    else:
        quantity = input("Enter new quantity: ")
        if quantity < 0:
            print("Invalid quantity.")
            return
        cursor_obj.execute("UPDATE equipment SET quantity = %s WHERE equipment_id = %s;", (quantity, eq_id))
        con.commit()
        print("Equipment quantity successfully changed.")

# make a payment
def make_payment(first_name, last_name, payment_amt):
    choice = input("\nMake a payment for $%s: Y/N? " % payment_amt)
    if (choice == 'Y'):
        # add code to update payment information for member
        payment_date = date.today()
        cursor_obj.execute("INSERT INTO payment_history (first_name, last_name, payment_date, payment_amount) "
                           "VALUES (%s, %s, %s, %s);", (first_name, last_name, payment_date, payment_amt))
        con.commit()
        return True
    print("Payment failed.")
    return False

def payment_history():
    cursor_obj.execute("SELECT * FROM payment_history;")
    history = cursor_obj.fetchall()
    print("\nFirst name  Last name    Payment date   Payment amount")
    print("------------------------------------------------------")
    for i in history:
        formatDate = i[2].strftime('%Y-%m-%d')
        print(f"{i[0]:<12}{i[1]:<13}{formatDate:<14} ${i[3]:<8}")

# display admin menu INC
def admin_menu():
    choice = 0
    while(choice != 5):
        print("\nADMINISTRATIVE STAFF MENU"
              "\n1. Room booking",
              "\n2. Equipment maintenance monitoring",
              "\n3. Show payment history",
              "\n4. Log out and return to main menu")
        choice = input("\nSelect (1/2/3/4): ")
        if choice == '1':
            book_room()

        elif choice == '2':
            equipment_maintenance()

        elif choice == '3':
            payment_history()
            
        # returns to main menu
        elif choice == '4':
            print("Returning to main menu.")
            return

        else:
            print("Invalid selection.")

# ##############################################

# new member registration
def new_user():
    first_name = input("\nEnter first name: ")
    last_name = input("Enter last name: ")
    current_date = date.today()
    if (make_payment(first_name, last_name, 800)) :
        new_date = current_date + timedelta(days=365)
        cursor_obj.execute("INSERT INTO members (first_name, last_name, payment_date) VALUES (%s, %s, %s);", (first_name, last_name, new_date))
        con.commit()
        print("Welcome! You are now a member at BuffBuddy.")
    else:
        print("You have to make a payment to register as a member.")

# MAIN MENU 

# repeatedly displays menu till user chooses to exit. displays database operations.
def start_menu():
    choice = 0
    while choice != 5:
        print("\nLOGIN TO BUFFBUDDY",
            "\n1. Member",
            "\n2. Trainer",
            "\n3. Admin Staff",
            "\n4. New Member",
            "\n5. Exit")

        choice = input("\nSelect (1/2/3/4/5): ")

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
            else:
                print("Login failed: invalid first or last name.")

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
            else:
                print("Login failed: invalid first or last name.")

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
            else:
                print("Login failed: invalid first or last name.")

        elif (choice == '4'):
            new_user()

        elif (choice == '5'):
            exit()

        else:
            print("Invalid selection.")

# program start
start_menu()
