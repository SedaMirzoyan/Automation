#!/usr/bin/env python3

import sys
import functional 
import automation 
from types import SimpleNamespace



def main():
	qa_check_path = sys.argv[1]
	logger = functional.add_logging()
	"""
	Create simple data container, like "manual mini module"
	"""
	context = SimpleNamespace()

	#txt_file = "errors.txt"
	error_data = {}
	directories = functional.build_directory_path(qa_check_path)
	functional.find_instances(error_data, directories)

	"""
	Strategy design pattern: Create recorder with csv recording strategy	
	"""    
	csv_strategy = automation.RecordingInCsvStrategy(module_name=context)
	csv_recorder = automation.Recorder(csv_strategy)

	"""
	Record data using csv strategy 
	"""
	csv_recorded_data = csv_recorder.record_data(error_data, logger)
	    

	#create recorder with html recording strategy	    
	html_strategy = automation.RecordingInHtmlStrategy(module_name=context)
	html_recorder = automation.Recorder(html_strategy)

	#record data using html strategy 
	html_recorded_data = html_recorder.record_data(error_data, logger)


	#Factory design pattern	   
	strategy = automation.RecordingFactory()
	csv_fact = strategy.create_strategy("csv", module_name=context)
	html_fact = strategy.create_strategy("html", module_name=context)

	csv_fact.record(error_data, logger)
	html_fact.record(error_data, logger)


	#Template design pattern
	tpl_method = automation.RecordingAutomation()
	tpl_method.template_method(csv_fact, html_fact, error_data, logger)
	
	
	
	
if __name__== "__main__":
	main()	
