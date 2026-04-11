# US News Hospital Rankings

I wrote these Python scripts to scrape hospital data and rankings from the [U.S. News & World Report website](https://health.usnews.com/best-hospitals). The code is easily modifiable to generate data for any combination of specialty and place in the United States. The output data are saved as .csv files in the [data directory](https://github.com/amandakreider/US-News-Hospital-Rankings/tree/main/data).

## Setup

### 1. Create and activate a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set environment variables

The scripts use the `MY_UA` environment variable to set a custom HTTP User-Agent for requests. If this variable is not set, the default `requests` library User-Agent will be used. To set it:

```bash
export MY_UA="your-user-agent-string"        # macOS/Linux
set MY_UA="your-user-agent-string"           # Windows Command Prompt
$env:MY_UA="your-user-agent-string"          # Windows PowerShell
```

## Steps

1. Input local directory and the specialty you wish to scrape rankings for at the top of [usnews_spec_ranks.py](https://github.com/amandakreider/US-News-Hospital-Rankings/blob/main/scripts/usnews_spec_ranks.py)
   - I will add a listing of specialties later for convenience.
2. Input local directory and the place (state, region, or city) you wish to scrape rankings for at the top of [usnews_local_ranks.py](https://github.com/amandakreider/US-News-Hospital-Rankings/blob/main/scripts/usnews_local_ranks.py)
3. Run [usnews_spec_ranks.py](https://github.com/amandakreider/US-News-Hospital-Rankings/blob/main/scripts/usnews_spec_ranks.py) to create specialty rankings
   - This script scrapes *all* rankings for the given specialty at the national level.
4. Run [usnews_local_ranks.py](https://github.com/amandakreider/US-News-Hospital-Rankings/blob/main/scripts/usnews_local_ranks.py) to create hospital rankings for a local area (state, region, or city)
