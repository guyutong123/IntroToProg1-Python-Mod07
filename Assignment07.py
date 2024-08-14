# ------------------------------------------------------------------------------------------ #
# Title: Assignment07
# Desc: This assignment demonstrates using data classes
# with structured error handling
# Change Log: (Who, When, What)
#   RRoot,1/1/2030,Created Script
#   <yutong gu>,<8/10/24>,<Classes and Objects>
# ------------------------------------------------------------------------------------------ #
import json

# Define the Data Constants
MENU: str = '''
---- Course Registration Program ----
  Select from the following menu:  
    1. Register a Student for a Course.
    2. Show current data.  
    3. Save data to a file.
    4. Exit the program.
----------------------------------------- 
'''
FILE_NAME: str = "Enrollments.json"

# Define the Data Variables
students: list = []  # a table of student data
menu_choice: str  # Hold the choice made by the user.

# Person Class
class Person:
    def __init__(self, first_name: str, last_name: str):
        self.first_name = first_name
        self.last_name = last_name

    @property
    def first_name(self) -> str:
        return self._first_name.title()

    @first_name.setter
    def first_name(self, value: str) -> None:
        if value.isalpha():
            self._first_name = value
        else:
            raise ValueError("First Name must be alphabetic")

    @property
    def last_name(self) -> str:
        return self._last_name.title()

    @last_name.setter
    def last_name(self, value: str) -> None:
        if value.isalpha():
            self._last_name = value
        else:
            raise ValueError("Last Name must be alphabetic")

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

# Student Class inheriting from Person
class Student(Person):
    def __init__(self, first_name: str, last_name: str, course_name: str):
        super().__init__(first_name, last_name)
        self.course_name = course_name

    @property
    def course_name(self) -> str:
        return self._course_name

    @course_name.setter
    def course_name(self, value: str) -> None:
        self._course_name = value

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}, {self.course_name}"

# Processing Class
class FileProcessor:
    """ A collection of processing layer functions that work with JSON files """

    @staticmethod
    def read_data_from_file(file_name: str, student_data: list) -> list:
        """ This function reads data from a JSON file and loads it into a list of Student objects """
        file_data = []
        file = None
        try:
            file = open(file_name, "r")
            file_data = json.load(file)
        except Exception as e:
            IO.output_error_messages(message="Error: There was a problem with reading the file.", error=e)
        finally:
            if file is not None and not file.closed:
                file.close()

        for row in file_data:
            first_name = row.get("first_name", "")
            last_name = row.get("last_name", "")
            course_name = row.get("course_name", "")

            # Validate the names before creating a Student object
            if first_name.isalpha() and last_name.isalpha():
                student_data.append(Student(first_name, last_name, course_name))
            else:
                print(f"Skipped invalid entry: {row}")

        return student_data

    @staticmethod
    def write_data_to_file(file_name: str, student_data: list) -> None:
        """ This function writes data to a JSON file with data from a list of Student objects """
        file_data = []
        for student in student_data:
            file_data.append({
                "first_name": student.first_name,
                "last_name": student.last_name,
                "course_name": student.course_name
            })
        file = None
        try:
            file = open(file_name, "w")
            json.dump(file_data, file, indent=4)
        except Exception as e:
            message = "Error: There was a problem with writing to the file.\n"
            message += "Please check that the file is not open by another program."
            IO.output_error_messages(message=message, error=e)
        finally:
            if file is not None and not file.closed:
                file.close()

# Presentation Class
class IO:
    """ A collection of presentation layer functions that manage user input and output """

    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        """ This function displays custom error messages to the user """
        print(message, end="\n\n")
        if error is not None:
            print("-- Technical Error Message -- ")
            print(error, error.__doc__, type(error), sep='\n')

    @staticmethod
    def output_menu(menu: str):
        """ This function displays the menu of choices to the user """
        print()  # Adding extra space to make it look nicer.
        print(menu)
        print()  # Adding extra space to make it look nicer.

    @staticmethod
    def input_menu_choice() -> str:
        """ This function gets a menu choice from the user """
        choice = "0"
        try:
            choice = input("Enter your menu choice number: ")
            if choice not in ("1", "2", "3", "4"):  # Note these are strings
                raise Exception("Please, choose only 1, 2, 3, or 4")
        except Exception as e:
            IO.output_error_messages(e.__str__())  # Not passing e to avoid the technical message
        return choice

    @staticmethod
    def output_student_and_course_names(student_data: list):
        """ This function displays the student and course names to the user """
        print("-" * 50)
        for student in student_data:
            print(f'Student {student.first_name} {student.last_name} is enrolled in {student.course_name}')
        print("-" * 50)

    @staticmethod
    def input_student_data(student_data: list) -> list:
        """ This function gets the student's first name, last name, and course name from the user """
        try:
            student_first_name = input("Enter the student's first name: ")
            student_last_name = input("Enter the student's last name: ")
            course_name = input("Please enter the name of the course: ")
            student = Student(student_first_name, student_last_name, course_name)
            student_data.append(student)
            print()
            print(f"You have registered {student_first_name} {student_last_name} for {course_name}.")
        except ValueError as e:
            IO.output_error_messages(message="One of the values was not the correct type of data!", error=e)
        except Exception as e:
            IO.output_error_messages(message="Error: There was a problem with your entered data.", error=e)
        return student_data

# Start of the main body

# When the program starts, read the file data into a list of lists (table)
students = FileProcessor.read_data_from_file(file_name=FILE_NAME, student_data=students)

# Present and Process the data
while True:
    IO.output_menu(menu=MENU)
    menu_choice = IO.input_menu_choice()

    if menu_choice == "1":  # Input user data
        students = IO.input_student_data(student_data=students)
    elif menu_choice == "2":  # Present the current data
        IO.output_student_and_course_names(student_data=students)
    elif menu_choice == "3":  # Save the data to a file
        FileProcessor.write_data_to_file(file_name=FILE_NAME, student_data=students)
    elif menu_choice == "4":  # Stop the loop
        break
    else:
        print("Please only choose option 1, 2, 3, or 4")

print("Program Ended")

