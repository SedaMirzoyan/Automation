#!/usr/bin/env python3

import glob
import os
import csv
import re
import pandas as pd

directories = glob.glob("*/*/compout/views/*")

output_csv = "errors_report.csv"
txt_file = "errors.txt"
failed_insts = "failed_insts.txt"
#search_pattern = re.search(r"\bErrors:\s*(?!0\b)\d+\b")

data = []



def findInstances():	
	with open(txt_file, 'w') as txt:
		for d in directories:
			if os.path.isdir(d):
				print("for testing ", d)
				try:
					for file_name in os.listdir(d):
						full_path = os.path.join(d, file_name)
						if os.path.isfile(full_path) and file_name.endswith(".log"):
							with open(full_path, 'r') as log_file:
								for line in log_file:
									if "Errors:" in line:
										ls = line.strip()
										print(ls)
										instance = os.path.basename(full_path)
                                        #txt.write(f"{instance} : {line.strip()}\n")
										txt.write(f"{instance} : {full_path} : {line.strip()}\n")
				except Exception as e:
					print(f"Issue with writing in file: {e}")
			elif os.path.isfile(d):
				print(f"{d} is file")




def writeIntoCsv():
	with open(txt_file, 'r') as txt:
		for line in txt:
			if re.search(r"\bErrors:\s*(?!0\b)\d+\b", line):
				print("Failed instance is {")
				if(len(parts) >= 2):
					#inst_name = parts[0].strip()
					inst_name = parts[0]
					inst_path = parts[1]
					
					try:
						with open(path, 'r') as log_file:
							for file_line in log_file:
								if ("ERROR" in file_line):
									data.append([inst_name, inst_path])
					
					except Exception as e:
						print(f"Issue with reading log file: {e}")	


	df = pd.DataFrame(data, columns = ["Instance name", "Error message"])
	df.to_csv("errors_report_pandas.csv", index = False)								
			
			



	    
	    
    
findInstances()
writeIntoCsv()


	    
	    
	   
	   
 

