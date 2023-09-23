from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime

from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField 
from wtforms.validators import DataRequired

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)
app.config['SECRET_KEY'] = '123abc'

class NameForm (FlaskForm): 
    name = StringField('What is your name?', validators=[DataRequired()]) 
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    name = None 
    form = NameForm() 
    if form.validate_on_submit(): 
        name = form.name.data 
        form.name.data = ''
    return render_template('index.html', form=form, name=name)

@app.route('/user/<name>')
def user(name):
    curr_date = datetime.utcnow()
    return render_template('user.html', name=name, current_time=curr_date)