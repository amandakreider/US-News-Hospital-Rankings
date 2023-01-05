import requests
import json
from bs4 import BeautifulSoup as bs
import pandas as pd
import os
from pathlib import Path
from datetime import date, datetime, timedelta
import time

# Input specialty code
specialty = 'IHQCANC' # this is the US News specialty code for cancer care

# Input directory where you want datafiles to be stored
#directory = 'c/Users/username/Documents/usnews/data/' 
directory = str(Path(__file__).parent.parent) + "/data/"

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
spec_ranks = []
spec_rank_tied_flags = []
spec_rank_revoked_flags = []
spec_rank_spec_ids = []
spec_rank_types = []
spec_scores = []
updated = []

# Scrape specialty rankings

for p in range(1, 999):

	time.sleep(1)

	pagestr = str(p)

	# URL:
	url = 'https://health.usnews.com/best-hospitals/search-data?specialty_id='+specialty+'&page='+pagestr

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
				spec_rank = matches[h]['ranking']['rank']
			except KeyError:
				spec_rank = None
			spec_ranks.append(spec_rank)

			try: 
				spec_rank_tied = matches[h]['ranking']['is_tied']
			except KeyError:
				spec_rank_tied = None
			spec_rank_tied_flags.append(spec_rank_tied)

			try:
				spec_rank_revoked = matches[h]['ranking']['is_revoked']
			except KeyError:
				spec_rank_revoked = None
			spec_rank_revoked_flags.append(spec_rank_revoked)

			spec_rank_specialty_id = matches[h]['ranking']['specialty_id']
			spec_rank_spec_ids.append(spec_rank_specialty_id)

			spec_rank_type = matches[h]['ranking']['type']
			spec_rank_types.append(spec_rank_type)

			spec_score = matches[h]['scores'][0]['score']
			spec_scores.append(spec_score)

			updated.append(timestamp)

	else:

		print('No page')
		break

print('Create a data file with specialty ranking data')
# Create a data file with specialty ranking data
df = pd.DataFrame()

df['Name (Specialty)'] = names
df['AHA ID'] = aha_ids
df['Hospital ID'] = hospital_ids
df['Specialty ID'] = spec_rank_spec_ids
df['Specialty Score'] = spec_scores
df['Specialty Ranking'] = spec_ranks
df['Specialty Ranking Tied?'] = spec_rank_tied_flags
df['Specialty Ranking Revoked?'] = spec_rank_revoked_flags
df['Specialty Ranking Type'] = spec_rank_types
df['Updated'] = updated

df = df.drop_duplicates()

# Save CSV and pickle files

print("csv and pickle files will be generated at ", directory)
df.to_csv(directory+'spec_hosp_rankings.csv')
df.to_pickle(directory+'spec_hosp_rankings.pkl')

