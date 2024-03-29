import psycopg2
from datetime import date, timedelta

#estbalishing connection with database server
con = psycopg2.connect(
    database="finalproject",
    user="postgres",
    password="37293",
    host="localhost",
    port= '5432'
    )

cursor_obj = con.cursor()

def member_menu():
    choice = 0
    while(choice != 4):
        print("\n1. Manage profile",
            "\n2. Register for classes",
            "\n3. Display dashboard",
            "\n4. Display personal schedule",
            "\n4. Exit")
        choice = input("Select (1/2/3/4): ")

def trainer_menu():
    choice = 0
    while(choice != 4):
        print("\n1. Set availability",
            "\n2. View member profiles",
            "\n3. Display trainer schedule"
            "\n4. Exit")
        choice = input("Select (1/2/3/4): ")

def admin_menu():
    choice = 0
    while(choice != 5):
        print("\n1. Room booking",
              "\n2. Equipment maintenance monitoring",
              "\n3. Update class schedule",
              "\n4. Process payments",
              "\n5. Exit")
        choice = input("Select (1/2/3/4/5): ")

def payment(first_name, last_name, payment_amt):
    choice = input("Make a payment for $%s: Y/N", payment_amt)
    if (choice == 'Y'):
        return True
    return False

def new_user():
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    current_date = date.today()
    if (payment(first_name, last_name, 800)) :
        new_date = current_date + timedelta(days=365)
        cursor_obj.execute("INSERT INTO members (first_name, last_name, payment_date) VALUES (%s, %s, %s);", (first_name, last_name, new_date))
        print("Welcome! You are now a member at BuffBuddy.")
    else:
        print("You have to make a payment to register a memmber.")

#repeatedly displays menu till user chooses to exit. displays database operations.
def start_menu():
    choice = 0

    print("LOGIN",
        "\n1. Member",
        "\n2. Trainer",
        "\n3. Admin Staff",
        "\n4. New Member",
        "\n4. Exit")

    choice = input("Select (1/2/3/4): ")

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
            member_menu()

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


start_menu()
