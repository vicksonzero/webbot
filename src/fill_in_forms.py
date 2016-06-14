# Google sheets
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


# selenium
import time
from selenium import webdriver
import requests
# Dickson
# import os
from keys import google_sheet_presets, selenium_presets
import random

SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CLIENT_SECRET_FILE = "keys/client_secret_oauth.json"
APPLICATION_NAME = 'Google Sheets API Python Quickstart'

def get_credentials():
	"""
	Gets valid user credentials from storage.

	If nothing has been stored, or if the stored credentials are invalid,
	the OAuth2 flow is completed to obtain the new credentials.

	Returns:
		Credentials, the obtained credential.
	"""
	home_dir = os.path.expanduser('~')
	credential_dir = os.path.join(home_dir, '.credentials')
	if not os.path.exists(credential_dir):
		os.makedirs(credential_dir)
	credential_path = os.path.join(
		credential_dir,
		'google-sheet-fill-in-forms-py.json')

	store = oauth2client.file.Storage(credential_path)
	credentials = store.get()
	if not credentials or credentials.invalid:
		flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
		flow.user_agent = APPLICATION_NAME
		if flags:
			credentials = tools.run_flow(flow, store, flags)
		else: # Needed only for compatibility with Python 2.6
			credentials = tools.run(flow, store)
		print('Storing credentials to ' + credential_path)
	return credentials

def getSpreadsheetValues(spreadsheetId, rangeName):
	credentials = get_credentials()
	http = credentials.authorize(httplib2.Http())

	discoveryUrl = 'https://sheets.googleapis.com/$discovery/rest?version=v4'
	service = discovery.build(
		'sheets',
		'v4',
		http = http,
		discoveryServiceUrl = discoveryUrl)
		# COLUMNS
	result = (service.spreadsheets().values().get(
		spreadsheetId = spreadsheetId,
		range = rangeName,
		majorDimension = "COLUMNS"
	)
		.execute())
	result.get('values', [])
	return result

def main():
	"""
	reads names from google sheet,
	uses selenium to open a chrome google.com
	input 5 random names from the sheet and search
	"""

	values = getSpreadsheetValues(google_sheet_presets.SHEET_ID, "C4:C29")
	print("sheet result:")
	print(values)

	chromedriver = selenium_presets.CHROME_DRIVER
	#os.environ["webdriver.chrome.driver"] = chromedriver
	driver = webdriver.Chrome(chromedriver)
	for i in range(5):
		randomName = random.choice (values["values"][0]);

		print(randomName);

		driver.get('http://www.google.com/xhtml');
		time.sleep(1) # Let the user actually see something!
		search_box = driver.find_element_by_id('gs_lc0')
		search_box = search_box.find_element_by_css_selector(".gsfi")
		search_box.send_keys("sc2 " + randomName)
		search_box.submit()
		time.sleep(3) # Let the user actually see something!

	time.sleep(3)
	driver.quit()

if __name__ == '__main__':
	main()
