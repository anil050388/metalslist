# importing the required lib
from datetime import date
from dateutil.rrule import rrule, DAILY, YEARLY
from dateutil.relativedelta import relativedelta
import pandas as pd
import json, requests
from datetime import datetime , timedelta, date
# from dotenv import load_dotenv
import os

secret_token = os.environ["token"]
api_key = secret_token


def main():
	#currentday = str(date.today())
	currentday = '2023-05-29'
	d = {'XAU': 'Gold', 'XAG': 'Silver', 'XPT': 'Platinum', 'XPD': 'Palladium' }
	for k in d:
		url = f'https://api.metalpriceapi.com/v1/{currentday}?api_key={api_key}&base={k}'
		response = requests.get(url)
		if response.status_code == 200:
			response = response.json()
			rates = response["rates"]
			dt_obj =  currentday
			new_data = {dt_obj : rates}
			write_json(new_data,k)	
   
#function to add to JSON
def write_json(new_data, k , filename='data.json'):
	with open(filename, 'r+', encoding="utf-8") as file:
		# First we load existing data into a dict.
		print(new_data)
		print(k)
		file_data = json.load(file)
		x = len(file_data[k])-1
		# Join new_data with file_data inside emp_details
		file_data[k][x]["rates"].update(new_data)
		# Sets file's current position at offset.
		file.seek(0)
		# convert back to json.
		json.dump(file_data, file, indent = 4)

if __name__ == '__main__':
    main()