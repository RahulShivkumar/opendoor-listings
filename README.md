#![alt tag](https://github.com/RahulShivkumar/opendoor-listings/blob/master/opendoor_awesome.png)

Opendoor Engineering Problem is written in Python using Flask & Postgresql as a datastore. SQLAlchemy is used as an ORM and the whole application is deployed on Heroku.

Live version of this app can be found at - https://opendoor-listings-1000.herokuapp.com/listings

Try using a JSON Formatter browser extension to format the output in your browser.

##Setup
Clone this project using -
```
git clone https://github.com/RahulShivkumar/opendoor-listings.git
```

Download the requirements using -
```
pip install -r requirements.txt
```

To run this application, you first need to setup the database and load it with data.

Set the location of your database in home.py(opendoor_listings/models/home.py). The current setup is for heroku in production, so you need to change this line to something like this
```
app.config['SQLALCHEMY_DATABASE_URI'] = postgresql://localhost/opendoor_listing
```

populate_script.py(opendoor_listings/models/populate_script.py) sets up the tables and loads with data from listings.csv
Run it using ```py populate_script.py``` within the models folder.

Once the data is setup, you can run ```py runserver.py``` that will start the server on local host port 5000 (http://127.0.0.1:5000/).

##Setup Using Heroku
I used Heroku to deploy this application. Create a Heroku account [here](signup.heroku.com).

Once an account is created, you can download Heroku's Toolbelt [here](https://toolbelt.heroku.com/).

Login to your heroku account using -
```
heroku login
``` 

Create a new app called opendoor_listings from the first directory using -
```
heroku create opendoor-listings-1000
```

Once the app is created, go to your heroku dashboard (https://dashboard.heroku.com/) and select opendoor_listings. Create a new Postgresql add on for the application. This ensures that you have a datastore when you deploy the application to heroku (The address to which is stored as os.environ['DATABASE_URL']).

Just as in the previous setup, you first have to run populate_scripts.py to create the tables and load the data. The Procfile in the project tells Heroku to run populate_scripts.py after the app is pushed to it. You can push the app to heroku using 
```
git push heroku
```

populate_scripts.py should have run and the data should be in the database. You can check if the script ran correctly by checking the heroku logs using ```heroku logs --tail```. If the output doesn't show any exceptions, the tables have been created and the data is in there!

Now, change the Procfile using your favorite editor to -
```
web: python runserver.py
```
This tells Heroku to run runserver.py.

Commit this change and push it to heroku ```git push heroku```.

Run the following command to allocate dynos.
```
heroku ps:scale web=1
```


Now run 
```
heroku open
```
This will open the app in your browser. Add a /listings to the url to see all the house listings! Add the get parameters to see specific ones.


##Time Taken
I timed myself while writing this application. It took me 3 hours and 15 minutes to build this app and deploy it. About an hour and 15 minutes went into deploying the app on Heroku since I had never used it before. I could have built it faster without proper error handling but I'm a pretty defensive programmer so I thought some good error handling and tests would be worth the time invested. 

##Things Learnt 
Using Heroku - I really like the service and will definitely use it again for some future project. 

GeoJson - Never heard of GeoJson before but it was cool plugging the results into geojson.io and seeing all the houses on a map!

##References 
[Flask SQLAlchemy](https://pythonhosted.org/Flask-SQLAlchemy/)

[Heroku](www.heroku.com)









