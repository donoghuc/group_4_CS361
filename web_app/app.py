#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request, render_template_string, json, redirect, url_for, flash, session
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

# db = SQLAlchemy(app)

# Automatically tear down SQLAlchemy.

# @app.teardown_request
# def shutdown_session(exception=None):
#     db_session.remove()


# Login required decorator.

# def login_required(test):
#     @wraps(test)
#     def wrap(*args, **kwargs):
#         if 'logged_in' in session:
#             return test(*args, **kwargs)
#         else:
#             flash('You need to login first.')
#             return redirect(url_for('login'))
#     return wrap

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('forms/login.html')
    else:
        return render_template('pages/placeholder.home.html')


@app.route('/about')
def about():
    if not session.get('logged_in'):
        return render_template('forms/login.html')
    else:
        return render_template('pages/placeholder.about.html')


@app.route('/login', methods =['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['password'] == 'password' and request.form['username'] == 'admin':
          session['logged_in'] = True;
        flash('Welcome!')
    return home()
       # form = LoginForm(request.form)
   # return render_template('forms/login.html', form=form)
   
@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()


@app.route('/register', methods=['GET', 'POST'])
def register():
    if not session.get('logged_in'):
        return render_template('forms/login.html')
    else:
        """ This view will handle the refugee registration form
            Get and validate data and push to database
        """

        # Intialize empty person object
        person = Person()
        person.setPlaceOfOrigin()
        person.setCampLocation()
        # get form data
        form = Reg2Form(request.form)
        if request.method == 'POST':
            # validate form data
            form.validate_on_submit()
            # set state of person based on validated form data
            person.build_person_from_form(form)
            # Insert person into database
            db.refugee_db_insertion(person, db.DATABASE_CON)
            # redirect to home.
            return redirect(url_for('home'))
        # render form for collecting registration data.
        return render_template('forms/register.html', person=person, form=form)


@app.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)


@app.route('/reg2', methods=['GET'])
def reg2():
    if not session.get('logged_in'):
        return render_template('forms/login.html')
    else:
        # If get request has /reg2?file_number=<file_number>
        if 'file_number' in request.args:
            file_number = request.args['file_number']
            person = db.refugee_db_selection(file_number, db.DATABASE_CON)
            new_entity = 0
        else:
            file_number = 0
            person = Person()
            new_entity = 1

        form = Reg2Form(request.form)
        form.marital_status.default = person.marital_status.lower()
        form.process()
        return render_template('forms/registration2.html', person=person,
                           form=form, new_entity=new_entity, file_number=file_number)


@app.route('/reg2db', methods=['POST'])
def reg2db():
    if not session.get('logged_in'):
        return render_template('forms/login.html')
    else:
        form = Reg2Form(request.form)
        form.validate_on_submit()

        person = Person(file_number=request.form['file_number'])
        person.build_person_from_form(form)
        new_entity = int(request.form['new_entity'])

    # Check person entity data in console
    # app.logger.info(person.__dict__)
    # app.logger.info(person.place_of_origin.__dict__)
    # app.logger.info(person.camp_location.__dict__)
    # app.logger.info('New Entity: ' + str(new_entity))

        if new_entity == 1:
            db.refugee_db_insertion(person, db.DATABASE_CON)
        else:
            db.refugee_db_update(person, db.DATABASE_CON)

    # Check post request data
    # This is temporary for checking data
    # Eventually maybe reroute to another page
        return json.jsonify(request.form)

@app.route('/search', methods= ['GET', 'POST'])
def search():
    if not session.get('logged_in'):
        return render_template('forms/login.html')
    else:
        if request.method == "POST":
            form = Reg2Form(request.form)
            form.validate_on_submit()
            name = request.args['search']
            person = db.refugee_db_search_by_name(name, db.DATABASE_CON)
            # redirect to results page
            return redirect("reg2.html", records=c.fetchall())
        return render_template('forms/search.html')

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
