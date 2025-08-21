import os
import csv
import re
import html
from itertools import groupby
from collections import defaultdict
from abc import ABC, abstractmethod

import sys


#Strategy
class RecordingStrategy(ABC):
    """
    Abstract base class with recording strategies
    """
    @abstractmethod
    def record(self, logger):
        pass


class RecordingInCsvStrategy(RecordingStrategy):
	"""
	Strategy for recording, using csv 
	
	Args:
		module_name (): 
		
	"""
	
	def __init__(self, error_data, module_name):
		self.module_name = module_name
		self.error_data = error_data


	def record(self, logger):
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
			with open(output_csv, 'w') as csv_out:
				writer = csv.writer(csv_out)
				writer.writerow(["Instance name", "Error message", "Log path"])
				for inst_name, path_and_count in self.error_data.items():
					for file_path, error_count in path_and_count:
						match = re.search(r"Errors:\s*(\d+)", error_count)
						if match and int(match.group(1)) != 0:
							inst_name = os.path.basename(file_path)
							try:
								with open(file_path, 'r') as input_file:
									for file_line in input_file:
										if ("ERROR" in file_line):
											writer.writerow([inst_name, file_line.strip(), file_path])
							except FileNotFoundError:
								logging.error(f"File not found: {file_path}")	
		except Exception as ie:
			logging.error(f"Issue with writing in csv file: {ie}")


			

class RecordingInHtmlStrategy(RecordingStrategy):
	"""
	Strategy for recording, using html 
	"""
	
	def __init__(self, error_data, module_name):
		self.module_name = module_name
		self.error_data = error_data
	

	def _add_error(self, data, inst_name, error_message, file_path):
		if inst_name is None:
			raise ValueError("inst_name must be provided and not None")
		inst_name = html.escape(inst_name)
		error_message = html.escape(error_message)
		file_path = html.escape(file_path)
		if inst_name not in data:
			data[inst_name] = []
		data[inst_name].append((error_message, file_path))

	
	def core(self, logger):
		"""
		Records using html

		Args:
			qa_check_path (string): path, provided by user ????????????????????????????????????? change comment
		"""
		logger.info("Calling recording in html method")
		data = defaultdict(list)
		
		"""
		*) Open txt file for reading
		*) Search if number of errors is not equal to 0 ("Errors:")
		*) Take till second ":" symbol, which are instance name (currently it is log file name) and log path
		*) Find actual error message ("ERROR")
		"""	
				
		for inst_name, path_and_count in self.error_data.items():
			for file_path, error_count in path_and_count:
				parts = file_path.strip().split(":")
				match = re.search(r"Errors:\s*(\d+)", error_count)
				if match and int(match.group(1)) != 0:
					inst_name = os.path.basename(file_path)
											
					#"inst_name" is log file name, remove ".log" extension, keep only actual instance name
					inst_name = os.path.splitext(inst_name)[0]
					try:
						with open(file_path, 'r') as input_file:
							for file_line in input_file:
								if ("ERROR" in file_line):
									error_message = file_line.strip().replace("<", "&lt;").replace(">", "&gt;")
									report_components = (inst_name, error_message, file_path)
									#html.append(f"<tr><td>{inst_name }</td><td>{error_message}</td><td>{inst_path}</td></tr>")
									#if(report_components not in seen):
									data[inst_name].append((error_message, file_path))
									print("data itemsssssssssss ", data.keys(), data.values())
					except FileNotFoundError:
						logging.error(f"File not found: {file_path}")	
						
		#self._add_error(data, inst_name, error_message, file_path)
		#self._add_error(self.error_data, inst_name, error_message, file_path)		
			
						 
		return data
							



		
		
	def record(self, logger):
	
		output_html = "errors_report.html"
		data = self.core(logger)

		html_parts = [
    		"<html><head><style>",
    		"table { border-collapse: collapse; width: 100%; }",
    		"th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }",
    		"th { background-color: #f2f2f2; }",
    		"</style></head><body>",
    		"<table>",
    		"<tr><th>Instance name</th><th>Error message</th><th>Log Path</th></tr>"
		]
		
			
		#this part is responsible for html formatting, for one instance there can be multiple error messages, it helps  format that section		
		for key, values in data.items():
			total_rows = len(values)  # Count how many rows this key will span in the table
			first_column_written = False  # Tracks whether we've written the key cell (column 1)

			# Sort the list of tuples by the first element to use groupby correctly
			sorted_values = sorted(values, key=lambda x: x[0])

			# Group the sorted list by the first element of the tuple (e.g., "B", "E")
			for first, group in groupby(sorted_values, key=lambda x: x[0]):
				group_list = list(group)            # Convert the group iterator to a list
				rowspan_first = len(group_list)     # Number of rows the first column cell should span

				# Now write each row for this group
				for i, (_, second) in enumerate(group_list):
					row = "<tr>"  # Start an HTML table row

					# Only write the main key ("A") once with correct rowspan
					if not first_column_written:
						row += f"<td rowspan='{total_rows}'>{key}</td>"
						first_column_written = True  # Mark that we've written the key cell

					# Only write the first column (e.g., "B", "E") on the first row of the group
					if i == 0:
						row += f"<td rowspan='{rowspan_first}'>{first}</td>"

					# Always write the second column (e.g., "C", "D", "F")
					row += f"<td>{second}</td></tr>"

					# Add the completed row to the list
					html_parts.append(row)

		
		html_parts.append("</table>")
		html_parts.append("</body>")
		html_parts.append("</html>")
		
		with open(output_html, 'w') as out_html:
			out_html.write("\n".join(html_parts))


	    	  
#class Recorder:
#	"""
#	Class which uses recording strategy
#	"""	 		
#	def __init__(self, strategy):
#		"""
#		Initialize with a recording strategy
#
#		Args:
#			strategy (RecordingStrategy instance): New recording strategy
#		"""
#
#		self.strategy = strategy
#			
#						
#	def record_data(self, txt_file, logger):
#		"""
#		Records using current strategy
#
#		Args:
#			qa_check_path (string): path, provided by user ????????????????????????????????? change comment
#		"""
#
#		return self.strategy.record(txt_file, logger)
		
		

#Factory		
#class RecordingFactory:
#class StrategyFactory:
#	"""
#	Factory class to create strategy objects
#	"""
#	def get_strategy(self, strategy_choice, module_name):
#		"""
#		Create strategy based on the provided type
#
#		Args:
#			strategy_choice (string): type of a strategy
#			
#		Return:
#			Html or csv object
#		"""
#		if(strategy_choice == "csv"):
#			return RecordingInCsvStrategy(error_data, module_name)
#			pass_data_to_csv(directories):
#		elif(strategy_choice == "html"):
#			return RecordingInHtmlStrategy(error_data, module_name)
#		else:
#			return ValueError("Unknown recording type")
		


#Template
#class RecordingAutomation(ABC):
#	"""
#	Template class to call recording methods
#	"""
#	def template_method(self, csv_obj, html_obj, txt_file, logger):
#		"""
#		Method records with csv and html methods
#		???????????????????????????????????????????????????????????????? change comment
#		
#		"""
#		csv_method = csv_obj.record(txt_file, logger)
#		html_method = html_obj.record(txt_file, logger)

class StrategyFactory:
	"""
	Factory class to create strategy objects
	"""
	def __init__(self, error_data):
		self.error_data = error_data

					

	def get_strategy(self, strategy_choice, module_name):
		"""
		Create strategy based on the provided type

		Args:
			strategy_choice (string): type of a strategy
			
		Return:
			Html or csv object
		"""
		if(strategy_choice == "csv"):
			return RecordingInCsvStrategy(self.error_data, module_name)
		elif(strategy_choice == "html"):
			return RecordingInHtmlStrategy(self.error_data, module_name)
		else:
			return ValueError("Unknown recording type")
		


 
    
class RecordingAutomation(ABC):
	"""
	Template class to call recording methods
	"""
	def run(self, logger):
		self.prepare()
		self.record(logger)
		self.cleanup()
	
	@abstractmethod
	def prepare(self):
		pass
		

	@abstractmethod	
	def record(self, logger):
		#csv_method = csv_obj.record(txt_file, logger)
		#html_method = html_obj.record(txt_file, logger)
		pass
		
	def cleanup(self):
		print("Default cleanup")	



class RecordingInCsvAutomation(RecordingAutomation):
	"""
	Template class to call recording methods
	"""
	def __init__(self, strategy):
		self.strategy = strategy
	 	
	
	def prepare(self):
		print("Preparing creating Csv report")
		
		
	def record(self, logger):
		self.strategy.record(logger)

	def cleanup(self):
		print("Csv cleanup")
		
		

class RecordingInHtmlAutomation(RecordingAutomation):
	"""
	Template class to call recording methods
	"""
	def __init__(self, strategy):
		self.strategy = strategy
	
	def prepare(self):
		print("Preparing creating Html report")

				
	def record(self, logger):
		self.strategy.record(logger)
		
		
	def cleanup(self):
		print("Html cleanup")
