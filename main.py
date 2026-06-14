#=====================================================
#Student Smart Progress Calculator
#Author = Aaryan
#Description = Calculate Total Marks , Percentage and Grade
#=====================================================

import sqlite3
import os
import matplotlib.pyplot as plt
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "students.db")

def initialize_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()


    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS students(
        roll_no INTEGER,
        student_class INTEGER,
        name TEXT,
        stream TEXT,
        PRIMARY KEY (roll_no, student_class)
    )
    """)

    for i in range(1,13):
        cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS class_{i}(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        roll_no INTEGER,
        test_name TEXT,
        date TEXT,
        total REAL,
        percentage REAL,
        grade TEXT,
        highest REAL,
        lowest REAL
    )
    """)
    conn.commit()
    conn.close()

def register_student():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    while True:
        try:
            roll_no = int(input("Enter Roll NO: "))
            break

        except ValueError:
            print("Enter Number Only!")


    while True:
        try:
            student_class = int(input("Enter Class (1-12): "))
            if 1 <= student_class <= 12:
                break
            else:
                print("Class should be between (1-12)")
        except ValueError:
            print("Enter Number Only!")


    cursor.execute("SELECT * FROM students WHERE roll_no=? AND student_class=?", (roll_no, student_class))
    if cursor.fetchone():
        print("Student already registered!")
        conn.close()
        return

    name = input("Enter Student Name: ").strip()

    stream = None
    if student_class == 11 or student_class == 12:
        while True:
            stream = input("Enter Stream (Science/Commerce): ").strip().lower()
            if stream in ["science", "commerce"]:
                break
            else:
                print("Invalid Stream!")

        if stream == "science":
            while True:
                sub_stream = input("Medical or Non-Medical?: ").strip().lower()
                if sub_stream in ["medical", "non-medical"]:
                    stream = sub_stream  # medical ya non-medical save karo
                    break
                else:
                    print("Invalid Input!")


    cursor.execute("""
    INSERT INTO students (roll_no, student_class, name, stream)
    VALUES (?,?,?,?)
    """, (roll_no, student_class, name, stream))
    conn.commit()
    conn.close()
    print(f"Student {name} Registered Successfully!")


def get_subjects(roll_no, student_class):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT stream FROM students WHERE roll_no=? AND student_class=?", (roll_no, student_class))
    result = cursor.fetchone()
    conn.close()

    if not result:
        print("Student not found! Pehle register karo.")
        return []
    
    stream = result[0]

    if (1 <= student_class <= 10):
        return ["English", "Hindi", "Maths", "Science", "Computer", "SST"]
    elif (student_class == 11 or student_class == 12):
        stream = input("Enter Stream (Science/Commerce): ").strip().lower()
        if stream == "science":
            sub_stream = input("Medical or Non-Medical?: ").strip().lower()
            if sub_stream == "medical":
                return ["English", "Hindi", "Biology", "Physics", "Chemistry", "Physical Education", "Music"]
            elif sub_stream == "non-medical":
                return ["English", "Music", "Maths", "Physics", "Chemistry", "Physical Education"]
            else:
                print("Invalid input.")
                return []
        elif stream == "commerce":
            return ["Accounts", "Business Studies", "Maths", "English", "Economics"]
        else:
            print("Invalid Stream")
            return []
    else:
        print("Invalid Class")
        return []
    

def get_marks(subjects):
    marks_list = []
    for subject in subjects:
        while True:
            try:
                score = float(input(f"Enter marks for {subject}: "))
                if 0 <= score <= 100:
                    marks_list.append(score)
                    break
                else:
                    print("Marks should be between 0-100")
            except ValueError:
                print("Invalid Input! Enter Number Only.")
    return marks_list


def calculate_result(marks_list):
    total = sum(marks_list)
    percentage = (total / (len(marks_list)*100)) * 100
    highest = max(marks_list)
    lowest = min(marks_list)
    if percentage >= 90:
        grade = "A"
    elif percentage >= 75:
        grade = "B"
    elif percentage >= 60:
        grade = "C"
    elif percentage >= 40:
        grade = "D"
    else:
        grade = "Fail"
    return total, percentage, highest, lowest, grade

def save_result(roll_no, student_class, test_name, date, total, percentage, grade, highest, lowest):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f"""
    INSERT INTO class_{student_class} (roll_no, test_name, date, total, percentage, grade, highest, lowest)
    VALUES (?,?,?,?,?,?,?,?)
    """, (roll_no, test_name, date, total, percentage, grade, highest, lowest))
    conn.commit()
    conn.close()

def view_class_students():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    while True:
        try:
            student_class = int(input("Enter class to view (1-12): "))
            if 1 <= student_class <= 12:
                break
            else:
                print("Class should be between (1-12)!")
        except ValueError:
            print("Enter number only!")

    
    cursor.execute("SELECT roll_no, name FROM students WHERE student_class=? ORDER BY roll_no", (student_class,))
    students = cursor.fetchall()

    if not students:
        print("No students found in this class!")
        conn.close()
        return

    
    cursor.execute(f"""
    SELECT DISTINCT test_name FROM class_{student_class} ORDER BY id
    """)
    tests = [row[0] for row in cursor.fetchall()]

    if not tests:
        print("No marks added yet!")
        conn.close()
        return

    print(f"\n==== Class {student_class} Students ====\n")
    header = "{:<8} {:<20}".format("Roll No", "Name")
    for test in tests:
        header += " {:<15}".format(test)
    print(header)
    print("-" * (28 + len(tests) * 15))


    for roll_no, name in students:
        row = "{:<8} {:<20}".format(roll_no, name)

        for test in tests:
            cursor.execute(f"""
            SELECT percentage FROM class_{student_class}
            WHERE roll_no=? AND test_name=?
            """, (roll_no, test))
            result = cursor.fetchone()
            if result:
                row += " {:<15}".format(f"{result[0]:.2f}%")
            else:
                row += " {:<15}".format("N/A")

        print(row)

    conn.close()

def search_student():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    while True:
        try:
            roll_no = int(input("Enter Roll No: "))
            break
        except ValueError:
            print("Enter Number Only!")

    while True:
        try:
            student_class = int(input("Enter Class (1-12): "))
            if 1 <= student_class <= 12:
                break
            else:
                print("Class should be between (1-12)!")
        except ValueError:
            print("Enter Number Only!")


    cursor.execute("SELECT roll_no, name, stream FROM students WHERE roll_no=? AND student_class=?", (roll_no, student_class))
    student = cursor.fetchone()

    if not student:
        print("Student not found!")
        conn.close()
        return

    print(f"\n==== Student Details ====")
    print(f"Roll No : {student[0]}")
    print(f"Name    : {student[1]}")
    print(f"Class   : {student_class}")
    print(f"Stream  : {student[2] if student[2] else 'N/A'}")

    cursor.execute(f"""
    SELECT test_name, date, total, percentage, grade, highest, lowest
    FROM class_{student_class}
    WHERE roll_no=?
    ORDER BY id
    """, (roll_no,))

    results = cursor.fetchall()
    conn.close()

    if not results:
        print("\nNo marks added yet!")
        return

    print(f"\n==== Test Results ====")
    print("{:<15} {:<12} {:<10} {:<12} {:<8} {:<10} {:<10}".format(
        "Test", "Date", "Total", "Percentage", "Grade", "Highest", "Lowest"))
    print("-" * 75)
    for r in results:
        print("{:<15} {:<12} {:<10.2f} {:<12.2f} {:<8} {:<10.2f} {:<10.2f}".format(
            r[0], r[1], r[2], r[3], r[4], r[5], r[6]))


def show_student_progress():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    while True :
        try:
            roll_no = int(input("Enter Roll_no: "))
            break

        except ValueError:
            print("Enter Numbers Only! ")

            student_class = int(input("Enter the class (1 - 12) :"))

            if (1 <= student_class <= 12):
                break
            
            else:
                print("class should be between (1-12) : ")

        except ValueError:
            print("Enter Numbers Only! ")

    cursor.execute(f"""
    SELECT s.name, c.test_name, c.percentage
    FROM students s
    JOIN class_{student_class} c ON s.roll_no = c.roll_no
    WHERE s.roll_no = ? AND s.student_class = ?
    ORDER BY c.id
    """, (roll_no, student_class))

    data = cursor.fetchall()
    conn.close()

    if not data:
        print("Data not found!")
        return
    

    student_name = data[0][0]
    test_name = [row[1] for row in data]
    percentage = [row[2] for row in data]


    plt.figure(figsize=(10, 5))
    plt.plot(test_name, percentage, marker = 'o', color='blue' , linewidth=2, markersize=8)

    plt.title(f"{student_name}'s Progress Report")
    plt.xlabel("Tests")
    plt.ylabel("Percentage")
    plt.ylim(0, 100)
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    
 
# ========== Main Program ===========
print("==== Student Smart Progress Calculator ====")
initialize_db()

while True:
    print("\n1. Register Student")
    print("2. Add Marks")
    print("3. View Class Students")
    print("4. Show Student Progress")
    print("5. Search Student")
    print("6. Exit")

    choice = input("Enter Choice (1/2/3/4/5): ").strip()

    if choice == "1":
        register_student()

    elif choice == "2":
        while True:
            try:
                roll_no = int(input("Enter Roll No: "))
                break
            except ValueError:
                print("Enter Number Only!")

        while True:
            try:
                student_class = int(input("Enter Class (1-12): "))
                if 1 <= student_class <= 12:
                    break
                else:
                    print("Class should be between (1-12)")
            except ValueError:
                print("Enter Number Only!")

        test_name = input("Enter Test Name: ").strip()
        date = datetime.now().strftime("%Y-%m-%d")

        subjects = get_subjects(roll_no, student_class)
        if not subjects:
            continue

        marks_list = get_marks(subjects)
        total, percentage, highest, lowest, grade = calculate_result(marks_list)

        print("\n======= Result =======")
        print("Total =", total)
        print("Percentage =", percentage)
        print("Grade =", grade)
        print("Highest =", highest)
        print("Lowest =", lowest)

        save_result(roll_no, student_class, test_name, date, total, percentage, grade, highest, lowest)
        print("Result Saved!")

    elif choice == "3":
        view_class_students()

    elif choice == "4":
        show_student_progress()

    elif choice == "5":
        search_student()

    elif choice == "6":
        print("Bye!")
    break