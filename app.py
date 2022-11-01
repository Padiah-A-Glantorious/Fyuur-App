#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from ast import keyword
import json
from re import A
import dateutil.parser
from datetime import datetime
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
#from flask_session import Session
from flask_marshmallow import Marshmallow

import os

# I have installed Marshmallow-sqlAlchemy aswell as flask-marshmallow

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:Traprusty@localhost:5432/fyuur'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
moment = Moment(app)
app.config['SESSION_TYPE'] = 'filesystem'
PERMANENT_SESSION_LIFETIME = 1800
app.config.update(SECRET_KEY=os.urandom(24))
app.config.from_object(__name__)
#Session(app)
#app.config.from_object('config')

db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app,db)



# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    website_link =db.Column(db.String(130))
    seeking_talent =db.Column(db.String(120))
    seeking_description = db.Column(db.String(200))
    shows = db.relationship('Show', backref='venue', lazy=False)
    

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link=db.Column(db.String(120))
    seeking_venue =db.Column(db.String(120))
    seeking_description =db.Column(db.String(120))
    shows = db.relationship('Show', backref='artist', lazy=False)
 
    

class Show(db.Model):
  __tablename__ = 'show'
  id = db.Column(db.Integer, primary_key=True)
  artist_id = db.Column(db.Integer, db.ForeignKey("Artist.id"), nullable=False)
  venue_id = db.Column(db.Integer, db.ForeignKey("Venue.id"), nullable=False)
  start_time = db.Column(db.DateTime, nullable=False)
    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.



#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():

  # TODO: replace with real venues data.
  #       num_futureShows should be aggregated based on number of upcoming shows per venue.
  
  #num_shows should be aggregated based on number of upcoming shows per venue.
  
  response = Venue.query.order_by('city', 'state', 'name').all()
  json_response = {}
  arr = []
  for i in range(len(response.venue)):
      json_response ={
        "id" : response.venue[i].id,
        "name" : response.venue[i].name
      }
      arr+=json_response
  
  

  return render_template('pages/venues.html', areas=arr)
 
 # data2 = db.session.query(Venue)
 
  

 # return render_template('pages/venues.html', areas=data2)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  results_array = []
  keyword = request.form.get('search_term')
  Database_response = Venue.query.filter(Venue.name.match(keyword)).order_by('name').all()
  for i in Database_response:
    Json_Arr = {
      "id": i.id,
      "name": i.name,
      "num_upcoming_shows": len(i.shows)
    }


    results_array.append(Json_Arr)

  response={
    "count": len(results_array),
    "data": results_array
  }

  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  
  response = Venue().query.filter(Venue.id==venue_id).first()
  print(response)
  #data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
  return render_template('pages/show_venue.html', venue=response)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  form = VenueForm()
  name=request.form['name']
  city=request.form['city']
  state=request.form['state'] 
  address=request.form['address']
  phone=request.form['phone']
  genres=request.form['genres']
  facebook_link=request.form['facebook_link']
  image_link=request.form['image_link']
  website_link=request.form['facebook_link']
  seeking_talent=request.form['seeking_talent']
  seeking_description =request.form['seeking_description']
  
  new_venue = Venue(name=name,city=city,state=state,address=address,phone=phone,image_link=image_link,facebook_link=facebook_link,genres=genres,website_link=website_link,seeking_talent=seeking_talent,seeking_description=seeking_description)

  db.session.add(new_venue)
  db.session.commit()

  
  def __repr__(self):
    return f'<create_venue_form  {self.name} {self.city} {self.state} {self.address} {self.phone} {self.genres} {self.fb_link} {self.img_link} {self.website} {self.seeking_talent} {self.description}>'
  

  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  #flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed in the database.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage

  query = Venue.query.filter_by(id=venue_id).delete()
  db.session.add(query)
  db.session.commit()
  flash('Venue ' + request.form['name'] + ' was successfully Deleted')
  return render_template('pages/home.html')

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  response = Artist().query.all()
  return render_template('pages/artists.html', artists=response)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  results_array = []
  keyword = request.form.get('search_term')
  Database_response = Artist.query.filter(Artist.name.match(keyword)).order_by('name').all()
  for i in Database_response:
    Json_Arr = {
      "id": i.id,
      "name": i.name,
      "num_upcoming_shows": len(i.shows)
    }
    results_array.append(Json_Arr)
  results={
    "count": len(results_array),
    "data": results_array
  }
  
  return render_template('pages/search_artists.html', results=results, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  futureShows = []
  PrevShows = []
  response = Artist.query.filter_by(id=artist_id).first()
  response.genres = json.dumps(response.genres)
  for show in response.shows:
    if show.start_time > datetime.now():
      futureShows.append(show)
    else:
      PrevShows.append(show)
  response.futureShows = list(futureShows)
  response.PrevShows = list(PrevShows)
  #data = list(filter(lambda d: d['id'] == artist_id, response))[0]
  return render_template('pages/show_artist.html', artist=response)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'] )
def edit_artist(artist_id):
  form = ArtistForm()

  results = Artist.query.filter_by(id=artist_id).first()
  form.name.data = results.name
  form.city.data = results.city
  form.state.data = results.state
  form.phone.data = results.phone
  form.facebook_link.data = results.facebook_link
  form.website_link.data = results.website_link
  form.image_link.data = results.image_link
  form.genres.data = json.dumps(results.genres)
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=results)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  results = Artist.query.filter_by(id=artist_id).first()
  request_data = request.get_json()
  results.name = request_data['name']
  results.city = request_data['city']
  results.state = request_data['state']
  results.phone = request_data['phone']
  results.genres = json.dumps(request_data['genres'])
  results.facebook_link = request_data['facebook_link']
  results.website_link = request_data['website_link']
  results.image_link = request_data['image_link']

  db.session.commit()
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
 
  response=Venue().query.filter(Venue.id==venue_id).first()

  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=response)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  name=request.form['name']
  city=request.form['city']
  state=request.form['state'] 
  phone=request.form['phone']
  genres=request.form['genres']
  facebook_link=request.form['facebook_link']
  image_link=request.form['image_link']
  website_link=request.form['facebook_link']
  seeking_venue =request.form['seeking_venue']
  seeking_description =request.form['seeking_description']
  new_artist = Artist(name=name,city=city,state=state,phone=phone,image_link=image_link,facebook_link=facebook_link,genres=genres,website_link=website_link,seeking_venue=seeking_venue,seeking_description=seeking_description)
  db.session.add(new_artist)
  db.session.commit() 
  # on successful db insert, flash success
  flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  
  response = []
  query =db.session.query(Show, Artist, Venue)
  results = query.join(Artist).join(Venue).filter(Show.start_time > datetime.now()).order_by('start_time').all()
  for i in range(len(results)):
    return_value = {
      'venue_id': results[i].Venue.id,
      'artist_id': results[i].Artist.id,
      'venue_name': results[i].Venue.name,
      'artist_name': results[i].Artist.name,
      'artist_image_link': results[i].Artist.image_link,
      'start_time': results[i].Show.start_time.strftime('%Y-%m-%d %H:%I')
    }
    response.append(return_value)


  return render_template('pages/shows.html', shows=response)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  venue = request.form['venue_id']
  artist = request.form['artist_id']
  time = request.form['start_time']
  new_show = Show(venue_id=venue,artist_id=artist,start_time=time)
  db.session.add(new_show)
  db.session.commit()
  # on successful db insert, flash success
  flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#
db.create_all()
db.session.commit() 

# Default port:
if __name__ == '__main__':
    app.debug=True
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
