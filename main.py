#=====================================================
#Student Smart Progress Calculator
#Author = Aaryan
#Description = Calculate Total Marks , Percentage and Grade
#=====================================================

print("====Student Smart Progress Calcuclator====")

# Student Name 
Name_of_Student = input("Enter the Name :")

# Taking class From input user 
student_class = int(input("Enter class From 1 to 12 :"))

# Assign Subjects According to class 
if (1 <= student_class <= 10):
    # subjects for classes 1 - 10
    subjects=["English" , "Hindi" , "Maths" , "Science" , "Computer" , "SST"]

elif (student_class==11 or student_class==12):

    # Ask stream for senior classes
    stream = input("Enter the Stream (Science/Commerce) :").strip().lower()
    if (stream == "Science"):

        # Ask for medical or Non Medical
        sub_stream = input("Medical or Non-Medical? :").strip().lower()
        if (sub_stream == "Medical"):
            subjects = ["English" , "Hindi" , "Biology" , "Physics" , "Chemistry" , "Physical Education" ,"Music"]
        elif (sub_stream == "Non-Medical"):
            subjects = ["English" , "Music" , "Maths" , "Physics" , "Chemistry" , "Physical Education"]
        else:
            print("Program terminated due to invalid input.")
            subjects = []   
    elif (stream == "commerce"):
        subjects = ["Accounts"  , "Business studies" , "Maths" , "English" , "Economics"]
    else :
        print("Invalid Stream")
        subjects =[]
else :
    print("Invalid Class")
    subjects = []

if not subjects :
    print("Program Stopped due to invalid input")

#Take number of Subjects as input
num_subjects = len(subjects)

#Create empty list to store marks
marks_list = []

#Take Marks input using loops
for subject in subjects:
    score = float(input(f"Enter marks for subjects {subject} :"))
    marks_list.append(score)
print("Marks List =" ,marks_list)

#Calculating Total Marks
total = sum(marks_list)

#Calculating Percentage
percentage = total / num_subjects

#Print after ending of loop
print("Total Marks =" , total)
print("Percentage =" , percentage)

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

# Display Final Result
print("\n ======= Result =======")
print("Student Name =" ,Name_of_Student)
print("Marks Entered =" ,marks_list)
print("Total Marks =" ,total)
print("Percentage =" ,percentage)
print("Grade = " ,grade )
print("Highest Marks =",highest)
print("Lowest Marks =",lowest)
