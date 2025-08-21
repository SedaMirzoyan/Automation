#!/usr/bin/env python3

import sys
import logging
import functional 
import automation 
from pathlib import Path
from types import SimpleNamespace

from collections import defaultdict

def main():
	logger = functional.add_logging()
	
	if(len(sys.argv) < 2):
		print("Error: Directory path argument is missing")
		return

	#qa_check_path = sys.argv[1]
	qa_check_path = Path(sys.argv[1])
	print("qcp  ",qa_check_path) 
	
	if not qa_check_path.exists():
		print("Error: Path does not exist")
		return
	
	if not qa_check_path.is_dir():
		print("Error: Path is not a directory")
		return
			
	"""
	Create simple data container, like "manual mini module"
	"""
	context = SimpleNamespace()

	#error_data = {}
	directories = functional.build_directory_path(qa_check_path)
	print("directories  ",directories )
	error_data = functional.find_instances(directories)
	
	for key in error_data:
		print(key)
	
#	for key, value in error_data.items():
#		print(f"{key}: {value} kv")
	


#	"""
#	Strategy design pattern: Create recorder with csv recording strategy	
#	"""    
#	csv_strategy = automation.RecordingInCsvStrategy(module_name=context)
#	csv_recorder = automation.Recorder(csv_strategy)
#
#	"""
#	Record data using csv strategy 
#	"""
#	csv_recorded_data = csv_recorder.record_data(error_data, logger)
#	    
#
#	#create recorder with html recording strategy	    
#	html_strategy = automation.RecordingInHtmlStrategy(module_name=context)
#	html_recorder = automation.Recorder(html_strategy)
#
#	#record data using html strategy 
#	html_recorded_data = html_recorder.record_data(error_data, logger)

##
##	#Factory design pattern	   
##	strategy = automation.StrategyFactory()
##	csv_fact = strategy.get_strategy("csv", module_name=context)
##	html_fact = strategy.get_strategy("html", module_name=context)
##	tpl_method = automation.RecordingInCsvAutomation(csv_fact)
##	tpl_method.run(error_data, logger)


#
#	csv_fact.record(error_data, logger)
#	html_fact.record(error_data, logger)
#
#
#	#Template design pattern
#	tpl_method = automation.RecordingAutomation()
#	tpl_method.template_method(csv_fact, html_fact, error_data, logger)
	


	factory = automation.StrategyFactory(error_data)
	csv_strategy = factory.get_strategy("csv", module_name=context)
	csv_tpl_method = automation.RecordingInCsvAutomation(csv_strategy)
	csv_tpl_method.run(logger)
	
	html_strategy = factory.get_strategy("html", module_name=context)
	html_tpl_method = automation.RecordingInHtmlAutomation(html_strategy)
	html_tpl_method.run(logger)	



#	strategy = functional.StrategyFactory(directories).get_strategy("csv", module_name=context)
#    
#	# Pass the strategy to the automation, which follows the Template pattern
#	automation_1 = automation.RecordingInCsvAutomation(strategy)
#    
#	# Run the automation with the required data
#	automation_1.run(logger)
	
if __name__== "__main__":
	main()	
