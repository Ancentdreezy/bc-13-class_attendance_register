from sqlalchemy.orm import sessionmaker
from db import Student, Classes
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine


engine = create_engine("sqlite:///Class_attendance.db")

Base = declarative_base()

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

#Deleting
def delete_student(student_id):
	delete = session.query(Student).filter_by(student_id=student_id)
	if delete.count() == 0:
		return "\n The student does not exist\n"
	else:
		delete.delete()
		session.commit()
		return "\nStudent ID: " + str(student_id) + " deleted!\n"

def delete_class(class_id):
	delete = session.query(Classes).filter_by(class_id=class_id)
	if delete.count() == 0:
		return " \n The class doesn't exist \n "
	else:
		delete.delete()
		session.commit()
		return "\nClass ID: " + str(class_id) + " deleted!\n"

def get_all_students():
	students = []
	students_rows = session.query(Student).all()
	for students_row in students_rows:
		students.append((students_row.student_id, students_row.first_name, students_row.last_name))

	return students


def get_student_details(student_id):
	student_details = []
	details_rows = session.query(Student).filter_by(student_id=student_id).all()
	for details_row in details_rows:
		student_details.append((details_row.first_name, details_row.last_name))

	return student_details

def get_all_student_ids():
	student_ids = []
	id_rows = session.query(Student).all()
	for id_row in id_rows:
		student_ids.append(id_row.student_id)

	return student_ids

# Functions for classes table
def get_all_classes():
	classes = []
	class_rows = session.query(Classes).all()
	for class_row in class_rows:
		classes.append((class_row.class_id, class_row.subject))

	return classes

def get_class_details(class_id):
	class_details = []
	details_rows = session.query(Classes).filter_by(class_id=class_id).all()
	for details_row in details_rows:
		class_details.append(details_row.subject)

	return class_details

def get_all_class_ids():
	class_ids = []
	id_rows = session.query(Classes).all()
	for id_row in id_rows:
		class_ids.append(id_row.class_id)

	return class_ids
