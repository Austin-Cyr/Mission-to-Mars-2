from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

app = Flask(__name__)


# telling Python how to connect to Mongo using Pymongo
# # Use flask_pymongo to set up mongo connection
# teh below tells Python that our app will connect to Mongo using a URI, a uniform resource identifier similar to a URL.
#the URI we'll be using to connect our app to Mongo. This URI is saying that the app can reach Mongo through our localhost 
# server, using port 27017, using a database named "mars_app".
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# tells Flask what to display when we're looking at teh home page of index.html
@app.route("/")
# teh below sets up a function
def index():
   # uses PyMongo to find the "mars" collection in our database, which we will create when we convert our Jupyter \
   # scraping code to Python Script. We will also assign that path to the mars variable for use later.
   mars = mongo.db.mars_app.find_one()
   # tells Flask to return an HTML template using an index.html file. and mars=mars  tells Python to use the "mars" collection in MongoDB.
   return render_template("index.html", mars=mars)

@app.route("/scrape")
def scrape():
   # we assign a new variable that points to our Mongo database
   mars = mongo.db.mars_app
   # we created a new variable to hold the newly scraped data
   mars_data = scraping.scrape_all()
   print(mars_data)
   # update the db with this data --- upsert=True means to create a new document if one doesn't already exist
   mars.update({}, mars_data, upsert=True)
   # This will navigate our page back to / where we can see the updated content.
   return redirect('/', code=302)

if __name__ == "__main__":
    app.run(debug=True, port=5001)