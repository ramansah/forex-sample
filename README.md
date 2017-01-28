# forex-sample

To start project - (prefer virtualenv)

Install MySQL server

Initialize DB
python forex.db.py

cd forex-sample
pip install -r requirements.txt
gunicorn forex.rest_api:api

Load data from web scraper
python forex.scraper.py

Go to http://localhost/forex
