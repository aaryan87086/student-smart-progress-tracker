#=====================================================
#Student Smart Progress Calculator
#Author = Aaryan
#Description = Calculate Total Marks , Percentage and Grade
#=====================================================

print("====Student Smart Progress Calcuclator====")

#Take number of Subjects as input
num_subjects = int(input("Enter Number of Subjects :"))

#Create empty list to store marks
marks_list = []

#Take Marks input using loops
for i in range(num_subjects):
    score = float(input("Enter marks for subjects {i+1} :"))
    marks_list.append(score)
print("Marks List =" ,marks_list)

#Calculating Total Marks
total = sum(marks_list)

#Calculating Percentage
percentage = total / num_subjects

#Print after ending of loop
print("Total Marks =" , total)
print("Percentage =" , percentage)

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
    print("Fail")

# Display Final Result
print("\n ======= Result =======")
print("Marks Entered =" ,marks_list)
print("Total Marks =" ,total)
print("Percentage =" ,percentage)
print("Grade = " ,grade )