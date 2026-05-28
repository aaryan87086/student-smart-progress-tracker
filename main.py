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
    for i in range(1,13):
        cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS class_{i}(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        roll_no INTEGER,
        name TEXT,
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

def get_subjects(student_class):
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

def save_result(roll_no, name, student_class, test_name, date, total, percentage, grade, highest, lowest):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f"""
    INSERT INTO class_{student_class} (roll_no, name, test_name, date, total, percentage, grade, highest, lowest)
    VALUES (?,?,?,?,?,?,?,?,?)
    """, (roll_no, name, test_name, date, total, percentage, grade, highest, lowest))
    conn.commit()
    conn.close()

def view_all_students():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    while True:
        try:
            student_class = int(input("Enter class to view (1-12): "))
            if 1 <= student_class <= 12:
                break
            else:
                print("Class should be between (1 - 12) !")
        except ValueError:
            print("Enter number only! ")


    cursor.execute(f"SELECT roll_no, name, total, percentage, grade, highest, lowest FROM class_{student_class}")
    rows = cursor.fetchall()
    conn.close()

    print(f"\n==== Class {student_class} Students ====")
    print("\n{:<10} {:<20} {:<10} {:<12} {:<8} {:<10} {:<10} ".format("Roll_no", "Name", "Total", "Percentage", "Grade", "Highest", "Lowest"))
    print("-" * 65)
    for row in rows:
        print("{:<10} {:<20} {:<10.2f} {:<12.2f} {:<8} {:<10.2f} {:<10.2f}".format(
            row[0], row[1], row[2], row[3], row[4], row[5], row[6]))


def show_student_progress():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    roll_no = int(input("Enter Roll_no: "))

    while True :
        try:
            student_class = int(input("Enter the class (1 - 12) :"))

            if (1 <= student_class <= 12):
                break
            
            else:
                print("class should be between (1-12) : ")

        except ValueError:
            print("Enter Numbers Only! ")

    cursor.execute(f"""
    SELECT name, test_name , percentage
    FROM class_{student_class}
    WHERE roll_no = ?
    """, (roll_no,))

    data = cursor.fetchall()
    conn.close()

    if not data:
        print("Data not Found! ")
        return
    
    test_name = []
    percentage = []

    student_name = data[0][0]

    for row in data:
        test_name.append(row[1])
        percentage.append(row[2])

    plt.plot(test_name, percentage, marker = 'o')

    plt.title(f"{student_name}'s Progress Report")

    plt.xlabel("Tests")

    plt.ylabel("Percentage")

    plt.grid(True)

    plt.show()
    
 
# ========== Main Program ===========
print("==== Student Smart Progress Calculator ====")
initialize_db()

while True:
    print("\n1. Add Students")
    print("2. View All Students")
    print("3. Show Student Progress Graph")
    print("4. Exit")
    choice = input("Enter Choice (1/2/3/4): ").strip()

    if choice == "1":
        roll_no = int(input("Enter Roll No. :"))
        name = input("Enter Student Name: ").strip()
        while True:
            try:
                student_class = int(input("Enter Class (1-12): "))
                if 1 <= student_class <=12:
                    break
                else:
                    print("Class should be between (1 - 12)")

            except ValueError:
                print("Enter Number Only!")

        test_name = input("Enter test name: ").strip()

        date = datetime.now().strftime("%Y-%m-%d")

        subjects = get_subjects(student_class)

        if not subjects:
            continue

        marks_list = get_marks(subjects)
        total, percentage, highest, lowest, grade = calculate_result(marks_list)

        print("\n======= Result =======")
        print("Student Name =", name)
        print("Total =", total)
        print("Percentage =", percentage)
        print("Grade =", grade)
        print("Highest =", highest)
        print("Lowest =", lowest)

        save_result(roll_no, name, student_class, test_name, date, total, percentage, grade, highest, lowest)
        print("Result Saved!")


    elif choice == "2":
        view_all_students()

    elif choice == "3":
        show_student_progress()

    elif choice == "4":
        print("Bye!")
        break