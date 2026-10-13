import csv
import re
from tabulate import tabulate
import statistics
import sys
class InvalidOption(Exception):
    pass
class OutOfRange(Exception):
    pass

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
        student_scores = []
        while True:
            name = input("Enter student's name:").lower()
            matches=re.fullmatch(r"[A-Za-z]+(?:[ '-][A-Za-z]+)*", name,re.IGNORECASE)

            if matches:
                break
            else:
                print("Invalid input. Please enter a valid name.")




        for i in range(3):
            while True:
                try:
                    scores = int(input("Enter student's score: "))
                    if scores > 100 or scores < 0:
                        raise OutOfRange

                    student_scores.append(scores)
                    break

                except ValueError:
                    print("Invalid input. Please enter a number.")
                except OutOfRange:
                    print("Number inputed is out of range")


        with open("studnets.csv", "a",newline="") as csvfile:
            writer=csv.DictWriter(csvfile,fieldnames=["student_name","first_score","second_score","third_score"])
            if csvfile.tell() == 0:
                writer.writeheader()
            writer.writerow(
             {"student_name":name,
             "first_score":student_scores[0],
             "second_score":student_scores[1],
             "third_score":student_scores[2],


             }
         )
def view_student():
    students = []
    with open("studnets.csv","r",newline="") as csvfile:
        reader=csv.DictReader(csvfile)
        for row in reader:
            students.append(row)
        return tabulate(students, headers="keys", tablefmt="grid")

def view_specific_student():
    while True:
        choice = input("Enter student's name:")
        matches = re.fullmatch(r"[A-Za-z]+(?:[ '-][A-Za-z]+)*", choice,re.IGNORECASE)
        if matches:
            break
        else:
            print("Invalid input. Please enter a valid name.")
            pass


    with open("studnets.csv","r",newline="") as csvfile:
        reader=csv.DictReader(csvfile)
        for row in reader:
            if row["student_name"] == choice:
                return tabulate([row], headers="keys", tablefmt="grid")

        return "Student not found"
def calculate_average():
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

    with open("studnets.csv", "r", newline="") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:


            if row["student_name"]==choic_e:
                average = statistics.mean([
                    int(row["first_score"]),
                    int(row["second_score"]),
                    int(row["third_score"])
                ])
                return tabulate({"student_name":[row["student_name"]],
                        "student_avg":[f"{average:.2f}%"]},headers="keys", tablefmt="grid")
        return "Student not found"

def view_class_stats():
    count = 0
    avg=0
    students=[]
    with open("studnets.csv", "r", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
           avg_stu=statistics.mean([
                    int(row["first_score"]),
                    int(row["second_score"]),
                    int(row["third_score"])
                ])
           row["average"]=avg_stu
           students.append(row)
           avg+=avg_stu
           count += 1
        top_student=max(students, key=lambda student: student["average"])
        least_student=min(students, key=lambda student: student["average"])
        total_avg=avg/count
        return tabulate({"Total Student":[f"{count}"],
                         "Class Average":[f"{total_avg:.2f}%"],
                         "Highest-Performing students":[f"{top_student['student_name']}-{top_student['average']:.2f}%"],
                         "Lowest Performing students":[f"{least_student['student_name']}-{least_student['average']:.2f}%"]
                         },headers="keys", tablefmt="github")








if __name__ == "__main__":
    main()