# imports
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import sys

app = Flask(__name__)

#set up mongo connecton
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mars_news_app'
mongo = PyMongo(app)

@app.route('/')
def index():
    mars_news = mongo.db.mars_news.find_one()
    return render_template('index.html',mars_news=mars_news)

@app.route('/scrape')
def scraper():
    mars_news = mongo.db.mars_news
    mars_news_data = scrape_mars.scrape()
    mars_news.update({}, mars_news_data, upsert=True)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)