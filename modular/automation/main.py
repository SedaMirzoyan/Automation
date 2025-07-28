#!/usr/bin/env python3

import sys
import functional 
import automation 
from types import SimpleNamespace



def main():
	qa_check_path = sys.argv[1]
	logger = functional.add_logging()
	"""
	Create simple data container, think of it as a "manual mini module"
	"""
	context = SimpleNamespace()

	txt_file = "errors.txt"
	directories = functional.build_directory_path(qa_check_path)
	functional.find_instances(txt_file, directories)

	"""
	Strategy design pattern: Create recorder with csv recording strategy	
	"""    
	csv_strategy = automation.RecordingInCsvStrategy(module_name=context)
	csv_recorder = automation.Recorder(csv_strategy)

	"""
	Record data using csv strategy 
	"""
	csv_recorded_data = csv_recorder.record_data(txt_file, logger)
	    

	#create recorder with html recording strategy	    
	html_strategy = automation.RecordingInHtmlStrategy(module_name=context)
	html_recorder = automation.Recorder(html_strategy)

	#record data using html strategy 
	html_recorded_data = html_recorder.record_data(txt_file, logger)


	#Factory design pattern	   
	strategy = automation.RecordingFactory()
	csv_fact = strategy.create_strategy("csv", module_name=context)
	html_fact = strategy.create_strategy("html", module_name=context)

	csv_fact.record(txt_file, logger)
	html_fact.record(txt_file, logger)


	#Template design pattern
	tpl_method = automation.RecordingAutomation()
	tpl_method.template_method(csv_fact, html_fact, txt_file, logger)
	
	
	
#	try:
#		os.remove(txt_file)
#		print(f"File '{txt_file}' was deleted successfully.")
#	except FileNotFoundError:
#		print(f"File '{txt_file}' not found.")
#	except Exception as e:
#		print(f"An error occurred: {e}")
	
	
if __name__== "__main__":
	main()	
