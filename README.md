# ski-monitor
This repo provides tools for interactive plotting of historic and forecast:
 - temperatures
 - windspeed
 - precipitation [rain or snow]
 - current snow depth
 
For a range of ski resorts (the default ones being the ones near me).

For a demo, see [this webapp](http://ski-monitor.herokuapp.com), which is deployed (for free) via [Heroku](http://heroku.com) (it's awesome).
 
If you'd like to set up something similar for yourself, see the [deployment section below](#deployment-to-heroku).
 
 ## Tech
This app uses:
 
 - the [Dash](https://plot.ly/dash/getting-started) package from Plotly for plotting + serving the webapp
 - the [DarkSky API](https://darksky.net/dev) for current and forecast weather
 - [OnTheSnow](https://www.onthesnow.com) + [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) for scraping current snow conditions
 - [Heroku](http://heroku.com) for deployment, which also gives us:
    - a [Postgres database](https://devcenter.heroku.com/articles/heroku-postgresql) to store data
    - a [Scheduler](https://devcenter.heroku.com/articles/scheduler) to update our database + scraped data once an hour
    - gunicorn for more robust serving than Flask provides
    
## Setup

### Requirements

Create a virtual environment with whatever framework takes your fancy (e.g. Conda or Virtualenv).

Now install the requirements:
```bash
pip install -r requirements.txt

```
You'll also need to visit [DarkSky](https://darksky.net/dev) and get your API key. Once you've done that, run

```bash
export DARKSKY_KEY=<your DarkSky API key>
```

To check everything is tickety-boo, run the tests:

```bash
pytest tests.py
```
### To run the web-app locally

To use the app, you'll need to create a  Postgres database somewhere. I'd strongly recommend [Heroku](https://www.heroku.com/postgres).

Once you've got a Postgres database setup, you'll need to export the `DATABASE_URL` for your database.

This is automaticaly set in Heroku and you can find it in the settings for your app.
```bash
export DATABASE_URL=<your database URL>
```

Now you're ready to run your app:
```bash
python app.py

```

This should return a URL which you can refer to for lovely JS graphs.

## Deployment to Heroku 

If you've never used Heroku before, check out their [Getting Started](https://devcenter.heroku.com/start) guide.

However, this repo is provisioned to work out-of-the-box, so you only really need to:

- Create a new project in Heroku
- Use the Postgres DB add-on to create a new database
- Use the Heroku Scheduler add-on to schedule the database updates every hour, with:

    ```python db_utils.py```
    
- Deploy the contents of this Git Repo to Heroku, by selecting the 'Deploy with Git' option under your project's deployment settings
## Contents

[app.py](/app.py): the web app itself, defining which graphs are plotted

[constants.py](/constants.py): definitions of the GPS co-ordinates and OnTheSnow URL's for each ski resport

[darksky.py](/darksky.py): tools for calling the darksky API and returning pandas dataframe

[db_utils.py](/db_utils.py): tools for interacting with the Postgres database. When called from the command line (i.e. `python db_utils.py`), this updates the database with calls to the Darksky API.

[plotting.py](/plotting.py): tools for plotting wih Dash/Plotly

[scraping.py](/scraping.py): tools for scraping snow conditions from OnTheSnow

[tests.py](/tests.py): minimal tests

[Procfile](/Procfile): Procfile instructing Heroku how to run the app (using gunicorn)


 