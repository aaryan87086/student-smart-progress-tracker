#=====================================================
#Student Smart Progress Calculator
#Author = Aaryan
#Description = Calculate Total Marks , Percentage and Grade
#=====================================================

import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "students.db")

def initialize_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        class INTEGER,
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

def save_result(name, student_class, total, percentage, grade, highest, lowest):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO students (name, class, total, percentage, grade, highest, lowest)
    VALUES (?,?,?,?,?,?,?)
    """, (name, student_class, total, percentage, grade, highest, lowest))
    conn.commit()
    conn.close()

def view_all_students():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name, class, percentage, grade FROM students")
    rows = cursor.fetchall()
    conn.close()
    print("\n{:<20} {:<8} {:<12} {}".format("Name", "Class", "Percentage", "Grade"))
    print("-" * 45)
    for row in rows:
        print("{:<20} {:<8} {:<12.2f} {}".format(*row))


# ========== Main Program ===========
print("==== Student Smart Progress Calculator ====")
initialize_db()

while True:
    print("\n1. Add Students")
    print("2. View All Students")
    print("3. Exit")
    choice = input("Enter Choice (1/2/3): ").strip()

    if choice == "1":
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

        save_result(name, student_class, total, percentage, grade, highest, lowest)
        print("Result Saved!")


    elif choice == "2":
        view_all_students()

    elif choice == "3":
        print("Bye!")
        break