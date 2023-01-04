import requests
import json
from bs4 import BeautifulSoup as bs
import pandas as pd
import os
from pathlib import Path

# Define city
searchcity = 'Philadelphia, PA'

# Define url
usn_url = 'https://health.usnews.com'

# Define headers
hdr = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0'
}

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
common_cares = []
high_perf_adult = []
national_ranks_adult = []
national_ranks_peds = []

for p in range(1, 10):

	pagestr = str(p)

	url = 'https://health.usnews.com/best-hospitals/search-data?city='+searchcity+'&page='+pagestr

	# Pull in json data from url
	r = requests.get(url, headers=hdr)
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

		metro_name = matches[h]['regional']['metro_area']['name']
		metro_names.append(metro_name)

		metro_recognized = matches[h]['regional']['metro_area']['is_recognized_in']
		metro_rec.append(metro_recognized)

		metro_rank = matches[h]['regional']['metro_area']['rank']
		metro_ranks.append(metro_rank)

		metro_tied = matches[h]['regional']['metro_area']['is_tied']
		metro_tied_flags.append(metro_tied)

		common_care_ratings = matches[h]['common_care_ratings']
		common_cares.append(common_care_ratings)

		high_performing_adult_specialties = matches[h]['high_performing_adult_specialties']
		high_perf_adult.append(high_performing_adult_specialties)

		national_rankings_adult = matches[h]['national_rankings']['adult']
		national_ranks_adult.append(national_rankings_adult)

		national_rankings_peds = matches[h]['national_rankings']['pediatric']
		national_ranks_peds.append(national_rankings_peds)

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
df['Metro'] = metro_names
df['Recognized in Metro'] = metro_rec
df['Metro Rank'] = metro_ranks
df['Tied?'] = metro_tied_flags
df['# of High Performing Adult Specialties'] = high_perf_adult
df['# of National Rankings (Adult)'] = national_ranks_adult
df['# of National Rankings (Pediatrics)'] = national_ranks_peds

df.drop_duplicates()

# Save CSV 

#directory = '/mnt/c/Users/akreid/iCloudDrive/Documents/GitHub/usnews/csv/'
directory = str(Path(__file__).parent.parent) + "/csv/"
print("csv file will be generated at ", directory)
df.to_csv(directory+'hosp_rankings_phila_pa.csv')





