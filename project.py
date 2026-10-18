import csv
import re
from fileinput import filename
from pathlib import Path
from sys import prefix

from tabulate import tabulate
import statistics
import sys
class InvalidOption(Exception):
    pass
class OutOfRange(Exception):
    pass

NAME_PATTERN = re.compile(r"[A-Za-z]+(?:[ '-][A-Za-z]+)*")

science_columns = [
    "student_id", "student_name", "department",
    "English_Language_CA", "English_Language_Exam",
    "General_Mathematics_CA", "General_Mathematics_Exam",
    "Civic_Education_CA", "Civic_Education_Exam",
    "Computer_Studies_CA", "Computer_Studies_Exam",
    "Trade_Subject", "Trade_CA", "Trade_Exam",
    "Biology_CA", "Biology_Exam",
    "Chemistry_CA", "Chemistry_Exam",
    "Physics_CA", "Physics_Exam",
    "Agricultural_Science_CA", "Agricultural_Science_Exam",
    "Further_Mathematics_CA", "Further_Mathematics_Exam",
    "Geography_CA", "Geography_Exam",
]

arts_columns = [
    "student_id", "student_name", "department",
    "English_Language_CA", "English_Language_Exam",
    "General_Mathematics_CA", "General_Mathematics_Exam",
    "Civic_Education_CA", "Civic_Education_Exam",
    "Digital_Technologies_CA", "Digital_Technologies_Exam",
    "Literature_in_English_CA", "Literature_in_English_Exam",
    "Government_CA", "Government_Exam",
    "History_CA", "History_Exam",
    "CRS_CA", "CRS_Exam",
    "Yoruba_CA", "Yoruba_Exam",
]

commercial_columns = [
    "student_id", "student_name", "department",
    "English_Language_CA", "English_Language_Exam",
    "General_Mathematics_CA", "General_Mathematics_Exam",
    "Civic_Education_CA", "Civic_Education_Exam",
    "Yoruba_CA", "Yoruba_Exam",
    "Economics_CA", "Economics_Exam",
    "Commerce_CA", "Commerce_Exam",
    "Financial_Accounting_CA", "Financial_Accounting_Exam",
    "Office_Practice_Bookkeeping_CA",
    "Office_Practice_Bookkeeping_Exam",
]

def main():
    print("""
    STUDENT PERFORMANCE ANALYZER
    1. Add student
    2. Find a specific student
    3. View all students
    4. Calculate student average
    5. View class statistics
    6. Quit
    """)
    while True:
        try:
            teacher = int(input("What are you doing today?Select from choice above and enter the number: "))
            if teacher not in range(1,7):
                raise InvalidOption
            break
        except ValueError:
            print("Invalid input. Please enter a number.")
        except InvalidOption:
            print("Invalid input. Please enter a valid option.")
            pass
    if teacher==1:
        add_student()
        print("Student Added Successfully")
    elif teacher==3:
        view_all=view_student()
        print(view_all)
    elif teacher==2:
        specific_student=view_specific_student()
        print(specific_student)
    elif teacher==4:
        get_average=calculate_average()
        print(get_average)
    elif teacher==5:
        class_stats=view_class_stats()
        print(class_stats)
    elif teacher==6:
        sys.exit("Logging out....")


def add_student():
    print("""
        CHOOSE DEPARTMENT
        1. Science
        2. Art
        3. Commercial
        """)
    department_choice=int(input("Select department option above: "))
    if department_choice==1:
        filename="science_student.csv"
        columns=science_columns
        prefix="SCI"
        department="science"
    elif department_choice==2:
        filename="art_students.csv"
        colunms=arts_columns
        prefix = "ART"
        department="art"
    elif department_choice==3:
        filename="commercial_students.csv"
        colunms=commercial_columns
        prefix = "COM"
        department="commercial"
    while True:
        student_name=input("Enter student name: ").strip()
        if NAME_PATTERN.fullmatch(student_name):
            break
        print("Invalid input. Please enter a valid student name.")

    highest_number = 0

    if Path(filename).exists():
        with open(filename, "r", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                student_id = row["student_id"]

                if student_id.startswith(prefix):
                    number = int(student_id[3:])

                    if number > highest_number:
                        highest_number = number

    student_id = f"{prefix}{highest_number + 1:03d}"

    scores={}
    for column in columns:
        if column in ["student_name","department","student_id"]:
            continue #continue means to skip
        else:
            while True:
                score=input(f"Enter {column}: ")
                if column.endswith("_CA"):
                    maximum=40
                else:
                    maximum=60
                if score.isdigit() and 0<=int(score)<=maximum:
                    scores[column]=score
                    break
                print("Invalid score. Please enter a valid score between 0 and 40.")
    student={
        "student_id":student_id,
        "student_name":student_name,
        "department":department,
    }
    student.update(scores)

    with open(filename, "a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writerow(student)





def view_student():
    students = []
    print("""
            CHOOSE DEPARTMENT
            1. Science
            2. Art
            3. Commercial
            """)
    department_choice = int(input("Select department option above: "))
    if department_choice==1:
        filename="science_student.csv"
        # columns=science_columns
        # prefix="SCI"
        # department="science"
    elif department_choice==2:
        filename="art_students.csv"
    #     colunms=arts_columns
    #     prefix = "ART"
    #     department="art"
    elif department_choice==3:
         filename="commercial_students.csv"
    #     colunms=commercial_columns
    #     prefix = "COM"
    #     department="commercial"

    with open(filename,"r",newline="") as csvfile:
        reader=csv.DictReader(csvfile)
        for row in reader:
            students.append(row)
    return tabulate(students, headers="keys", tablefmt="grid")

def view_specific_student():
    print("""
                CHOOSE DEPARTMENT
                1. Science
                2. Art
                3. Commercial
                """)
    department_choice = int(input("Select department option above: "))
    if department_choice == 1:
        filename = "science_student.csv"
        # columns=science_columns
        # prefix="SCI"
        # department="science"
    elif department_choice == 2:
        filename = "art_students.csv"
    #     colunms=arts_columns
    #     prefix = "ART"
    #     department="art"
    elif department_choice == 3:
        filename = "commercial_students.csv"
    #     colunms=commercial_columns
    #     prefix = "COM"
    #     department="commercial"

    while True:
        choice = input("Enter student's name:")
        matches = re.fullmatch(r"[A-Za-z]+(?:[ '-][A-Za-z]+)*", choice,re.IGNORECASE)
        if matches:
            break
        else:
            print("Invalid input. Please enter a valid name.")
            pass


    with open(filename,"r",newline="") as csvfile:
        reader=csv.DictReader(csvfile)
        for row in reader:
            if row["student_name"] == choice:
                return tabulate([row], headers="keys", tablefmt="grid")

        return "Student not found"

def calculate_average():
    subject_totals = []
    print("""
                CHOOSE DEPARTMENT
                1. Science
                2. Art
                3. Commercial
                """)
    department_choice = int(input("Select department option above: "))
    if department_choice == 1:
        filename = "science_student.csv"
        colunms=science_columns
        # prefix="SCI"
        # department="science"
    elif department_choice == 2:
        filename = "art_students.csv"
        colunms=arts_columns
    #     prefix = "ART"
    #     department="art"
    elif department_choice == 3:
        filename = "commercial_students.csv"
        colunms=commercial_columns
    #     prefix = "COM"
    #     department="commercial"

    while True:
        choic_e = input("Enter student's name: ")
        matches = re.fullmatch(
            r"[A-Za-z]+(?:[ '-][A-Za-z]+)*",
            choic_e
        )

        if matches:
            break
        else:
            print("Invalid input. Please enter a valid name.")

    with open(filename, "r", newline="") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:


            if row["student_name"]==choic_e:
                for column in colunms:
                    if column.endswith("_CA"):
                        exam_column = column.replace("_CA", "_Exam")
                        total = int(row[column]) + int(row[exam_column])
                        subject_totals.append(total)

                overall_average = statistics.mean(subject_totals)
                return tabulate({"student_name":[row["student_name"]],
                        "student_avg":[f"{overall_average:.2f}%"]},headers="keys", tablefmt="grid")
        return "Student not found"

def view_class_stats():
    print("""
                    CHOOSE DEPARTMENT
                    1. Science
                    2. Arts
                    3. Commercial
                    """)

    department_choice = input("Select department option above: ")

    if department_choice == "1":
        filename = "science_student.csv"
        columns = science_columns
    elif department_choice == "2":
        filename = "art_students.csv"
        columns = arts_columns
    elif department_choice == "3":
        filename = "commercial_students.csv"
        columns = commercial_columns
    else:
        print("Invalid department option.")
        return

    count = 0
    avg = 0
    students = []

    with open(filename, "r", newline="") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            subject_totals = []

            for column in columns:
                if column.endswith("_CA"):
                    exam_column = column.replace("_CA", "_Exam")

                    total = int(row[column]) + int(row[exam_column])
                    subject_totals.append(total)

            avg_stu = statistics.mean(subject_totals)

            row["average"] = avg_stu
            students.append(row)

            avg += avg_stu
            count += 1

    if count == 0:
        print("No student records found.")
        return

    top_student = max(students, key=lambda student: student["average"])
    least_student = min(students, key=lambda student: student["average"])
    total_avg = avg / count

    return tabulate(
        {
            "Total Students": [count],
            "Class Average": [f"{total_avg:.2f}%"],
            "Highest-Performing Student": [
                f"{top_student['student_name']} - {top_student['average']:.2f}%"
            ],
            "Lowest-Performing Student": [
                f"{least_student['student_name']} - {least_student['average']:.2f}%"
            ],
        },
        headers="keys",
        tablefmt="github"
    )



if __name__ == "__main__":
    main()