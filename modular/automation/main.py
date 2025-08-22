#!/usr/bin/env python3

import sys
import logging
import functional 
import automation 
from pathlib import Path
from types import SimpleNamespace


def main():
	"""
	This part checks if user input is valid.
	"""
	logger = functional.add_logging()
	
	if(len(sys.argv) < 2):
		print("Error: Directory path argument is missing")
		return

	qa_check_path = Path(sys.argv[1])
	
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


	"""
	Builds absolute path, then collect Error info
	"""
	directories = functional.build_directory_path(qa_check_path)
	error_data = functional.create_error_data(directories)	
	
	"""
	Use strategy creation via factory, not directly
	"""
	factory = automation.StrategyFactory(error_data)
	csv_strategy = factory.get_strategy("csv", module_name=context)
	html_strategy = factory.get_strategy("html", module_name=context)
	
	"""
	Pass the strategies to the automation, which follows the Template pattern.
	"""
	csv_tpl_method = automation.RecordingInCsvAutomation(csv_strategy)
	csv_tpl_method.run(logger)
	html_tpl_method = automation.RecordingInHtmlAutomation(html_strategy)
	html_tpl_method.run(logger)	

	
if __name__== "__main__":
	main()	
