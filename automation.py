#!/usr/bin/env python3

import glob
import os
import csv


directories = glob.glob("*/*/compout/views/*")


for d in directories:
     #directory case
	if os.path.isdir(d):
		try:
			for file_name in os.listdir(d):
				full_path = os.path.join(d, file_name)
 
				if os.path.isfile(full_path):
					print(f"{file_name}")
					if (file_name.endswith(".log")):
						print(f"'Errors:' in {file_name}")
						try:
							with open(full_path, 'r') as log_file:
								for line in log_file:
									if "Errors:" in line:
										ls = line.strip()
										print(ls)
						except Exception as e:
							print(f"Issue with reading file: {e}")
		except Exception as e:
			print(f"Issue with reading directory: {e}")
 
	#file case
	elif os.path.isfile(d):
		print(f"'{d} is file")
		#try:
		#	with open(d, 'r') as log_file:
		#		for line in log_file:
		#			if "Errors:" in line:
		#				ls = line.strip()
		#				print(ls)
		#except Exception as e:
		#	print(f"Issue with reading file: {e}")
 


