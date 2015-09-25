import os
import sys
import csv
from home import db, Home

# Create our tables 
db.create_all()

print "Starting to parse file into database"
# Open our csv file and load data into our table
with open(os.path.dirname(os.path.abspath(__file__)) + '/data/listings.csv', 'rb') as f:
    listings = csv.reader(f, delimiter=',')

    # Skip Header
    next(listings, None)
    for listing in listings:
        try:
            home = Home(listing[0], listing[1], listing[2], listing[3], listing[4], listing[5], listing[6], listing[7], listing[8])
            db.session.add(home)
        except Exception, e:
            print ("Unable to read file properly. Exiting with error: %s" % (e))
            sys.exit(0)

    db.session.commit()
    print "Successfully created database"
