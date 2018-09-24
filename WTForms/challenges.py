from flask import Flask, request, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import Required, Email
import requests
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.debug = True

@app.route('/')
def home():
    return "Hello, world!"
    
#create class to represent WTForm that inherits flask form
class NameForm(FlaskForm):
    artist = StringField('Enter artist', validators=[Required()])
    result = IntegerField('Enter the number of results', validators=[Required()])
    email = StringField('Enter your email', validators=[Required(),Email()])
    submit = SubmitField('Submit')

@app.route('/itunes-form')
def itunes_form():
    #what code goes here?
    simpleForm = NameForm()
    return render_template('itunes-form.html', form=simpleForm) # HINT : create itunes-form.html to represent the form defined in your class

@app.route('/itunes-result', methods = ['GET', 'POST'])
def itunes_result():
	form = NameForm()
	if request.method == 'POST' and form.validate_on_submit():
		artist = form.artist.data
		results = form.result.data
		params = {}
		params['term'] = artist
		params['limit'] = results
		response = requests.get('https://itunes.apple.com/search', params = params)
		response_py = json.loads(response.text)['results']

    # HINT : create itunes-results.html to represent the results and return it
	flash('All fields are required!')
	return render_template('itunes-result.html', result_html = response) #this redirects you to itunes_form if there are errors

if __name__ == '__main__':
    app.run()
