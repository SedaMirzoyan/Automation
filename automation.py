#!/usr/bin/env python3

import glob
import os
import csv
import re
from collections import defaultdict
from abc import ABC, abstractmethod



#Builds absolute path with qa_check_path(provided by user) and const_path variables
def makeDirectoryPath(qa_check_path):
	#below variable has always the same structure for all QA checks
	const_path = "/*/*/compout/views/*"
	
	full_path_pattern = qa_check_path + const_path
	directories = glob.glob(full_path_pattern)	
	
	return directories



#This method finds log files, redirects instance name, log path, number of errors ("Errors:") into txt file
def findInstances(txt_file):	
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
							except Exception as re:
								print(f"Issue with reading a file: {re}")
						elif os.path.isfile(d):
							print(f"{d} is file")
	except Exception as we:
		print(f"Issue with writing into a file: {we}")	



#Strategy
class RecordingStrategy(ABC):
    """
    Abstract base class with recording strategies
    """
    @abstractmethod
    def record(self, qa_check_path):
        pass
		
		


class RecordingInCsvStrategy(RecordingStrategy):
	"""
	Strategy for recording, using csv 
	"""

	def record(self, qa_check_path):
		"""
		Records using csv

		Args:
    		qa_check_path (string): path, provided by user 
		"""
		print("calling recording in csv method")
		output_csv = "errors_report.csv"
		
		
		"""
		*) Open csv file for writing and txt for reading
		*) Search if number of errors is not equal to 0 ("Errors:")
		*) Take till second ":" symbol, means take instance name (currently it is log file name) and log path
		*) Find actual error message (""ERROR")
		*) Write instance name, error message, instance path in csv file
		"""
		try:
			with open(txt_file, 'r') as log_file, open(output_csv, 'w') as csv_out:
				writer = csv.writer(csv_out)
				writer.writerow(["Instance name", "Error message", "Log path"])
				for line in log_file:
					parts = line.strip().split(":")
					if re.search(r"\bErrors:\s*(?!0\b)\d+\b", line):
						if(len(parts) >= 2):
							inst_name = parts[0].strip()
							
							#"inst_name" is log file name, remove ".log" extension, keep only actual instance name
							inst_name = os.path.splitext(inst_name)[0]
							
							inst_path = parts[1].strip()
							try:
								with open(inst_path, 'r') as input_file:
									for file_line in input_file:
										if ("ERROR" in file_line):
											writer.writerow([inst_name, file_line.strip(), inst_path])
							except Exception as e:
								print(f"Issue with writing in csv file: {e}")	
		except Exception as ie:
			print(f"Issue with reading a log file: {ie}")




class RecordingInHtmlStrategy(RecordingStrategy):
	"""
	Strategy for recording, using html 
	"""
	def record(self, qa_check_path):
		"""
		Records using html

		Args:
			qa_check_path (string): path, provided by user 
		"""
		print("calling recording in html method")
		data = defaultdict(list)
		output_html = "errors_report.html"

		html = [
    		"<html><head><style>",
    		"table { border-collapse: collapse; width: 100%; }",
    		"th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }",
    		"th { background-color: #f2f2f2; }",
    		"</style></head><body>",
    		"<h2>Hello Messages</h2>",
    		"<table>",
    		"<tr><th>Instance name</th><th>Error message</th><th>Log Path</th></tr>"
		]
		
		"""
		*) Open txt file for reading
		*) Search if number of errors is not equal to 0 ("Errors:")
		*) Take till second ":" symbol, means take instance name (currently it is log file name) and log path
		*) Find actual error message (""ERROR")
		"""
			
		try:
			with open(txt_file, 'r') as log_file:
				for line in log_file:
					parts = line.strip().split(":")
					if re.search(r"\bErrors:\s*(?!0\b)\d+\b", line):
						if(len(parts) >= 2):
							inst_name = parts[0].strip()
							inst_name = os.path.splitext(inst_name)[0]
							inst_path = parts[1].strip()
							try:
								with open(inst_path, 'r') as input_file:
									for file_line in input_file:
										if ("ERROR" in file_line):
											error_message = file_line.strip().replace("<", "&lt;").replace(">", "&gt;")
											#html.append(f"<tr><td>{inst_name }</td><td>{error_message}</td><td>{inst_path}</td></tr>")
											data[inst_name].append((error_message, inst_path))
							except Exception as e:
								print(f"Issue with writing in csv file: {e}")	
		except Exception as ie:
			print(f"Issue with reading a log file: {ie}")
		
		
		"""
		this part is responsible for html formatting, for one instance there can be multiple error messages,
		it helps 
		"""
		
		for inst_name, inst_name_values in data.items():
			inst_name_values = [i for i in inst_name_values if i[0].strip() and i[1].strip()]
			if (not inst_name_values):
				continue
				
			rowspan = len(inst_name_values)
			for j, (error_message, path) in enumerate(inst_name_values):
				if j == 0:
					html.append(f"<tr><td rowspan='{rowspan}'>{inst_name}</td><td>{error_message}</td><td>{inst_path}</td></tr>")
				else:
					html.append(f"<tr><td>{error_message}</td><td>{inst_path}</td></tr>")
				
		
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
			
						
	def record_data(self, qa_check_path):
		"""
		Records using current strategy

		Args:
			qa_check_path (string): path, provided by user 
		"""

		return self.strategy.record(qa_check_path)
		
		

#Factory		
class RecordingFactory:
	"""
	Factory class to create strategy objects
	"""
	def createStrategy(self, strategy_choice):
		"""
		Create strategy based on the provided type

		Args:
			strategy_choice (string): type of a strategy
			
		Return:
			An object of an html or csv
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
	def template_method(self, csv_obj, html_obj, qa_check_path):
		#records with csv and html methods
		csv_method = csv_obj.record(qa_check_path)
		html_method = html_obj.record(qa_check_path)

    



#please provide path for QA check, currently it is empty
qa_check_path = ""

txt_file = "errors.txt"
directories = makeDirectoryPath(qa_check_path)
findInstances(txt_file)

#Startegy design pattern
#create recorder with csv recording strategy	    
csv_strategy = RecordingInCsvStrategy()
csv_recorder = Recorder(csv_strategy)

#record data using csv strategy 
csv_recorded_data = csv_recorder.record_data(directories)
	    

#create recorder with html recording strategy	    
html_strategy = RecordingInHtmlStrategy()
html_recorder = Recorder(html_strategy)

#record data using html strategy 
html_recorded_data = html_recorder.record_data(directories)


#Factory design pattern	   
strategy = RecordingFactory()
csv_fact = strategy.createStrategy("csv")
html_fact = strategy.createStrategy("html")

csv_fact.record(qa_check_path)
html_fact.record(qa_check_path)


#Template design pattern
automation = RecordingAutomation()
automation.template_method(csv_fact, html_fact, qa_check_path)

