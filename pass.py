import subprocess, random, string
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form
from wtforms import IntegerField, SubmitField
from wtforms.validators import Required, NumberRange
from flask import request, Flask, render_template
from diceware import get_passphrase as pphrase

def password(length=12):
	chars = string.letters + string.digits + string.punctuation
	return ''.join(random.choice(chars) for i in range(length))

class PasswordForm(Form):
	length = IntegerField('Number of Symbols?', validators=[Required(), NumberRange(min=1, max=30, message="Should be between 1 and 30")])
	submit = SubmitField('Submit')

class PassphraseForm(Form):
	length = IntegerField('Number of Symbols?', validators=[Required(), NumberRange(min=1, max=12, message="Should be between 1 and 12")])
	submit = SubmitField('Submit')

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = password(8) 

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/password', methods=('GET', 'POST'))
def pwgen():
	form = PasswordForm()
	length = None
	entropy = 78.66 
	if form.validate_on_submit():
		length = form.length.data
		entropy = 6.555 * length
		return render_template('pwgen.html', password=password(length), entropy=entropy, form=form)
	else:
		return render_template('pwgen.html', password=password(), entropy=entropy, form=form)

@app.route('/passphrase', methods=('GET', 'POST'))
def ppgen():
	form = PassphraseForm()
	length = None
	entropy = 77.55
	if form.validate_on_submit():
		length = form.length.data
		entropy = 12.925 * length
		passphrase=subprocess.check_output(['diceware -n ' + str(length)], shell=True)
		return render_template('ppgen.html', passphrase=passphrase, entropy=entropy, form=form)
	else:
		passphrase = pphrase()
		return render_template('ppgen.html', passphrase=passphrase, entropy=entropy, form=form)

if __name__ == '__main__':
        app.run(host='0.0.0.0', port=80)
