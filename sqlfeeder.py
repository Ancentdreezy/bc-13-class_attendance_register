import sqlite3, datetime, time

connection = sqlite3.connect("Class_attendance.db")
run_cursor = connection.cursor()

class Student(object):
	def __init__(self, firstname, lastname):
		self.firstname = firstname
		self.lastname = lastname


	def save_student(self):
		add_student_query = '''
		INSERT INTO students (first_name, last_name)
		VALUES ('{0}', '{1}')
		'''.format(self.firstname, self.lastname)

		if run_cursor.execute(add_student_query):
			connection.commit()
			return "\nStudent\n" + str(self) + " added!\n"
		return "\nError when adding a student!\n"


	def __str__(self):
		return "First Name: " + self.firstname \
				+ " Last Name: " + str(self.lastname)

class Classes(object):
	def __init__(self, subject):
		self.subject = subject


	def save_class(self):
		subject = self.subject
		add_subject_query = '''
		INSERT INTO classes (subject)
		VALUES ('{0}')
		'''.format(self.subject)

		if run_cursor.execute(add_subject_query):
			connection.commit()
			return "\n" + str(self) + " added!\n"
		return "\nError when adding a class!\n"



	def __str__(self):
		return "Class Subject: " + self.subject
