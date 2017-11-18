#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request, render_template_string, json
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from forms import *
import os
from refugee import Person

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

# Automatically tear down SQLAlchemy.

# @app.teardown_request
# def shutdown_session(exception=None):
#     db_session.remove()


# Login required decorator.

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def home():
    return render_template('pages/placeholder.home.html')


@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')


@app.route('/login')
def login():
    form = LoginForm(request.form)
    return render_template('forms/login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    
    person = Person()
    person.setPlaceOfOrigin()
    person.setCampLocation()
    form = Reg2Form(request.form)
    # form.process()
    if request.method == 'POST' and form.validate():
        print('here')
        print(form.name.data)
    return render_template('forms/register.html', person=person, form=form)


@app.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)


@app.route('/reg2', methods=['GET'])
def reg2():
    # If get request has /reg2?file_number=<file_number>
    if 'file_number' in request.args:
        file_number = request.args['file_number']
        new_entity = 0

        # TODO get person from sql database
        person = Person('John M Doe', '2010-10-20', 'married', 'American',
                        'High School', 'Mason', 'Agnostic', 'White',
                        '2017-11-16')
        person.setPlaceOfOrigin('123 Pleasant St', '', 'Sharpsburg',
                                'MD', '12345', 'US')
        person.setCampLocation('23F', 'D', '4')
    else:
        person = Person()
        new_entity = 1

    form = Reg2Form(request.form)
    form.marital_status.default = person.marital_status.lower()
    form.process()
    return render_template('forms/registration2.html', person=person,
                           form=form, new_entity=new_entity)


@app.route('/reg2db', methods=['GET', 'POST'])
def reg2db():

    person = Person(**request.form)
    person.setPlaceOfOrigin(**request.form)
    person.setCampLocation(**request.form)
    new_entity = int(request.form['new_entity'])

    # Check person entity data in console
    # app.logger.info(person.__dict__)
    # app.logger.info(person.place_of_origin.__dict__)
    # app.logger.info(person.camp_location.__dict__)
    # app.logger.info('New Entity: ' + str(new_entity))

    # TODO insert/update database with info
    # insert if new_entity == 1, otherwise update

    # Check post request data
    # This is temporary for checking data
    # Eventually maybe reroute to another page
    return json.jsonify(request.form)


# Error handlers.


@app.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

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


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
