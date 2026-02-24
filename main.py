import csv
import os
print("File save ho rahi hai yaha 👉", os.getcwd())
#=====================================================
#Student Smart Progress Calculator
#Author = Aaryan
#Description = Calculate Total Marks , Percentage and Grade
#=====================================================

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
   #Create empty list to store marks
    marks_list = []

    #Take Marks input using loops
    for subject in subjects:
        score = float(input(f"Enter marks for subjects {subject} :"))
        marks_list.append(score)
    return marks_list

def calculate_result(marks_list):

    #Calculating Total Marks
    total = sum(marks_list)
    #Calculating Percentage
    percentage = total / len(marks_list)
    # Find Highest and Lowest Marks
    highest = max(marks_list)
    lowest = min(marks_list)
#Decide Grade based on percentage
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

    file_exists = os.path.isfile("students_progress.csv")

    with open("students_progress.csv", "a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["Name", "Class", "Total", "Percentage", "Grade", "Highest", "Lowest"])

        writer.writerow([name, student_class, total, percentage, grade, highest, lowest])

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