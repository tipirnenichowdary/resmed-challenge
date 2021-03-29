import argparse
import requests
import json
import locale
from datetime import datetime
import pandas as pd

# Defining args to run the script
parser = argparse.ArgumentParser()
parser.add_argument('location', help='Sets location and language')
parser.add_argument('sport', help='Sport to get the results for')
args = parser.parse_args()

#Setting Locale
if (args.location):
    locale.setlocale(category=locale.LC_ALL, locale=args.location)

#API call
API_ENDPOINT = "https://ancient-wood-1161.getsandbox.com/results"
headers = {'content-type': 'application/json'}
response = requests.post(url = API_ENDPOINT, headers=headers)

if response.status_code != 200:
    # This means something went wrong.
    raise Exception('Your request did not receive a valid response, Please retry in sometime...')

#Filtering the result by selected sport
result = response.json()[args.sport]

try:
    # Sort the list in reverse chronological order of dates
    sorted_data = sorted(result, key=lambda x: datetime.strptime(x['publicationDate'], '%b %d, %Y %H:%M:%S %p'), reverse=True)
    
    # Print the data in table format
    if(sorted_data):
        formatted_data = pd.DataFrame.from_dict(sorted_data)
        print(formatted_data)

except ValueError:
    print("The provided information could not be processed. Please try again")
except NameError:
    print("Provided data object is undefined!")
else:
    print("Data retrieved successfully")

