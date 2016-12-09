"""
	Commands:
		add_student <firstname> <lastname>
		remove_student <student_id>
		list_students
		class_add <subject>
		remove_class <class_id>
		class_list_all
		log_start <class_id>
		class_list
		log_end <class_id>
		check_in <student_id> <class_id>
		check_out <student_id> <class_id> <reason>
		quit

	Arguments:
		<firstname> Student First Name
		<lastname> Student Last Name
		<student_id> Student ID Number
		<class_id> Class ID Number
		<subject> Subject taught
		<reason> Reason for checking out a student from class
	Options:
		-h, --help  Show this screen and exit
		--version  Show version
"""

from docopt import docopt, DocoptExit
import cmd
import session_db
from sqlfeeder import Classes, Student
from data import Data
from pyfiglet import Figlet
from colorama import Fore
from colorama import Back
from colorama import Style
from colorama import init





def docopt_cmd(func):
	"""
	This decorator is used to simplify the try/except block and pass the result
	of the docopt parsing to the called action
	"""
	def fn(self, arg):
		try:
			opt = docopt(fn.__doc__, arg)

		except DocoptExit as e:
			# The DocoptExit is thrown when the args do not match
			# We print a message to the user and the usage block
			print('Invalid Command!')
			print(e)
			return

		except SystemExit:
			# The SystemExit exception prints the usage for --help
			# We do not need to do the print here
			return


		return func(self, opt)

	fn.__name__ = func.__name__
	fn.__doc__ = func.__doc__
	fn.__dict__.update(func.__dict__)
	return fn


def intro():
	init(autoreset=True)
	font = Figlet(font='doubleshorts')
	print(Fore.GREEN +font.renderText("CLASS ATTENDANCE REGISTER"))
	print("="*60)
	print(Fore.RED + __doc__)

class ClassRegister(cmd.Cmd):
	prompt = "Register >>>"

	# Student Commands
	@docopt_cmd
	def do_add_student(self, arg):
		"""Usage: add_student <firstname> <lastname>"""
		firstname = arg["<firstname>"]
		lastname = arg["<lastname>"]
		student_to_save = Student(firstname, lastname)
		print(student_to_save.save_student())

	@docopt_cmd
	def do_remove_student(self, arg):
		"""Usage: remove_student <student_id>"""
		student_id = arg["<student_id>"]
		print(session_db.delete_student(student_id))

	@docopt_cmd
	def do_list_students(self, arg):
		"""Usage: list_students"""
		students = session_db.get_all_students()
		print("\t")
		print("\tSTUDENT ID".ljust(15) + "FIRST NAME".ljust(15) + "SECOND NAME".ljust(15))
		print("\t-----------".ljust(15) + "----------".ljust(15)+ "------------".ljust(15))
		for a_student in students:
			print("\t" + str(a_student[0]).ljust(15) + a_student[1].ljust(15) + a_student[2].ljust(15))
	# Class Commands
	@docopt_cmd
	def do_class_add(self, arg):
		"""Usage: class_add <subject>... """
		subject = arg["<subject>"]
		subject_name = ''
		for word in subject:
			subject_name += word + ' '

		class_to_save = Classes(subject_name.strip())
		print(class_to_save.save_class())

	@docopt_cmd
	def do_remove_class(self, arg):
		"""Usage: remove_class <class_id>"""
		class_id = arg["<class_id>"]
		print(session_db.delete_class(class_id))


	@docopt_cmd
	def do_class_list_all(self, arg):
		"""Usage: class_list_all """
		Data.get_all_classes()


	@docopt_cmd
	def do_class_list(self, arg):
		"""Usage: class_list """
		Data.get_ongoing_classes()

	# Log Commands
	@docopt_cmd
	def do_log_start(self, arg):
		"""Usage: log_start <class_id> """
		class_id = arg["<class_id>"]
		Data.log_start(int(class_id))


	@docopt_cmd
	def do_log_end(self, arg):
		"""Usage: log_end <class_id> """
		class_id = arg["<class_id>"]
		Data.end_class(int(class_id))


	# Check In/Out Student
	@docopt_cmd
	def do_check_in(self, arg):
		"""Usage: check_in <student_id> <class_id>"""
		student_id = arg["<student_id>"]
		class_id = arg["<class_id>"]
		print(Data.check_in(int(student_id), int(class_id)))


	@docopt_cmd
	def do_check_out(self, arg):
		"""Usage: check_out <student_id> <class_id> <reason>"""
		student_id = arg["<student_id>"]
		class_id = arg["<class_id>"]
		reasons = arg["<reason>"]
		check_out_reason = ""
		for reason in reasons:
			check_out_reason += reason
		Data.check_out(int(student_id), int(class_id), check_out_reason.strip())


	@docopt_cmd
	def do_quit(self, arg):
		"""Usage: quit"""
		exit()

if __name__ == "__main__":
	intro()
	ClassRegister().cmdloop()
