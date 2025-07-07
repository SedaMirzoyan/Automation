#!/usr/bin/env python3

import glob
import os
import csv
import re
from collections import defaultdict


qa_check_path = "/remote/us01sgnfs00693/ss8/ss8-6428856/work/mirzoyan/qa/all"
const_path = "/*/*/compout/views/*"

full_path_pattern = qa_check_path + const_path
directories = glob.glob(full_path_pattern)


txt_file = "errors.txt"
output_csv = "errors_report.csv"
output_html = "errors_report.html"

data = defaultdict(list)


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
		with open(txt_file, 'r') as log_file:
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
										error_message = file_line.strip().replace("<", "&lt;").replace(">", "&gt;")
										#html.append(f"<tr><td>{inst_name }</td><td>{error_message}</td><td>{inst_path}</td></tr>")
										data[inst_name].append((error_message, inst_path))
						except Exception as e:
							print(f"Issue with writing in csv file: {e}")	
	except Exception as ie:
		print(f"Issue with reading a log file: {ie}")
		
		
		
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
				
						
	html.extend(["</table>", "</body></html>"])
	
	with open(output_html, 'w') as out_html:
		out_html.write("\n".join(html))


	    
	    
    
findInstances()
writeIntoCsv()
writeIntoHtml()

	    
	    
	   
	   
 

