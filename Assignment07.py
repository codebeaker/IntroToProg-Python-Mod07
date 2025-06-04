# ------------------------------------------------------------------------------------------ #
# Title: Assignment07
# Desc: This assignment demonstrates using data classes
# with structured error handling
# Change Log: (Who, When, What)
#   RRoot,1/1/2030,Created Script
#   Sonu Mishra, 6/3/2025, edited and completed script
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

# Define the Data Variables-----------------
students_unsaved: list = []  # a list of unsaved student objects
students_saved: list = [] # a list of saved student objects
menu_choice: str  # Hold the choice made by the user.

# Define object classes------------------

#Person object class
class Person:
    '''
    A class representing person data.
    Properties:
    - first_name (str): first name.
    -last_name (str): last name
    '''
    #initialize the person object
    def __init__(self, first_name: str = "", last_name: str = ""):
        self.first_name = first_name
        self.last_name = last_name


    #get/set first_name property
    @property
    def first_name(self):
        return self.__first_name.title()

    @first_name.setter
    def first_name(self, value: str):
        if value.replace(" ","").isalpha() or value =="":
            self.__first_name = value
        else:
            raise ValueError("The first name should not contain numbers.")

    #get/set last_name property
    @property
    def last_name(self):
        return self.__last_name.title()

    @last_name.setter
    def last_name(self, value: str):
        if value.replace(" ", "").isalpha() or value == "":
            self.__last_name = value
        else:
            raise ValueError("The last name should not contain numbers.")
    def __str__(self):
        return f"{self.first_name},{self.last_name}"


        def __str__(self):
            return f"{self.first_name},{self.last_name}"




#Student object class, which inherits some properties from the Person class
class Student(Person):
    """
    A class representing student data. Inherits first name and last name
    from Person and has an additional property, course_name.
    Properties:
    -first_name (str): first name [inherited]
    -last_name (str): last name [inherited]
    -course_name (str): course name.
    """

    def __init__(self, first_name: str = '', last_name: str = '',
                 course_name: str = ''):
        super().__init__(first_name=first_name, last_name=last_name)
        self.course_name = course_name

    # get/set course_name property
    @property
    def course_name(self):
        return self.__course_name.title()

    @course_name.setter
    def course_name(self, value: str):
        # allow alphanumeric characters
        if value.replace(" ", "").isalnum() or value == "":
            self.__course_name = value
        else:
            raise ValueError("The course name should not contain special characters.")

    def __str__(self):
        return f'{self.first_name},{self.last_name},{self.course_name}'




# Processing layer for reading and writing data --------------------------- #
class FileProcessor:
    """
    A collection of processing layer functions that work with Json files
    """
    @staticmethod
    def read_data_from_file(file_name: str):
        """ This function reads data from a json file and loads it into a list of dictionary rows
        then converts the dictionaries to student objects.
        :param file_name: string data with name of file to read from
        :return: list of objects
        """

        try:
            # Get a list of dictionary rows from the data file
            file = open(file_name, "r")
            json_students = json.load(file)

            # Convert the list of dictionary rows into a list of Student objects

            # TODO replace this line of code to convert dictionary data to Student data
            #student_objects = json_students
            for student in json_students:
                student_object: Student = Student(first_name=student["FirstName"],
                                                  last_name = student["LastName"],
                                                  course_name = student["CourseName"])
                students_saved.append(student_object)

            file.close()

        except Exception as e:
            IO.output_error_messages(message="Error: There was a problem with reading the file.", error=e)

        finally:
            if file.closed == False:
                file.close()
        #Don't forget the return statement!
        return students_saved

    @staticmethod
    def write_data_to_file(file_name: str, student_data: list):
        """ This function writes data to a json file with data, first
         converting a list of objects to a list of dictionary
         rows and then writing to json

        :param file_name: string data with name of file to write to
        :param student_data: list of student objects to be writen to the file

        :return: None
        """

        try:
            students_saved_dict: list = [] #list to hold the dictionary rows

            for student in student_data:
                student_as_dict: dict = {"FirstName": student.first_name,
                                          "LastName": student.last_name,
                                          "CourseName": student.course_name}
                students_saved_dict.append(student_as_dict)

            file = open(file_name, "w")
            json.dump(students_saved_dict, file)
            file.close()

        except Exception as e:
            message = "Error: There was a problem with writing to the file.\n"
            message += "Please check that the file is not open by another program."
            IO.output_error_messages(message=message,error=e)
        finally:
            if file.closed == False:
                file.close()


# Presentation Layer --------------------------------------- #
class IO:
    """
    A collection of presentation layer functions that manage user input and output
    """

    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        """ This function displays custom error messages to the user

        :param message: string with message data to display
        :param error: Exception object with technical message to display

        :return: None
        """
        print(message, end="\n\n")
        if error is not None:
            print("-- Technical Error Message -- ")
            print(error, error.__doc__, type(error), sep='\n')

    @staticmethod
    def output_menu(menu: str):
        """ This function displays the menu of choices to the user
        :return: None
        """
        print()  # Adding extra space to make it look nicer.
        print(menu)
        print()  # Adding extra space to make it look nicer.

    @staticmethod
    def input_menu_choice():
        """ This function gets a menu choice from the user
        :return: string with the users choice
        """
        choice = "0"
        try:
            choice = input("Enter your menu choice number: ")
            if choice not in ("1","2","3","4"):  # Note these are strings
                raise Exception("Please, choose only 1, 2, 3, or 4")
        except Exception as e:
            IO.output_error_messages(e.__str__())  # Not passing e to avoid the technical message

        return choice

    @staticmethod
    def output_student_and_course_names(saved_data: list, unsaved_data: list):
        """ This function displays the student and course names to the user

        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function

        :param student_data: list of dictionary rows to be displayed

        :return: None
        """

        print("-" * 50)
        print("This data has been saved to file:")
        for student in saved_data:
            print(f'{student.first_name} {student.last_name} is enrolled in {student.course_name}')
        print()

        if unsaved_data != []:
            print("--!--"*10)
            print("You still need to save this data:")
            for student in unsaved_data:
                print(f'{student.first_name} {student.last_name} is being '
                      f'enrolled in {student.course_name}')


            # TODO Add code to access Student object data instead of dictionary data
        print("-" * 50)

    @staticmethod
    def input_student_data(student_data: list):
        """ This function gets the student's first name and last name, with a course name from the user

        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function

        :param student_data: list of dictionary rows to be filled with input data

        :return: list
        """
        student = Student()
        student.first_name = input("Enter the student's first name: ")
        student.last_name = input("Enter the student's last name: ")
        student.course_name = input("Please enter the name of the course: ")

        student_data.append(student)
        print()
        print(f"You are registering {student.first_name} {student.last_name} for {student.course_name}.")
        print("Remember to save this data to file!")


    @staticmethod
    def move_unsaved_to_saved(unsaved_data: list, saved_data: list):
        '''
        This function appends items from the 'unsaved' data list to the
        'saved' data list, and clears the 'unsaved' data.
        :param unsaved_data:
        :param saved_data:
        :return: saved_data: list
        '''
        for item in unsaved_data:
            saved_data.append(item)
        unsaved_data.clear()
        return saved_data


# Start of main body

# When the program starts, read the file data into a list of lists (table)
# Extract the data from the file
students = FileProcessor.read_data_from_file(file_name=FILE_NAME)

# Present and Process the data
while (True):

    # Present the menu of choices
    IO.output_menu(menu=MENU)

    menu_choice = IO.input_menu_choice()

    # Input user data
    if menu_choice == "1":
        students = IO.input_student_data(students_unsaved)
        continue

    # Present the current data
    elif menu_choice == "2":
        IO.output_student_and_course_names(students_saved, students_unsaved)
        continue

    # Save the data to a file
    elif menu_choice == "3":
        IO.move_unsaved_to_saved(students_unsaved, students_saved)
        FileProcessor.write_data_to_file(FILE_NAME, students_saved)
        #show the user the data that is now saved as confirmation
        IO.output_student_and_course_names(students_saved, students_unsaved)
        continue

    # Stop the loop
    elif menu_choice == "4":
        break  # out of the loop
    else:
        print("Please only choose option 1, 2, or 3")

print("Program Ended")
