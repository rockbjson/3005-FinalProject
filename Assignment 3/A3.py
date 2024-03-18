import psycopg2 

# connecting to server
connection = psycopg2.connect(user="postgres",
                                password="postgres",
                                host="127.0.0.1",
                                port="5432",
                                database="assignment3")

cursor = connection.cursor()


# getAllStudents
def getAllStudents(connection, cursor):
    try:
        cursor.execute("SELECT  * from students")
        getAllStudents = cursor.fetchall()

        print("getAllStudents: ")

        print("ID   First Name   Last Name     Email                        Enrollment Date")
        for i in getAllStudents:
            formatDate = i[4].strftime('%Y-%m-%d')

            print(f"{i[0]:<6}{i[1]:<13}{i[2]:<13}{i[3]:<30}{formatDate}")

    except:
        print("Error getting all students ")


# addStudent
def addStudent(connection, cursor):
    try:
        first_name = input("Enter the first name: ")
        last_name = input("Enter the last name: ")
        email = input("Enter the email: ")
        enrollment_date = input("Enter the enrollment date [yyyy-mm-dd]: ")
        cursor.execute("""INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES
                    (%s, %s, %s, %s);""",(first_name, last_name, email, enrollment_date))

        connection.commit()
    
    except: 
        print("Error adding student ")


# updateStudentEmail
def updateStudentEmail(connection, cursor):
    try:
        email = input("Enter the new email: ")
        student_id = input("Enter the student id: ")
        cursor.execute("""UPDATE students SET email = %s WHERE student_id = %s;""", (email, student_id))

        connection.commit()

    except: 
        print("Error updating student email ")

# deleteStudent
def deleteStudent(connection, cursor):
    try:
        student_id = input("Enter the student id: ")
        cursor.execute("""DELETE from students where student_id = %s;""", (student_id))
        connection.commit()

    except:
        print("Error deleting student ")


while True:

    print("\nMenu:")
    print("1. getAllStudents")
    print("2. addStudent")
    print("3. updateStudentEmail")
    print("4. deleteStudent")
    print("5. exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        getAllStudents(connection,cursor)
    elif choice == '2':
        addStudent(connection,cursor)
    elif choice == '3':
        updateStudentEmail(connection,cursor)
    elif choice == '4':
        deleteStudent(connection,cursor)
    elif choice == '5x':
        print("Exiting program.")
        break
    else:
        print("Invalid choice. Please enter a valid option.")

cursor.close()
connection.close()
print("PostgreSQL connection is closed")

