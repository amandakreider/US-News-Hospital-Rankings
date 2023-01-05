import requests
import json
from bs4 import BeautifulSoup as bs
import pandas as pd
import os
from pathlib import Path
from datetime import date, datetime, timedelta
import time
import pprint

pp = pprint.PrettyPrinter(indent=4)

# Define city
searchcity = 'Low Country'

# Define url
usn_url = 'https://health.usnews.com'

# Define headers
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

# First gather cancer rankings

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

			pp.pprint(matches[h])	

			aha_id = matches[h]['aha_id']
			aha_ids.append(aha_id)

			hospital_id = matches[h]['hospital_id']
			hospital_ids.append(hospital_id)

			cancer_rank = matches[h]['ranking']['rank']
			cancer_ranks.append(cancer_rank)

			cancer_rank_tied = matches[h]['ranking']['is_tied']
			cancer_rank_tied_flags.append(cancer_rank_tied)

			cancer_rank_revoked = matches[h]['ranking']['is_revoked']
			cancer_rank_revoked_flags.append(cancer_rank_revoked)

			cancer_rank_specialty_id = matches[h]['ranking']['specialty_id']
			cancer_rank_spec_ids.append(cancer_rank_specialty_id)

			cancer_rank_type = matches[h]['ranking']['type']
			cancer_rank_types.append(cancer_rank_type)

			cancer_score = matches[h]['scores'][0]['score']
			cancer_scores.append(cancer_score)

	else:

		print('No page')
		break

print('Create a csv file with cancer ranking data')
# Create a csv file with cancer ranking data
canc_df = pd.DataFrame()

canc_df['Name'] = names
canc_df['AHA ID'] = aha_ids
canc_df['Hospital ID'] = hospital_ids
canc_df['Cancer Ranking'] = cancer_ranks
canc_df['Cancer Ranking Tied?'] = cancer_rank_tied_flags
canc_df['Cancer Ranking Revoked?'] = cancer_rank_revoked_flags
canc_df['Cancer Ranking Specialty ID'] = cancer_rank_spec_ids
canc_df['Cancer Ranking PrettyPrinter'] = cancer_rank_types
canc_df['Cancer Care Score'] = cancer_scores

df.drop_duplicates()

# Save CSV 

directory = '/mnt/c/Users/akreid/iCloudDrive/Documents/GitHub/usnews/csv/'
#directory = str(Path(__file__).parent.parent) + "/csv/"
print("csv file will be generated at ", directory)
df.to_csv(directory+'cancer_hosp_rankings.csv')

# Initiate lists 
names = []
aha_ids = []
hospital_ids = []
addresses = []
cities = []
states = []
state_abbrevs = []
zips = []
lats = []
longs = []
input_locations = []
input_location_dists = []
phones = []
urls = []
metro_names = []
metro_rec = []
metro_ranks = []
metro_tied_flags = []
region_names = []
region_rec = []
region_ranks = []
region_tied_flags = []
state_rec = []
state_ranks = []
state_tied_flags = []
high_perf_adult = []
national_ranks_adult = []
national_ranks_peds = []
updated = []

for p in range(1, 999):

	time.sleep(1)

	pagestr = str(p)

	# Regional rankings url:
	url = 'https://health.usnews.com/best-hospitals/search-data?city='+searchcity+'&page='+pagestr

	# Cancer rank url: 
	# 'https://health.usnews.com/best-hospitals/search-data?specialty_id=IHQCANC&page=3'

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

			pp.pprint(matches[h])	

			aha_id = matches[h]['aha_id']
			aha_ids.append(aha_id)

			hospital_id = matches[h]['hospital_id']
			hospital_ids.append(hospital_id)

			address = matches[h]['location']['address']
			addresses.append(address)

			city = matches[h]['location']['city']
			cities.append(city)

			state = matches[h]['location']['state']['name']
			states.append(state)

			state_abbrev = matches[h]['location']['state']['abbreviation']
			state_abbrevs.append(state_abbrev)

			zip_code = matches[h]['location']['zip_code']
			zips.append(zip_code)

			latitude = matches[h]['location']['geolocation']['lat']
			lats.append(latitude)

			longitude = matches[h]['location']['geolocation']['lon']
			longs.append(longitude)

			input_location = matches[h]['input_location']
			input_locations.append(input_location)

			input_location_distance = matches[h]['input_location_distance']
			input_location_dists.append(input_location_distance)

			phone = matches[h]['phone']
			phones.append(phone)

			url = usn_url+matches[h]['url']
			urls.append(url)

			try:
				state_recognized = matches[h]['regional']['state']['is_recognized_in']
			except KeyError:
				state_recognized = None
			state_rec.append(state_recognized)

			try:
				state_rank = matches[h]['regional']['state']['rank']
			except KeyError:
				state_rank = None
			state_ranks.append(state_rank)

			try:
				state_tied = matches[h]['regional']['state']['is_tied']
			except KeyError:
				state_tied = None
			state_tied_flags.append(state_tied)

			try:
				region_name = matches[h]['regional']['region']['name']
			except KeyError:
				region_name = ''
			region_names.append(region_name)

			try:
				region_recognized = matches[h]['regional']['region']['is_recognized_in']
			except KeyError:
				region_recognized = None
			region_rec.append(region_recognized)

			try:
				region_rank = matches[h]['regional']['region']['rank']
			except KeyError:
				region_rank = None
			region_ranks.append(region_rank)

			try:
				region_tied = matches[h]['regional']['region']['is_tied']
			except KeyError:
				region_tied = None
			region_tied_flags.append(region_tied)

			try:
				metro_name = matches[h]['regional']['metro_area']['name']
			except KeyError:
				metro_name = ''
			metro_names.append(metro_name)

			try:
				metro_recognized = matches[h]['regional']['metro_area']['is_recognized_in']
			except KeyError:
				metro_recognized = None
			metro_rec.append(metro_recognized)

			try:
				metro_rank = matches[h]['regional']['metro_area']['rank']
			except KeyError:
				metro_rank = None
			metro_ranks.append(metro_rank)

			try:
				metro_tied = matches[h]['regional']['metro_area']['is_tied']
			except KeyError:
				metro_tied = None
			metro_tied_flags.append(metro_tied)

			high_performing_adult_specialties = matches[h]['high_performing_adult_specialties']
			high_perf_adult.append(high_performing_adult_specialties)

			national_rankings_adult = matches[h]['national_rankings']['adult']
			national_ranks_adult.append(national_rankings_adult)

			national_rankings_peds = matches[h]['national_rankings']['pediatric']
			national_ranks_peds.append(national_rankings_peds)

			updated.append(timestamp)

	else:

		print('No page')
		break

print('Create a csv file with hospital data')
# Create a csv file with hospital data
df = pd.DataFrame()

df['Name'] = names
df['AHA ID'] = aha_ids
df['Hospital ID'] = hospital_ids
df['Address'] = addresses
df['City'] = cities
df['State Name'] = states
df['State Abbrev'] = state_abbrevs
df['Zip Code'] = zips
df['Latitude'] = lats 
df['Longitude'] = longs
df['Search Location'] = input_locations
df['Distance from Search Location'] = input_location_dists
df['Phone'] = phones
df['URL'] = urls
df['Recognized in State'] = state_rec
df['State Rank'] = state_ranks
df['Tied in State?'] = state_tied_flags
df['Region'] = region_names
df['Recognized in Region'] = region_rec
df['Region Rank'] = region_ranks
df['Tied in Region?'] = region_tied_flags
df['Metro'] = metro_names
df['Recognized in Metro'] = metro_rec
df['Metro Rank'] = metro_ranks
df['Tied in Metro?'] = metro_tied_flags
df['# of High Performing Adult Specialties'] = high_perf_adult
df['# of National Rankings (Adult)'] = national_ranks_adult
df['# of National Rankings (Pediatrics)'] = national_ranks_peds
df['Updated'] = updated

df.drop_duplicates()

# Save CSV 

directory = '/mnt/c/Users/akreid/iCloudDrive/Documents/GitHub/usnews/csv/'
#directory = str(Path(__file__).parent.parent) + "/csv/"
print("csv file will be generated at ", directory)
df.to_csv(directory+'hosp_rankings_lowcountry.csv')





