# EasyLend Server

## Important Points:

- To run it please take a close look at `server/settings-sample.py` file. You'll need to modify the credentials for your setup and rename it to `settings.py`. 
- If you're running it locally with a local PostgreSQL setup, make sure you set an environment variable `LOCAL_DATABASE`. Set it to whatever you like. It just needs to exist. I deployed it on Google App Engine hence the `GAE_` checks in the settings file. You can deploy it wherever you like and change the settings file accordingly. 