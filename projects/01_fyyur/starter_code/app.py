#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from datetime import date
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# TODO: connect to a local postgresql database
migrate = Migrate(app, db)

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

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    genres = db.Column(db.String())
    website_link = db.Column(db.String(120))
    past_shows_count = db.Column(db.Integer)
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(120))

    shows_venue = db.relationship('Show', backref='venue')


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

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    website_link = db.Column(db.String(120))
    upcoming_shows_count = db.Column(db.Integer)
    past_shows_count = db.Column(db.Integer)
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(200))

    shows_artist = db.relationship('Show', backref='artist')


# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

class Show(db.Model):
    __tablename__ = 'Show'
    venue_id = db.Column(db.Integer, db.ForeignKey(
        'Venue.id'), primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey(
        'Artist.id'), primary_key=True)
    start_time = db.Column(db.String(25), nullable=False)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


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
    #       num_shows should be aggregated based on number of upcoming shows per venue.

    # a part of this code was a help from mintor I found on udacity knowledge
    areas = Venue.query.distinct('city', 'state').all()
    data = []
    for area in areas:
        venues = Venue.query.filter(
            Venue.city == area.city, Venue.state == area.state).all()
        record = {
            'city': area.city,
            'state': area.state,
            'venues': [{
                "id": venue.id,
                "name": venue.name,
                "num_upcoming_shows": Show.query.filter_by(venue_id=venue.id).count()
            } for venue in venues],
        }
        data.append(record)

    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

    data = request.form
    print(data['search_term'])
    venues = Venue.query.filter(
        Venue.name.ilike('%' + data['search_term'] + '%')).all()
    print(venues)

    response = {
        "count": len(venues),
        "data": [{
            "id": venue.id,
            "name": venue.name,
            "num_upcoming_shows": Show.query.filter_by(venue_id=venue.id).count()
        } for venue in venues]
    }

    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id

    venue = Venue.query.filter_by(id=venue_id).first()
    # formate geners to be list of strings
    genres = venue.genres.translate(
        str.maketrans('', '', '{ }')).split(",")

    shows = Show.query.filter_by(venue_id=venue_id).all()

    now = datetime.now()
    past_shows = []
    upcoming_shows = []
    for show in shows:
        show_date_formatted = datetime.strptime(
            show.start_time, '%Y-%m-%d %H:%M:%S')
        if show_date_formatted > now:
            artist = Artist.query.filter_by(id=show.artist_id).first()
            upcoming_shows.append({
                "artist_id": show.artist_id,
                "artist_name": artist.name,
                "artist_image_link": artist.image_link,
                "start_time": show.start_time
            })
        else:
            artist = Artist.query.filter_by(id=show.artist_id).first()
            past_shows.append({
                "artist_id": show.artist_id,
                "artist_name": artist.name,
                "artist_image_link": artist.image_link,
                "start_time": show.start_time
            })

    data = {
        "id": venue.id,
        "name": venue.name,
        "genres": genres,
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": venue.website_link,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "image_link": venue.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows),
    }

    return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion
    data = request.form
    print(data)
    name = data['name']
    city = data['city']
    state = data['state']
    address = data['address']
    phone = data['phone']
    genres = request.form.getlist('genres')
    facebook_link = data['facebook_link']
    image_link = data.get(
        'image_link', 'https://esns.nl/wp-content/uploads/2020/01/Flohio_GrandTheatreMain_BartHeemskerk_02.jpg')

    # print(genres)

    if Venue.query.first() != None and Venue.query.filter_by(phone=phone).first() != None:
        flash('this Venue is already listed!')
    else:
        try:
            new_venue = Venue(name=name, city=city, state=state, address=address,
                              phone=phone, genres=genres, facebook_link=facebook_link, image_link=image_link)

            db.session.add(new_venue)
            db.session.commit()
            # on successful db insert, flash success
            flash('Venue ' + request.form['name'] +
                  ' was successfully listed!')

        except:
            db.session.rollback()
            # TODO: on unsuccessful db insert, flash an error instead.
            flash('Something went wrong :( Venue ' +
                  request.form['name'] + ' could not be listed')

        finally:
            db.session.close()

    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

    venue = Venue.query.filter_by(id=venue_id).first()
    try:
        db.session.delete(venue)
        db.session.commit()
        flash('venue' + venue.name + 'deleted')
    except:
        db.session.rollback()
        flash('An error occured while trying to delete venue ' + venue.name)
    finally:
        db.session.close()

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    # TODO: replace with real data returned from querying the database

    artists = Artist.query.all()
    data1 = [{
        "id": artist.id,
        "name": artist.name
    } for artist in artists
    ]

    return render_template('pages/artists.html', artists=data1)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".

    data = request.form
    print(data['search_term'])
    artists = Artist.query.filter(
        Artist.name.ilike('%' + data['search_term'] + '%')).all()
    print(artists)

    response = {
        "count": len(artists),
        "data": [{
            "id": artist.id,
            "name": artist.name,
            "num_upcoming_shows": Show.query.filter_by(artist_id=artist.id).count()
        } for artist in artists]
    }

    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id

    artist = Artist.query.filter_by(id=artist_id).first()
    genres = artist.genres.translate(
        str.maketrans('', '', '{ }')).split(",")

    shows = Show.query.filter_by(artist_id=artist_id).all()

    now = datetime.now()
    past_shows = []
    upcoming_shows = []
    for show in shows:
        show_date_formatted = datetime.strptime(
            show.start_time, '%Y-%m-%d %H:%M:%S')
        if show_date_formatted > now:
            venue = Venue.query.filter_by(id=show.venue_id).first()
            upcoming_shows.append({
                "venue_id": show.venue_id,
                "venue_name": venue.name,
                "venue_image_link": venue.image_link,
                "start_time": show.start_time
            })
        else:
            venue = Venue.query.filter_by(id=show.venue_id).first()
            past_shows.append({
                "venue_id": show.venue_id,
                "venue_name": venue.name,
                "venue_image_link": venue.image_link,
                "start_time": show.start_time
            })

    data = {
        "id": artist.id,
        "name": artist.name,
        "genres": genres,
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "website": artist.website_link,
        "facebook_link": artist.facebook_link,
        "seeking_venue": artist.seeking_venue,
        "seeking_description": artist.seeking_description,
        "image_link": artist.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows),
    }

    return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()

    artist = Artist.query.filter_by(id=artist_id).first()
    genres = artist.genres.translate(
        str.maketrans('', '', '{ }')).split(",")

    artist = {
        "id": artist.id,
        "name": artist.name,
        "genres": genres,
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "website": artist.website_link,
        "facebook_link": artist.facebook_link,
        "seeking_venue": artist.seeking_venue,
        "seeking_description": artist.seeking_description,
        "image_link": artist.image_link
    }

    # TODO: populate form with fields from artist with ID <artist_id>
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes

    data = request.form

    artist = Artist.query.filter_by(id=artist_id).first()

    artist.name = data['name']
    artist.city = data['city']
    artist.state = data['state']
    artist.phone = data['phone']
    artist.genres = data.getlist('genres')
    artist.facebook_link = data['facebook_link']
    artist.image_link = data.get(
        'image_link', 'https://www.thepeakid.com/wp-content/uploads/2016/03/default-profile-picture.jpg')

    try:
        db.session.commit()

        # on successful db insert, flash success
        flash('Artist ' + request.form['name'] +
              ' was successfully updated!')

    except:
        db.session.rollback()

        # TODO: on unsuccessful db insert, flash an error instead.
        flash('Something went wrong :( Artist ' +
              request.form['name'] + ' could not be updated')

    finally:
        db.session.close()

    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = Venue.query.filter_by(id=venue_id).first()
    genres = venue.genres.translate(
        str.maketrans('', '', '{ }')).split(",")

    venue = {
        "id": venue.id,
        "name": venue.name,
        "genres": genres,
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": venue.website_link,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "seeking_description": venue.seeking_description,
        "image_link": venue.image_link
    }
    # TODO: populate form with values from venue with ID <venue_id>
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes

    data = request.form

    venue = Venue.query.filter_by(id=venue_id).first()

    venue.name = data['name']
    venue.city = data['city']
    venue.state = data['state']
    venue.phone = data['phone']
    venue.genres = data.getlist('genres')
    venue.facebook_link = data['facebook_link']

    try:
        db.session.commit()

        # on successful db insert, flash success
        flash('Venue ' + request.form['name'] +
              ' was successfully updated!')

    except:
        db.session.rollback()

        # TODO: on unsuccessful db insert, flash an error instead.
        flash('Something went wrong :( Venue ' +
              request.form['name'] + ' could not be updated')

    finally:
        db.session.close()

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

    data = request.form

    name = data['name']
    city = data['city']
    state = data['state']
    phone = data['phone']
    genres = data.getlist('genres')
    facebook_link = data['facebook_link']
    image_link = data.get(
        'image_link', 'https://www.thepeakid.com/wp-content/uploads/2016/03/default-profile-picture.jpg')

    if Artist.query.first() != None and Artist.query.filter_by(phone=phone).first() != None:
        flash('this Artist is already listed!')
    else:
        try:

            new_artist = Artist(name=name, city=city, state=state,
                                phone=phone, genres=genres, facebook_link=facebook_link, image_link=image_link)

            db.session.add(new_artist)
            db.session.commit()

            # on successful db insert, flash success
            flash('Artist ' + request.form['name'] +
                  ' was successfully listed!')

        except:
            db.session.rollback()

            # TODO: on unsuccessful db insert, flash an error instead.
            flash('Something went wrong :( Artist ' +
                  request.form['name'] + ' could not be listed')

        finally:
            db.session.close()

    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.

    shows = Show.query.all()

    data1 = [{
        "venue_id": show.venue_id,
        "venue_name": Venue.query.filter_by(id=show.venue_id).first().name,
        "artist_id": Artist.query.filter_by(id=show.artist_id).first().id,
        "artist_name": Artist.query.filter_by(id=show.artist_id).first().name,
        "artist_image_link": Artist.query.filter_by(id=show.artist_id).first().image_link,
        "start_time": show.start_time

    }
        for show in shows
    ]

    print(data1)

    return render_template('pages/shows.html', shows=data1)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODO: insert form data as a new Show record in the db, instead

    data = request.form

    artist_id = data['artist_id']
    venue_id = data['venue_id']
    start_time = data['start_time']
    try:
        show = Show(artist_id=artist_id, venue_id=venue_id,
                    start_time=start_time)
        db.session.add(show)
        db.session.commit()
        # on successful db insert, flash success
        flash('Show was successfully listed!')
    except:
        db.session.rollback()
        # TODO: on unsuccessful db insert, flash an error instead.
        flash('Something went wrong :( new show could not be listed')

    finally:
        db.session.close()

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
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
