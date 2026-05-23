#=====================================================
#Student Smart Progress Calculator
#Author = Aaryan
#Description = Calculate Total Marks , Percentage and Grade
#=====================================================

import sqlite3

print("====Student Smart Progress Calcuclator====")

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
                print("Marks Should be entered between (1 - 100)")

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


# Data Save Function

def save_result(name, student_class, total, percentage, grade, highest, lowest):
    print("Saving data...")
    
    conn = sqlite3.connect("C:\VSCODE\student-smart-progress-tracker\students.db")
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
    INSERT INTO students
    (name , class, total, percentage, grade, highest, lowest)
    VALUES (?,?,?,?,?,?,?)
    """ , (name , student_class, total, percentage, grade, highest, lowest))

    conn.commit()
    conn.close()


# ========== Main Program ===========
Name_of_student = input("Enter Student Name :")
student_class = int(input("Enter class 1- 12 :"))

subjects = get_subjects(student_class)

if not subjects:
    print("program stopped due to invalid input")
    exit()

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