from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime

from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField 
from wtforms.validators import DataRequired, Email

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)
app.config['SECRET_KEY'] = '123abc'

class NameForm (FlaskForm): 
    name = StringField('What is your name?', validators=[DataRequired()]) 
    email = StringField('What is your UofT Email Address?', validators=[Email()]) 
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
    uoft = 'utoronto'
    uoft_val = None #uoft email validation variable: none if not uoft, 1 if uoft  
    first = None

    if 'name' not in session:
        session['name'] = None

    if 'email' not in session:
        session['email'] = None

    if 'first' not in session:
        first = True
    else:
        first = session.get('first')

    form = NameForm()    
    if form.validate_on_submit():
        old_name = session.get('name')
        old_email = session.get('email')

        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')

        if old_email is not None and old_email != form.email.data:
            flash('Looks like you have changed your email!')
        session['name'] = form.name.data
        session['email'] = form.email.data
        if uoft not in form.email.data:
            flash('Please enter a valid UofT email')

        session['first'] = False

        return redirect(url_for('index'))
   
    if session['email'] is not None and uoft in session['email']:
        uoft_val = 1
    else:
        uoft_val = 0

    return render_template('index.html', form = form, name = session.get('name'), uoft_val = uoft_val, email = session.get('email'), first = first)

@app.route('/user/<name>')
def user(name):
    curr_date = datetime.utcnow()
    return render_template('user.html', name=name, current_time=curr_date)