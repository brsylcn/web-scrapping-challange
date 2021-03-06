from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scraper_mars

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_data"
mongo = PyMongo(app)

@app.route("/")
def index():
    mars_data = mongo.db.mars_data.find_one()
    return render_template("index.html", mars_data=mars_data)

@app.route("/scrape")
def scrape():
    mars_data = scraper_mars.scrape()
    mongo.db.mars_data.update({}, mars_data, upsert=True)

    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)