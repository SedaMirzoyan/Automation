import os
import csv
import re
import html
from itertools import groupby
from collections import defaultdict
from abc import ABC, abstractmethod



#Strategy
class RecordingStrategy(ABC):
	"""
	Abstract base class with recording strategies
    """
	
	@abstractmethod
	def record(self, logger):
		"""
		Abstract method which should be overriden in child classes.
		
		Args:
			logger (logging.Loger): logger object
		"""
		pass


class RecordingInCsvStrategy(RecordingStrategy):
	"""
	Strategy for recording, using csv.  
	
	Attributes:
		module_name (object) : Simple object subclass that provides attribute access to its namespace.
		error_data (dictionary): log file name, absolute path and count of error messages.
	"""
	
	def __init__(self, error_data, module_name):
		"""
		Args:
			module_name (object) : Simple object subclass that provides attribute access to its namespace.
			error_data (dictionary): log file name, absolute path and count of error messages
		"""
		self.module_name = module_name
		self.error_data = error_data


	def record(self, logger):
		"""
		Records using csv.

		Args:
    		logger (logging.Loger): logger object
		"""
		logger.info("Calling recording in csv method")
		output_csv = "errors_report.csv"
		
		
		"""
		*) Open csv file for writing info.
		*) Iterate over dictionary value, check if number of errors (second item in values list) is not equal to 0 ("Errors:")
		*) Find actual error message ("ERROR")
		*) Write instance name, error message, instance path in csv file
		*) Meanwhile check if log file exists and check write permissions for csv file
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
							#"inst_name" is log file name, remove ".log" extension, keep only actual instance name
							inst_name = os.path.splitext(inst_name)[0]
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
	Strategy for recording, using html. 
	"""
	
	def __init__(self, error_data, module_name):
		"""
		Args:
			module_name (object) : Simple object subclass that provides attribute access to its namespace.
			error_data (dictionary): log file name, absolute path and count of error messages
		"""
		self.module_name = module_name
		self.error_data = error_data
	

	def _add_error(self, data, inst_name, error_message, file_path):
		"""
		Escaping input for safety.
		
		Args:
			data (dictionary): it has log file name, absolute path and error message
			inst_name (string): log file name
			error_message (string): Error message
			file_path (string): log file path
			
		"""
		if inst_name is None:
			raise ValueError("inst_name must be provided and not None")
		inst_name = html.escape(inst_name)
		error_message = html.escape(error_message)
		file_path = html.escape(file_path)
		
		"""
		Checks if the instance name is already a key in the data dictionary.
		If not, it creates a new entry with an empty list. Each instance has its own list to store multiple errors
		"""
		if inst_name not in data:
			data[inst_name] = []
		"""
		Adds a tuple (error_message, inst_path) to the list for the given instance.
		"""
		data[inst_name].append((error_message, file_path))


	
	def core(self, logger):
		"""
		Creating dictionary with instance name, error message and log file path.

		Args:
			logger (logging.Loger): logger object
		"""
		logger.info("Calling recording in html method")
		data = defaultdict(list)
		
		"""
		*) Iterate over dictionary value, checks if number of errors (second item in values list) is not equal to 0 ("Errors:")
		*) Find actual error message ("ERROR")
		*) Add instance name, error message and log path tuple to dictionary
		*) Meanwhile check if log file exists and call method for html escaping.
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
									data[inst_name].append((error_message, file_path))
					except FileNotFoundError:
						logging.error(f"File not found: {file_path}")	
						
		self._add_error(self.error_data, inst_name, error_message, file_path)			
						 
		return data
							

		
		
	def record(self, logger):
		"""
		This part is responsible for html formatting, for one instance there can be multiple error messages, it helps  format that section.	
		
		Args:
			logger (logging.Loger): logger object				
		"""
	
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
		
			
		for key, values in data.items():
			"""
			Count how many rows this key will span in the table
			"""
			total_rows = len(values)  
			
			"""
			Tracks whether we've written the key cell (column 1)
			"""
			first_column_written = False  

			"""
			Sort the list of tuples by the first element to use groupby correctly
			"""
			sorted_values = sorted(values, key=lambda x: x[0])

			"""
			Group the sorted list by the first element of the tuple 
			"""
			for first, group in groupby(sorted_values, key=lambda x: x[0]):
				"""
				Convert the group iterator to a list.
				"""
				group_list = list(group)  
				"""
				Number of rows the first column cell should span.
				"""          
				rowspan_first = len(group_list)     

				"""
				Write each row for this group
				"""
				for i, (_, second) in enumerate(group_list):
					"""
					Start an HTML table row
					"""
					row = "<tr>"  

					
					"""
					Only write the main key once with correct rowspan.
					"""
					if not first_column_written:
						row += f"<td rowspan='{total_rows}'>{key}</td>"
						first_column_written = True  # Mark that we've written the key cell

					"""
					Only write the first column on the first row of the group.
					"""
					if i == 0:
						row += f"<td rowspan='{rowspan_first}'>{first}</td>"

					"""
					Always write the second column.
					""" 
					row += f"<td>{second}</td></tr>"

					"""
					Add the completed row to the list.
					"""
					html_parts.append(row)

		
		"""
		Write instance name, error message, instance path in html file.
		"""
		html_parts.append("</table>")
		html_parts.append("</body>")
		html_parts.append("</html>")
		
		with open(output_html, 'w') as out_html:
			out_html.write("\n".join(html_parts))


	    	  
#Factory			  
class StrategyFactory:
	"""
	Factory class to create strategy objects.
	
	Attributes:
		error_data (dictionary): log file name, absolute path and count of error messages.
	"""
	
	
	def __init__(self, error_data):
		"""
		Args:
			error_data (dictionary): log file name, absolute path and count of error messages.
		"""
		self.error_data = error_data

					

	def get_strategy(self, strategy_choice, module_name):
		"""
		Create strategy based on the provided type.

		Args:
			strategy_choice (string): type of a strategy
			module_name (object) : Simple object subclass that provides attribute access to its namespace.
						
		Return:
			Html or csv object.
		"""
		if(strategy_choice == "csv"):
			return RecordingInCsvStrategy(self.error_data, module_name)
		elif(strategy_choice == "html"):
			return RecordingInHtmlStrategy(self.error_data, module_name)
		else:
			return ValueError("Unknown recording type")
		


 
#Template  
class RecordingAutomation(ABC):
	"""
	Template class defines algorithm skeleton, abstarct and hook methods.
	"""
	
	def run(self, logger):
		"""
		Method defines the algorithm skeleton.
		"""
		self.prepare()
		self.record(logger)
		self.cleanup()
		
	
	@abstractmethod
	def prepare(self):
		"""
		Abstract method which should be overriden in child classes.
		"""
		pass
		

	@abstractmethod	
	def record(self, logger):
		"""
		Abstract method which should be overriden in child classes.
		"""
		pass
		
	def cleanup(self):
		"""
		Optional hook method that can be overriden. 
		Prints general message.
		"""
		print("Default cleanup")	



class RecordingInCsvAutomation(RecordingAutomation):
	"""
	Template class to call recording methods
	
	Attributes:
		strategy (object): csv_strategy or html_strategy object.
	"""
	
	def __init__(self, strategy):
		"""
		Args:
			strategy (object): csv_strategy or html_strategy object.
		"""
		self.strategy = strategy
	 	
	
	def prepare(self):
		"""
		Inherited from base class, prints general message.
		"""
		print("Preparing creating Csv report")
		
		
	def record(self, logger):
		"""
		Delegate that responsibility to another object, referenced by self.strategy.
		Actual behavior of record depends on what self.strategy is.
		"""
		self.strategy.record(logger)


	def cleanup(self):
		"""
		Inherited form base class, prints general message.
		"""
		print("Csv cleanup")
		
		

class RecordingInHtmlAutomation(RecordingAutomation):
	"""
	Template class to call recording methods
	
	Attributes:
		strategy (object): csv_strategy or html_strategy object.
	"""
	
	def __init__(self, strategy):
		"""
		Args:
			strategy (object): csv_strategy or html_strategy object
		"""
		self.strategy = strategy
	
	
	def prepare(self):
		"""
		Inherited from base class, prints general message.
		"""
		print("Preparing creating Html report")

				
	def record(self, logger):
		"""
		Delegate that responsibility to another object, referenced by self.strategy.
		Actual behavior of record depends on what self.strategy is.
		"""
		self.strategy.record(logger)
		
		
	def cleanup(self):
		"""
		Inherited form base class, prints general message.
		"""
		print("Html cleanup")
