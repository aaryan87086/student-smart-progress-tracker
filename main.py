#=====================================================
#Student Smart Progress Calculator
#Author = Aaryan
#Description = Calculate Total Marks , Percentage and Grade
#=====================================================

import sqlite3
import cv2
import face_recognition
import os
import pickle
from datetime import datetime


# ======= Functions Define =======
def get_subjects(student_class):
# Assign Subjects According to class 
    if (1 <= student_class <= 10):
    # subjects for classes 1 - 10
        return ["English" , "Hindi" , "Maths" , "Science" , "Computer" , "SST"]

    elif (student_class==11 or student_class==12):

    # Ask stream for senior classes
        stream = input("Enter the Stream (Science/Commerce) :").strip().lower()
        if (stream == "science"):

        # Ask for medical or Non Medical
            sub_stream = input("Medical or Non-Medical? :").strip().lower()
            if (sub_stream == "medical"):
                return ["English" , "Hindi" , "Biology" , "Physics" , "Chemistry" , "Physical Education" ,"Music"]
            elif (sub_stream == "non-medical"):
                return ["English" , "Music" , "Maths" , "Physics" , "Chemistry" , "Physical Education"]
            else:
                print("Program terminated due to invalid input.")
                return []   
        elif (stream == "commerce"):
            return ["Accounts"  , "Business studies" , "Maths" , "English" , "Economics"]
        else :
            print("Invalid Stream")
            return []
    else :
        print("Invalid Class")
        return []

def get_marks(subjects):
   
    marks_list = []

    #Take Marks input using loops
    for subject in subjects:

        while True:
            score = float(input(f"Enter marks for subjects {subject} :"))

            if (0 <= score <= 100):
                marks_list.append(score)
                break

            else :
                print("Marks Should be entered between (0 - 100)")

    return marks_list

def calculate_result(marks_list):

    total = sum(marks_list)
    percentage = total / len(marks_list)
    highest = max(marks_list)
    lowest = min(marks_list)

    if (percentage >= 90):
        grade ="A"
    elif (percentage >= 75):
        grade ="B"
    elif (percentage >= 60):
        grade ="C"
    elif (percentage >= 40 ):
        grade ="D"
    else :
        grade ="Fail"

    return total , percentage , highest , lowest , grade

#FACE RECOGNITION

def mark_attendance(name):
    conn = sqlite3.connect("C:/VSCODE/student-smart-progress-tracker/students.db")
    cursor = conn.cursor()

    now = datetime.now()

    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")

    cursor.execute("""
    INSERT INTO attendance
    (name, date, time, status)
    VALUES (?, ?, ?, ?)
    """, (name, date, time, "Present"))

    conn.commit()
    conn.close()

    print(f"Attendance Marked for {name}")

# Data Save Function

def save_result(name, student_class, total, percentage, grade, highest, lowest):
    print("Saving data...")
    
    conn = sqlite3.connect(r"C:\VSCODE\student-smart-progress-tracker\students.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO students
    (name , class, total, percentage, grade, highest, lowest)
    VALUES (?,?,?,?,?,?,?)
    """ , (name , student_class, total, percentage, grade, highest, lowest))

    conn.commit()
    conn.close()


def initialize_db():
    conn = sqlite3.connect(r"C:\VSCODE\student-smart-progress-tracker\students.db")
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

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        date TEXT,
        time TEXT,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()

    
def recognize_face():

    with open("face_data.pkl", "rb") as f:
        data = pickle.load(f)

    known_faces = data["faces"]
    known_names = data["names"]

    cap = cv2.VideoCapture(0)

    while True:

        ret, frame = cap.read()

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        locations = face_recognition.face_locations(rgb)

        encodings = face_recognition.face_encodings(rgb, locations)

        for face_encoding in encodings:

            matches = face_recognition.compare_faces(
                known_faces,
                face_encoding
            )

            if True in matches:

                match_index = matches.index(True)

                name = known_names[match_index]

                print("Face Recognized :", name)

                mark_attendance(name)

                cap.release()
                cv2.destroyAllWindows()

                return name

        cv2.imshow("Face Recognition", frame)

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

    return None


# ========== Main Program ===========
print("====Student Smart Progress Calcuclator====")
initialize_db()

while True:
    print("\n--Scan Student--")
    Name_of_student = recognize_face()

    if Name_of_student is None:
        print("Face Not Recognized")

    else:
        print(f"\nWelcome {Name_of_student}!")

        print("\n1. Enter Marks")
        print("2. Scan Next Student")
        print("3. Exit")

        choice = input("Enter Choice (1/2/3): ").strip()

        if choice == "1":
            student_class = int(input("Enter Class 1-12: "))
            subjects = get_subjects(student_class)

            if not subjects:
                print("Invalid input, skipping...")
                continue

            marks_list = get_marks(subjects)
            total, percentage, highest, lowest, grade = calculate_result(marks_list)

            # ======= Final Input =======

            # Display Final Result
            print("\n ======= Result =======")
            print("Student Name =" ,Name_of_student)
            print("Marks Entered =" ,marks_list)
            print("Total Marks =" ,total)
            print("Percentage =" ,percentage)
            print("Grade = " ,grade )
            print("Highest Marks =",highest)
            print("Lowest Marks =",lowest)
            save_result(Name_of_student, student_class, total, percentage, grade, highest, lowest)
            print("Result Saved Successfully!")


            save_result(Name_of_student, student_class, total, percentage, grade, highest, lowest)
            print("Result Saved Successfully!")

        elif choice == "2":
            print("Scanning next student...")
            continue

        elif choice == "3":
            print("Program Closed!")
            break