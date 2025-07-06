#!/usr/bin/env python3

import glob
import os
import csv
import re

directories = glob.glob("*/*/compout/views/*")

output_csv = "errors_report.csv"
txt_file = "errors.txt"
failed_insts = "failed_insts.txt"
#search_pattern = re.search(r"\bErrors:\s*(?!0\b)\d+\b")

data = []



def findInstances():	
	try:
		with open(txt_file, 'w') as txt:
			for d in directories:
				if os.path.isdir(d):
					print("for testing ", d)
					for file_name in os.listdir(d):
						full_path = os.path.join(d, file_name)
						if os.path.isfile(full_path) and file_name.endswith(".log"):
							try:
								with open(full_path, 'r') as log_file:
									for line in log_file:
										if "Errors:" in line:
											ls = line.strip()
											print(ls)
											instance = os.path.basename(full_path)
                                        	#txt.write(f"{instance} : {line.strip()}\n")
											txt.write(f"{instance} : {full_path} : {line.strip()}\n")
							except Exception as re:
								print(f"Issue with reading a file: {re}")
						elif os.path.isfile(d):
							print(f"{d} is file")
	except Exception as we:
		print(f"Issue with writing into a file: {we}")




def writeIntoCsv():
	try:
		with open(txt_file, 'r') as log_file, open(output_csv, 'w') as csv_out:
			writer = csv.writer(csv_out)
			writer.writerow(["Instance name", "Error message", "Log path"])
			for line in log_file:
				parts = line.strip().split(":")
				if re.search(r"\bErrors:\s*(?!0\b)\d+\b", line):
					print("Failed instance is {")
					if(len(parts) >= 2):
						inst_name = parts[0].strip()
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





def writeIntoHtml():
	try:
		with open(txt_file, 'r') as log_file, open(output_csv, 'w') as csv_out:
			writer = csv.writer(csv_out)
			writer.writerow(["Instance name", "Error message", "Log path"])
			for line in log_file:
				parts = line.strip().split(":")
				if re.search(r"\bErrors:\s*(?!0\b)\d+\b", line):
					print("Failed instance is {")
					if(len(parts) >= 2):
						inst_name = parts[0].strip()
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


	    
	    
    
findInstances()
writeIntoCsv()


	    
	    
	   
	   
 

