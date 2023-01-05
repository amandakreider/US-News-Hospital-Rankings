import requests
import json
from bs4 import BeautifulSoup as bs
import pandas as pd
import os
from pathlib import Path
from datetime import date, datetime, timedelta
import time

# Input directory where you want datafiles to be stored
directory = '/mnt/c/Users/akreid/iCloudDrive/Documents/GitHub/usnews/data/' 
#directory = str(Path(__file__).parent.parent) + "/data/"

# Definitions 
usn_url = 'https://health.usnews.com'
hdr = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0'
}

# Timestamp
timestamp = datetime.now()
print(timestamp)

# Initiate lists
names = []
aha_ids = []
hospital_ids = []
cancer_ranks = []
cancer_rank_tied_flags = []
cancer_rank_revoked_flags = []
cancer_rank_spec_ids = []
cancer_rank_types = []
cancer_scores = []
updated = []

# Scrape cancer rankings

for p in range(1, 999):

	time.sleep(1)

	pagestr = str(p)

	# Cancer rank url: 
	url = 'https://health.usnews.com/best-hospitals/search-data?specialty_id=IHQCANC&page='+pagestr

	# Pull in json data from url
	r = requests.get(url, headers=hdr)
	print(r.status_code)

	if r.status_code != 204 and r.status_code != 404:

		soup = bs(r.content, "html.parser")
		json_data = soup.text
		data = json.loads(json_data)

		matches = data['matches']

		for h in range(len(data['matches'])):

			# Get hospital data
			name = matches[h]['name']
			names.append(name)

			print('Working on hospital: '+name)

			aha_id = matches[h]['aha_id']
			aha_ids.append(aha_id)

			hospital_id = matches[h]['hospital_id']
			hospital_ids.append(hospital_id)


			try:
				cancer_rank = matches[h]['ranking']['rank']
			except KeyError:
				cancer_rank = None
			cancer_ranks.append(cancer_rank)

			try: 
				cancer_rank_tied = matches[h]['ranking']['is_tied']
			except KeyError:
				cancer_rank_tied = None
			cancer_rank_tied_flags.append(cancer_rank_tied)

			try:
				cancer_rank_revoked = matches[h]['ranking']['is_revoked']
			except KeyError:
				cancer_rank_revoked = None
			cancer_rank_revoked_flags.append(cancer_rank_revoked)

			cancer_rank_specialty_id = matches[h]['ranking']['specialty_id']
			cancer_rank_spec_ids.append(cancer_rank_specialty_id)

			cancer_rank_type = matches[h]['ranking']['type']
			cancer_rank_types.append(cancer_rank_type)

			cancer_score = matches[h]['scores'][0]['score']
			cancer_scores.append(cancer_score)

			updated.append(timestamp)

	else:

		print('No page')
		break

print('Create a data file with cancer ranking data')
# Create a data file with cancer ranking data
df = pd.DataFrame()

df['Name'] = names
df['AHA ID'] = aha_ids
df['Hospital ID'] = hospital_ids
df['Cancer Ranking'] = cancer_ranks
df['Cancer Ranking Tied?'] = cancer_rank_tied_flags
df['Cancer Ranking Revoked?'] = cancer_rank_revoked_flags
df['Cancer Ranking Specialty ID'] = cancer_rank_spec_ids
df['Cancer Ranking PrettyPrinter'] = cancer_rank_types
df['Cancer Care Score'] = cancer_scores
df['Updated'] = updated

df.drop_duplicates()

# Save CSV and pickle files

print("csv and pickle files will be generated at ", directory)
df.to_csv(directory+'cancer_hosp_rankings.csv')
df.to_pickle(directory+'cancer_hosp_rankings.pkl')

