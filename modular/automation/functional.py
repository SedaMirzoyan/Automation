import glob
import os
import re
import logging


def add_logging():
	"""
	Adding logging to a file and console
	
	Return:
		logger (logging.Loger): logger object
	"""

	"""
	Creates root loger with INFO level
	"""
	logger = logging.getLogger()
	logger.setLevel(logging.INFO)
	
	"""
	Log messages into report.log file with overwrite mode.
	File format is level name: message.
	"""

	file_name = logging.FileHandler('report.log', mode='w')
	file_name.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
	logger.addHandler(file_name)
	
	"""
	Log messages to the terminal, with the same format as in log file.
	
	"""
	console_handler = logging.StreamHandler()
	console_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
	logger.addHandler(console_handler)
	
	return logger



def build_directory_path(qa_check_path):
	"""
	Builds absolute path with qa_check_path(provided by user) and const_path variables
	
	Args:
		qa_check_path (string): path, provided by user
	Return:
		directories (list): absolute path		
	"""
	
	#below variable has always the same structure for all QA checks
	const_path = "/*/*/c/v/*"
	
	full_path_pattern = qa_check_path + const_path
	directories = glob.glob(full_path_pattern)	
	
	return directories



def find_instances(error_data, directories):	
	"""
	This method finds log files, redirects instance name, log path, number of errors ("Errors:") into txt file
	
	Args:
		directories (list): absolute path
		txt_file (file): ???????????????????????????????????? change comment
	"""

	for d in directories:
		if os.path.isdir(d):
			for file_name in os.listdir(d):
				full_path = os.path.join(d, file_name)
				if os.path.isfile(full_path) and file_name.endswith(".log"):
					try:
						with open(full_path, 'r') as log_file:
							for line in log_file:
								if "Errors:" in line:
									ls = line.strip()
									instance = os.path.basename(full_path)
									error_data.setdefault(instance, []).append((full_path, ls))
									logging.info(f"Checking file '{instance}' at file path '{full_path}'")
					except Exception as re:
						logging.error(f"Issue with reading a file: {re}")
				elif os.path.isfile(d):
					logging.info(f"{d} is file")







