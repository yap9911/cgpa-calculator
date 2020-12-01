

courses_list = dict()  # dict[course_id (str)] -> course name (str)
courses_list["FHCT1012"] = "COMPUTING TECHNOLOGY"
courses_list["FHCT1014"] = "INTRODUCTION TO DATA ANALYSIS"
courses_list["FHCT1022"] = "PROGAMMING CONCEPTS AND DESIG"
courses_list["FHMM1014"] = "MATHEMATICS 1"
courses_list["FHMM1024"] = "MATHEMATICS 2"
courses_list["FHSB1224"] = "BIOLOGY 2"
courses_list["FHSC1014"] = "MECHANICS"
courses_list["FHSC1124"] = "ORGANIC CHEMISTRY"


# This class stores all the information for a particular student
class Student:
    name: str
    nric: str
    courses: dict  # dict[course_id (str)] -> results (float)

    def __init__(self, name: str, nric: str, courses: dict):
        self.name = name
        self.nric = nric
        self.courses = courses


# This dictionary stores all the data of students
student_record = dict()  # dict[id (int)] -> Student
student_record[2003001] = Student("Robert", "020413-03-1636", {
    "FHCT1012": "A+",
    "FHMM1014": "A",
})
student_record[2003002] = Student("Tommy", "020826-31-1235", {
    "FHCT1012": "A-",
    "FHMM1014": "B+",
})


# Stores GPA according to the grades.
grades_dict = {
        "A+": 4.0,
        "A": 4.0,
        "A-": 3.6667,
        "B+": 3.3333,
        "B": 3.0,
        "B-": 2.6667,
        "C+": 2.3333,
        "C": 2.0,
        "F": 0
    }
# All helper functions are located here.
# This class encompasses all items for common user interface logics


class CommonInterface:
    is_line_last: bool  # is the last printed string a '----' line?

    # Asks a user with yes/no question
    def ask(self, message):
        print(message, end=" ")
        print("(Y/N)")
        user_input = input().strip().lower()

        self.is_line_last = False

        if user_input == 'y':
            return True
        elif user_input == 'n':
            return False
        else:
            return self.ask("Invalid input.")

    # Asks the user to input information, or press Q/q to quit.
    def ask_or_quit(self, message):
        print(message, end=" ")
        print("or (q)uit: ")
        user_input = input()

        self.is_line_last = False

        if user_input.strip().lower() == 'q':
            exit(0)
        else:
            return user_input

    def ask_with_option(self, message, options: [str]):
        print(message, end=' ')

        userinput = input().strip().lower()
        self.is_line_last = False

        for opt in options:
            if userinput == opt:
                return opt

        # invalid input, repeat again
        return self.ask_with_option(message, options)

    def clear(self):
        self.is_line_last = False
        print('\n' * 100)

    def put_line(self):
        banner_line_width = 80
        print('-' * banner_line_width)
        self.is_line_last = True

    # --------------------------
    # A banner looks like this.
    # --------------------------
    def put_banner(self, message: [str]):
        if not self.is_line_last:
            self.put_line()

        for m in message:
            print(m)

        self.put_line()


# This class encompasses all logics for the user interface seen by an admin
class AdminInterface:
    interface: CommonInterface

    def __init__(self, interface):
        self.interface = interface

    def view_main_menu(self):
        self.interface.clear()
        self.interface.put_banner(["UTAR CFS STUDENT CGPA CALCULATOR"])
        self.interface.put_banner([
            "1. Courses",
            "2. Students' Biodata",
            "3. Student CGPA Calculator",
            "4. Run batch processing",
            "",
            "Q. Quit",
        ])
        opt = self.interface.ask_with_option("Option:", ['1', '2', '3', '4', 'q'])
        if opt == 'q':
            print("Quitting.")
            exit(0)
        else:
            print("Error: Unimplemented function")


# This class encompasses all logics for the user interface seen by a student
class StudentInterface:
    student_id: int
    interface: CommonInterface

    def __init__(self, interface):
        self.student_id = -1
        self.interface = interface

    def ask_for_info(self):
        try:
            self.interface.put_line()
            qinput = self.interface.ask_or_quit("Student's ID")
            self.student_id = int(qinput)
            self.interface.clear()

            # student ID is invalid
            if self.student_id > 9999999:
                raise RuntimeError()

        except RuntimeError:
            print("Invalid student ID. Quitting.")
            exit(0)

        if self.student_id not in student_record:
            self.interface.put_banner(["UTAR CFS STUDENTS' CGPA CALCULATOR"])
            print("Student ID is valid, but record not found.")
            if self.interface.ask("Create a new record?"):
                name = input("Name: ")
                nric = input("NRIC: ")
                student_record[self.student_id] = Student(name, nric, {})
                self.interface.put_line()
            else:
                self.interface.clear()
                return self.ask_for_info()

        return True

    def cgpa_calculation(self):
        total_gp = 0
        total_credit_hour = 0
        cgpa = 0
        count = 0
        student = student_record[self.student_id]
        course_codes = list(student.courses.keys())
        course_grades = list(student.courses.values())

        for i in course_codes:
            total_gp += grades_dict[course_grades[count]] * int((course_codes[count][-1]))
            total_credit_hour += int((course_codes[count][-1]))
            count += 1
        if total_credit_hour != 0:
            cgpa = total_gp / total_credit_hour

    def view_student(self):
        student = student_record[self.student_id]
        Sinterface = StudentInterface(CommonInterface)
        self.interface.put_banner(["{} ({})".format(self.student_id, student.name)])
        self.interface.put_banner(["UTAR CFS STUDENTS' CGPA CALCULATOR"])
        self.interface.put_banner([
                                      ("{:<4}  {:<8.8}  {:<30.30}  {:<5.5}  {:<5.5}  "
                                       .format(i + 1, j, courses_list[j], student.courses[j],
                                               grades_dict[student.courses[j]]))
                                      for (i, j) in enumerate(student.courses.keys())  # enumerate courses code
                                  ] + [
                                        "\n\n"
                                        ] +
                                      [("0{:<4}  TotCH: {:<8.8}  TotGP: {:<30.30}  CGPA: {:<5}   "
                                        .format(i, "-", "-", Sinterface.cgpa_calculation()))
                                      for (i, j) in enumerate(student.courses.keys())
                                  ] + [

                                        "(A)dd  (D)elete  (E)dit    (Q)uit"])

        userinput = self.interface.ask_with_option("Option >>", ['a', 'd', 'e', 'q'])

        # Add
        if userinput == 'a':
            course_id = input("Course: ").upper().strip()
            course_result = input("Grade: ").upper().strip()

            if course_id not in courses_list:
                print("Invalid course. Grade not recorded.")
            elif course_id in student.courses:
                print("Course already exists in student record. Grade not updated.")
            else:
                try:
                    if course_result not in grades_dict.keys():
                        raise RuntimeError
                    else:
                        student_record[self.student_id].courses[course_id] = course_result
                        print("Course added.")
                except RuntimeError:
                    print("Invalid grade. Grade not recorded.")

        # Delete
        elif userinput == 'd':
            course_id = input("Course: ").upper().strip()

            if course_id not in student.courses:
                print("Course not found in student record.")
            else:
                student_record[self.student_id].courses.pop(course_id)
                print("Course deleted.")

        # Edit
        elif userinput == 'e':
            course_id = input("Course: ").upper().strip()
            course_result = input("Grade: ").upper().strip()

            if course_id not in courses_list:
                print("Invalid course. Grade not recorded.")
            elif course_id in student.courses:
                try:
                    if course_result not in grades_dict.keys():
                        raise RuntimeError
                    student_record[self.student_id].courses[course_id] = course_result
                except RuntimeError:
                    print("Invalid result. Result not recorded.")
            else:
                print("Course not found in student record. Result not recorded.")

        # Quit
        elif userinput == 'q':
            print("Quitting.")
            exit(0)


if __name__ == "__main__":
    interface = CommonInterface()

    mode = interface.ask_with_option("(A)dmin mode, (S)tudent mode, or (Q)uit?", ['a', 's', 'q'])

    if mode == 'a':
        ainterface = AdminInterface(interface)

        while True:
            ainterface.view_main_menu()
            input("Press any key to continue... ")
            ainterface.interface.clear()

    elif mode == 's':
        sinterface = StudentInterface(interface)
        sinterface.ask_for_info()
        sinterface.cgpa_calculation()

        while True:
            sinterface.view_student()
            input("Press any key to continue... ")
            sinterface.interface.clear()
    else:
        print("Quitting.")
        exit(0)
