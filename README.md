# ski-monitor
This repo provides tools for interactive plotting of historic and forecast:
 - temperatures
 - windspeed
 - precipitation [rain or snow]
 - current snow depth
 
 For a range of ski resorts (the default ones being the ones near me).
 
 ## Tech
This repo uses:
 
 - the Dash package from Plotly for plotting + serving the webapp
 - the DarkSky API for current and forecast weather
 - onthesnow.com + BeautifulSoup for scraping current snow conditions
 - Heroku for deployment, which also gives us:
    - a postgres database to store data
    - a scheduler to update our database + scraped data once an hour
    - gunicorn for more robust serving than Flask provides
    
## Setup

### Requirements

```buildoutcfg
pip install -r requirements.txt
```

## Files

[app.py](/app.py): the web app itself, defining which graphs are plotted

[constants.py](/constants.py): definitions of the GPS co-ordinates and OnTheSnow URL's for each ski resport

[darksky.py](/darksky.py): tools for calling the darksky API and returning pandas dataframe

[db_utils.py](/db_utils.py): tools for interacting with the Postgres database

[plotting.py](/plotting.py): tools for plotting wih Dash/Plotly

[scraping.py](/scraping.py): tools for scraping snow conditions from OnTheSnow

[tests.py](/tests.py): minimal tests

[Procfile](/Procfile): Procfile instructing Heroku how to run the app (using gunicorn)


 