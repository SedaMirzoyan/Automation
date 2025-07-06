#!/usr/bin/env python3

import glob
import os
import csv
import re

directories = glob.glob("*/*/compout/views/*")

output_csv = "errors_report.csv"
txt_file = "errors.txt"
#search_pattern = re.search(r"\bErrors:\s*(?!0\b)\d+\b")



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
					print(f"Issue with reading file: {e}")
			elif os.path.isfile(d):
				print(f"{d} is file")


    
def writeIntoCsv():
	with open(txt_file, 'r') as txt, open(output_csv, 'w') as csv_out:
		writer = csv.writer(csv_out)
		writer.writerow(["Instance name", "Log File Path"])
		for line in txt:
			#print(type(line))

			if re.search(r"\bErrors:\s*(?!0\b)\d+\b", line):
				print("Failed instance is {")
				pattern_match = re.search(r"^(.*?)\s*:\s*", line)
				#pattern_second_part = re.search(r"\s*:\s*(.*?)\s*:\s*", line)
				#pattern_second_part = re.search(r":\s*(.*?)\s*:", line)
				if (pattern_match):
					result = pattern_match.group(1).strip()
					writer.writerow([result])				
			else:
				print("No failed instance")
		
	    
	    
    
findInstances()
writeIntoCsv()


	    
	    
	   
	   
 

