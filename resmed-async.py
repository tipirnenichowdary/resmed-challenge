import argparse
import requests
import json
import locale
from datetime import datetime
import pandas as pd
import aiohttp
import asyncio
import os
from aiohttp import ClientSession
from urllib.error import HTTPError

parser = argparse.ArgumentParser()
parser.add_argument('location', help='Sets location and language')
parser.add_argument('sport', help='Sport to get the results for')

args = parser.parse_args()

#Setting Locale
if (args.location):
    locale.setlocale(category=locale.LC_ALL, locale=args.location)

#API call
API_ENDPOINT = "https://ancient-wood-1161.getsandbox.com/results"
HEADERS = {'content-type': 'application/json'}

SPORTS_LIST = [args.sport]

async def get_sport_details_async(sport):
    """Get sport details using ancient-wood API (asynchronously)"""
    url = API_ENDPOINT
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=HEADERS) as response:
                response.raise_for_status()
                print(f"Response status ({url}): {response.status}")
                response_json = await response.json()
                return response_json
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error ocurred: {err}")

async def run_program(sport):
    """Wrapper for running program in an asynchronous manner"""
    try:
        response = await get_sport_details_async(sport)
        response = response[sport]
        sorted_data = sorted(response, key=lambda x: datetime.strptime(x['publicationDate'], '%b %d, %Y %H:%M:%S %p'), reverse=True)

        # Print the data in table format
        formatted_data = pd.DataFrame.from_dict(sorted_data)
        print(formatted_data)
    except Exception as err:
        print(f"Exception occured: {err}")
        pass

loop = asyncio.get_event_loop()
loop.run_until_complete(get_sport_details_async(SPORTS_LIST))
loop.run_until_complete(
    asyncio.gather(
        *(run_program(args) for args in SPORTS_LIST)
    )
)