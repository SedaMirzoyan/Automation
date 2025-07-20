#!/usr/bin/env python3

import glob
import os
import csv
import re
import sys
import logging
from collections import defaultdict
from abc import ABC, abstractmethod


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
	const_path = "/*/*/compout/views/*"
	
	full_path_pattern = qa_check_path + const_path
	directories = glob.glob(full_path_pattern)	
	
	return directories



#def find_instances(txt_file, directories):	
#	"""
#	This method finds log files, redirects instance name, log path, number of errors ("Errors:") into txt file
#	
#	Args:
#		directories (list): absolute path
#		txt_file (file): ???????????????????????????????????? change comment
#	"""
#	try:
#		with open(txt_file, 'w') as txt:
#			for d in directories:
#				if os.path.isdir(d):
#					for file_name in os.listdir(d):
#						full_path = os.path.join(d, file_name)
#						if os.path.isfile(full_path) and file_name.endswith(".log"):
#							try:
#								with open(full_path, 'r') as log_file:
#									for line in log_file:
#										if "Errors:" in line:
#											ls = line.strip()
#											instance = os.path.basename(full_path)
#											txt.write(f"{instance} : {full_path} : {ls}\n")
#							except Exception as re:
#								print(f"Issue with reading a file: {re}")
#						elif os.path.isfile(d):
#							print(f"{d} is file")
#	except Exception as we:
#		print(f"Issue with writing into a file: {we}")	
#	print("txt_file ", type(txt_file))


def find_instances(txt_file, directories):	
	"""
	This method finds log files, redirects instance name, log path, number of errors ("Errors:") into txt file
	
	Args:
		directories (list): absolute path
		txt_file (file): ???????????????????????????????????? change comment
	"""
	try:
		with open(txt_file, 'w') as txt:
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
											txt.write(f"{instance} : {full_path} : {ls}\n")
											logging.info(f"Checking file '{instance}' at file path '{full_path}'")
							except Exception as re:
								logging.error(f"Issue with reading a file: {re}")
						elif os.path.isfile(d):
							logging.info(f"{d} is file")
	except Exception as we:
		logging.error(f"Issue with writing into a file: {we}")	
	print("txt_file ", type(txt_file))



#Strategy
class RecordingStrategy(ABC):
    """
    Abstract base class with recording strategies
    """
    @abstractmethod
    def record(self, txt_file):
        pass
		
		


class RecordingInCsvStrategy(RecordingStrategy):
	"""
	Strategy for recording, using csv 
	"""

	def record(self, txt_file, logger):
		"""
		Records using csv

		Args:
    		txt_file (string): path, provided by user ?????????????????????????????????????????? change comment
		"""
		logger.info("Calling recording in csv method")
		output_csv = "errors_report.csv"
		
		
		"""
		*) Open csv file for writing and txt for reading
		*) Search if number of errors is not equal to 0 ("Errors:")
		*) Take till second ":" symbol, which are instance name (currently it is log file name) and log path
		*) Find actual error message ("ERROR")
		*) Write instance name, error message, instance path in csv file
		"""
		try:
			with open(txt_file, 'r') as log_file, open(output_csv, 'w') as csv_out:
				writer = csv.writer(csv_out)
				writer.writerow(["Instance name", "Error message", "Log path"])
				for line in log_file:
					parts = line.strip().split(":")
					if re.search(r"\bErrors:\s*(?!0\b)\d+\b", line):
						inst_name = parts[0].strip()
													
						#"inst_name" is log file name, remove ".log" extension, keep only actual instance name
						inst_name = os.path.splitext(inst_name)[0]
						
						inst_path = parts[1].strip()
						try:
							with open(inst_path, 'r') as input_file:
								for file_line in input_file:
									if ("ERROR" in file_line):
										writer.writerow([inst_name, file_line.strip(), inst_path])
						except FileNotFoundError:
							logging.error(f"File not found: {inst_path}")
						except Exception as e:
							logging.error(f"Issue with writing in csv file: {e}")	
		except Exception as ie:
			logging.error(f"Issue with reading a log file: {ie}")




class RecordingInHtmlStrategy(RecordingStrategy):
	"""
	Strategy for recording, using html 
	"""
	def record(self, txt_file, logger):
		"""
		Records using html

		Args:
			qa_check_path (string): path, provided by user ????????????????????????????????????? change comment
		"""
		logger.info("Calling recording in html method")
		data = defaultdict(list)
		output_html = "errors_report.html"
		seen = set()

		html = [
    		"<html><head><style>",
    		"table { border-collapse: collapse; width: 100%; }",
    		"th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }",
    		"th { background-color: #f2f2f2; }",
    		"</style></head><body>",
    		"<table>",
    		"<tr><th>Instance name</th><th>Error message</th><th>Log Path</th></tr>"
		]
		
		"""
		*) Open txt file for reading
		*) Search if number of errors is not equal to 0 ("Errors:")
		*) Take till second ":" symbol, which are instance name (currently it is log file name) and log path
		*) Find actual error message ("ERROR")
		"""
			
		try:
			with open(txt_file, 'r') as log_file:
				for line in log_file:
					parts = line.strip().split(":")
					if re.search(r"\bErrors:\s*(?!0\b)\d+\b", line):
						inst_name = parts[0].strip()
						inst_name = os.path.splitext(inst_name)[0]
						inst_path = parts[1].strip()
						try:
							with open(inst_path, 'r') as input_file:
								for file_line in input_file:
									if ("ERROR" in file_line):
										error_message = file_line.strip().replace("<", "&lt;").replace(">", "&gt;")
										report_components = (inst_name, error_message, inst_path)
										#html.append(f"<tr><td>{inst_name }</td><td>{error_message}</td><td>{inst_path}</td></tr>")
										#if(report_components not in seen):
										data[inst_name].append((error_message, inst_path))
										#	seen.add(report_components)
						except FileNotFoundError:
							logging.error(f"File not found: {inst_path}")
						except Exception as e:
							logging.error(f"Issue with writing in csv file: {e}")	
		except Exception as ie:
			logging.error(f"Issue with reading a log file: {ie}")
		
		
		#this part is responsible for html formatting, for one instance there can be multiple error messages, it helps  format that section		
#		for inst_name, inst_name_values in data.items():
#			inst_name_values = [i for i in inst_name_values if i[0].strip() and i[1].strip()]
#			if (not inst_name_values):
#				continue
#				
#			rowspan_len = len(inst_name_values)
#			for j, (error_message, path) in enumerate(inst_name_values):
#				if j == 0:
#					html.append(f"<tr><td rowspan='{rowspan_len}'>{inst_name}</td><td>{error_message}</td><td>{inst_path}</td></tr>")
#				else:
#					html.append(f"<tr><td>{error_message}</td><td>{inst_path}</td></tr>")


		for inst_name, inst_name_values in data.items():
			#inst_name_values = [i for i in inst_name_values if i[0].strip() and i[1].strip()]
			if (not inst_name_values):
				continue
				
			for j, (error_message, path) in enumerate(inst_name_values):
				inst_name_report = inst_name if j == 0 else ""
				html.append(f"<tr><td>{inst_name_report}</td><td>{error_message}</td><td>{inst_path}</td></tr>")
				
		
		#*) Write instance name, error message, instance path in html file				
		html.extend(["</table>", "</body></html>"])
		with open(output_html, 'w') as out_html:
			out_html.write("\n".join(html))


	    	  
class Recorder:
	"""
	Class which uses recording strategy
	"""	 		
	def __init__(self, strategy):
		"""
		Initialize with a recording strategy

		Args:
			strategy (RecordingStrategy instance): New recording strategy
		"""

		self.strategy = strategy
			
						
	def record_data(self, txt_file, logger):
		"""
		Records using current strategy

		Args:
			qa_check_path (string): path, provided by user ????????????????????????????????? change comment
		"""

		return self.strategy.record(txt_file, logger)
		
		

#Factory		
class RecordingFactory:
	"""
	Factory class to create strategy objects
	"""
	def create_strategy(self, strategy_choice):
		"""
		Create strategy based on the provided type

		Args:
			strategy_choice (string): type of a strategy
			
		Return:
			Html or csv object
		"""
		if(strategy_choice == "csv"):
			return RecordingInCsvStrategy()
		elif(strategy_choice == "html"):
			return RecordingInHtmlStrategy()
		else:
			return ValueError("Unknown recording type")
		


#Template
class RecordingAutomation:
	"""
	Template class to call recording methods
	"""
	def template_method(self, csv_obj, html_obj, txt_file, logger):
		"""
		Method records with csv and html methods
		???????????????????????????????????????????????????????????????? change comment
		
		"""
		csv_method = csv_obj.record(txt_file, logger)
		html_method = html_obj.record(txt_file, logger)

    



def main():
	qa_check_path = sys.argv[1]
	logger = add_logging()

	txt_file = "errors.txt"
	directories = build_directory_path(qa_check_path)
	find_instances(txt_file, directories)

	#Strategy design pattern
	#create recorder with csv recording strategy	    
	csv_strategy = RecordingInCsvStrategy()
	csv_recorder = Recorder(csv_strategy)

	#record data using csv strategy 
	csv_recorded_data = csv_recorder.record_data(txt_file, logger)
	    

	#create recorder with html recording strategy	    
	html_strategy = RecordingInHtmlStrategy()
	html_recorder = Recorder(html_strategy)

	#record data using html strategy 
	html_recorded_data = html_recorder.record_data(txt_file, logger)


	#Factory design pattern	   
	strategy = RecordingFactory()
	csv_fact = strategy.create_strategy("csv")
	html_fact = strategy.create_strategy("html")

	csv_fact.record(txt_file, logger)
	html_fact.record(txt_file, logger)


	#Template design pattern
	automation = RecordingAutomation()
	automation.template_method(csv_fact, html_fact, txt_file, logger)
	
	
	
#	try:
#		os.remove(txt_file)
#		print(f"File '{txt_file}' was deleted successfully.")
#	except FileNotFoundError:
#		print(f"File '{txt_file}' not found.")
#	except Exception as e:
#		print(f"An error occurred: {e}")
	
	
if __name__== "__main__":
	main()	
