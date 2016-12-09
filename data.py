import sqlite3, datetime, time
import session_db

connection = sqlite3.connect("register.db")
run_cursor = connection.cursor()


class Data(object):
	ongoing_classes = {}
	students_in_class = {}
	class_logs = []

	@staticmethod
	def log_start(class_id):
		start_time = time.asctime(time.localtime(time.time()))

		all_class_ids = session_db.get_all_class_ids()
		if class_id in all_class_ids:
			Data.ongoing_classes[class_id] = start_time
			print("\nClass ID: " + str(class_id) + " started\n" \
					+ "Start time: " + str(start_time) + "\n")
		else:
			print("\nThe class " + str(class_id) + " does not exist!\n")


	@staticmethod
	def check_in(student_id, class_id):
		all_student_ids = session_db.get_all_student_ids()
		student_ids_in_class = []
		for class_id in  Data.students_in_class.keys():
			student_list = Data.students_in_class[class_id]
			for student in student_list:
				student_ids_in_class.append(student)

		if class_id in Data.ongoing_classes.keys() and student_id in all_student_ids:
			if class_id in Data.students_in_class.keys():
				if student_id not in student_ids_in_class:
					Data.students_in_class[class_id].append(student_id)
				else:
					return "\nStudent ID: " + str(student_id) + " Attended!\n"
			else:
				Data.students_in_class[class_id] = [student_id]
			return "\nStudent ID: " + str(student_id) + " checked in to class " + str(class_id) + "\n"

		else:
			return "\nClass ID or Student ID" + str(class_id) + "does not exist!\n"


	@staticmethod
	def check_out(student_id, class_id, reason):
		if class_id in Data.ongoing_classes.keys():
			students = Data.students_in_class[class_id]
			if student_id in students:
				print("\nStudent ID: " + str(student_id) + "checked out!")
				print("Reason: " + reason + "\n")
				students.remove(student_id)
			else:
				print("\nStudent ID " + str(student_id) + " is not in that class!\n")
		else:
			print("\nClass ID " + str(class_id) + " is not ongoing!\n")


	@staticmethod
	def get_all_classes():
		all_classes = session_db.get_all_classes()
		print("\t")
		print("\tCLASS ID".ljust(15) + "SUBJECT".ljust(15))
		print("\t---------".ljust(15) + "---------".ljust(15))
		for a_class in all_classes:
			print("\t" + str(a_class[0]).ljust(15) + str(a_class[1].ljust(15)) + ("\n"))

	@staticmethod
	def get_ongoing_classes():
		if not Data.ongoing_classes.keys():
			print('\n\tNo onging classes!\n')
		else:
			for class_id in Data.ongoing_classes.keys():
				class_details = session_db.get_class_details(class_id)
				for class_det in class_details:
					print("\n\tOn going class")
					print("Class      --------->      " + class_det + "\n")

				start_time = Data.ongoing_classes[class_id]
				print("\tStart Time: " + start_time + "\n")
				if class_id in Data.students_in_class.keys():
					students = Data.students_in_class[class_id]
					print("\tNumber of students in the class: " + str(len(students)))
					print("\n\tID of Students found in this class\n")
					for student_id in students:
						print("\t\tStudent ID: " + str(student_id) + "\n")


	@staticmethod
	def end_class(class_id):
		end_time = time.asctime(time.localtime(time.time()))
		if class_id in Data.ongoing_classes.keys():
			Data.ongoing_classes.pop(class_id)
			print("\nClass ID: " + str(class_id) + " ended!")
			print("End Time: " + end_time + "\n")
		else:
			print("\nClass ID: " + str(class_id) + " not on going!\n")
