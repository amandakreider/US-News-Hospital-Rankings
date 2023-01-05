# US News Hospital Rankings

I wrote these Python scripts to scrape hospital data and rankings from the [U.S. News & World Report website](https://health.usnews.com/best-hospitals). The code is easily modifiable to generate data for any combination of specialty and place in the United States. The output data are saved as .csv files in the [data directory](https://github.com/amandakreider/US-News-Hospital-Rankings/tree/main/data).

## Steps:

1. Input local directory and the specialty you wish to scrape rankings for at the top of scripts/usnews_spec_ranks.py
   - I will add a listing of specialties later for convenience.
2. Input local directory and the place (state, region, or city) you wish to scrape rankings for at the top of scripts/usnews_local_ranks.py
3. Run scripts/usnews_spec_ranks.py to create specialty rankings 
   - This script scrapes *all* rankings for the given specialty at the national level.
4. Run scripts/usnews_local_ranks.py to create hospital rankings for a local area (state, region, or city)
   - This script also merges in the specialty data created in step #1.


