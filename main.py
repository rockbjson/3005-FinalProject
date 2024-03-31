import psycopg2
from datetime import date, timedelta

#establishing connection with database server
con = psycopg2.connect(
    database="finalproject",
    user="postgres",
    password="37293",
    host="localhost",
    port= '5432'
    )

cursor_obj = con.cursor()

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

        # updating member health metrics ???
        elif choice == '3':
            # update table for member health metrics ???
            current_weight = input("Enter current weight: ")
            # sql statement
            print("Health metrics successfully updated.")

        # return to member menu
        elif choice == '4':
            print("Returning to menu.")
            return

# member registration for classes INC
def class_register():
    print("something")

# display member dashboard
def display_member_dashboard(member_id):
    cursor_obj.execute("SELECT * FROM members WHERE member_id = %s", (member_id))
    member = cursor_obj.fetchall()
    columns = ['Member ID', 'First name', 'Last name', 'Weight goal', 'Time goal', 'Payment due date']
    for i in range(len(member)):
        for j in range(len(columns)):
            print('%s: %s' % (columns[j], member[i][j]))

# display member schedule
def display_member_schedule():
    print("something")

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
            class_register()

        elif choice == '3':
            display_member_dashboard(member_id)

        elif choice == '4':
            display_member_schedule()

        # returns to main menu
        elif choice == '5':
            print("Returning to main menu.")
            return

# display trainer menu INC
def trainer_menu():
    choice = 0
    while(choice != 4):
        print("\n1. Set availability",
            "\n2. View member profiles",
            "\n3. Display trainer schedule"
            "\n4. Exit")
        choice = input("Select (1/2/3/4): ")

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

# make a payment
def payment(first_name, last_name, payment_amt):
    choice = input("Make a payment for $%s: Y/N", payment_amt)
    if (choice == 'Y'):
        # add code to update payment information for member
        return True
    return False

# new member registration
def new_user():
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    current_date = date.today()
    if (payment(first_name, last_name, 800)) :
        new_date = current_date + timedelta(days=365)
        cursor_obj.execute("INSERT INTO members (first_name, last_name, payment_date) VALUES (%s, %s, %s);", (first_name, last_name, new_date))
        print("Welcome! You are now a member at BuffBuddy.")
    else:
        print("You have to make a payment to register a member.")

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
                                   (first_name,
                                                                                                        last_name))
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
                trainer_menu()

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
                admin_menu()

        elif (choice == '4'):
            new_user()

        elif (choice == '5'):
            exit()


start_menu()
