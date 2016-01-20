from flask import request, Flask, render_template
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form
from wtforms.validators import Required, NumberRange, IPAddress
from wtforms import IntegerField, StringField, SubmitField
from subprocess import check_output as sub
from random import choice
from string import letters, digits, punctuation
from diceware import get_passphrase as ppgen

cs = letters + digits + punctuation
def pwgen(n=12): return ''.join(choice(cs) for s in range(n))


app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = pwgen(8)

class PasswordForm(Form):
    length = IntegerField('Number of Symbols?', validators=[Required(), NumberRange(min=1, max=30, message="Should be between 1 and 30")])
    submit = SubmitField('Submit')

class PassphraseForm(Form):
    length = IntegerField('Number of Symbols?', validators=[Required(), NumberRange(min=1, max=12, message="Should be between 1 and 12")])
    submit = SubmitField('Submit')

class DigForm(Form):
	domain = StringField('Domain Name', validators=[Required()])
	submit = SubmitField('Submit')

class WhoisForm(Form):
	domain = StringField('Domain Name', validators=[Required()])
	submit = SubmitField('Submit')

class TracerouteForm(Form):
	domain = StringField('Domain Name', validators=[Required()])
	submit = SubmitField('Submit')

@app.route('/')
def index():
        return render_template('index.html')
	
@app.route('/password', methods=('GET', 'POST'))
def password():
        form = PasswordForm()
        length = None
        entropy = 78.66
        if form.validate_on_submit():
                length = form.length.data
                entropy = 6.555 * length
                return render_template('pwgen.html', password=pwgen(length), entropy=entropy, form=form)
        else:
                return render_template('pwgen.html', password=pwgen(), entropy=entropy, form=form)

@app.route('/passphrase', methods=('GET', 'POST'))
def passphrase():
        form = PassphraseForm()
        length = None
        entropy = 77.55
        if form.validate_on_submit():
                length = form.length.data
                entropy = 12.925 * length
                passphrase=sub(['diceware -n ' + str(length)], shell=True)
                return render_template('ppgen.html', passphrase=passphrase, entropy=entropy, form=form)
        else:
                passphrase = ppgen()
                return render_template('ppgen.html', passphrase=passphrase, entropy=entropy, form=form)

@app.route('/dig', methods=('GET', 'POST'))
def dig():
	form = DigForm()
	domain = None
	if form.validate_on_submit():
		domain = form.domain.data
		digout = sub(['dig -t ANY ' + domain], shell=True).replace('\n', '<br />')
		return render_template('dig.html', form=form, output=digout, domain=domain)
	else:
		return render_template('dig.html', form=form, domain=domain)
		
@app.route('/whois', methods=('GET', 'POST'))
def whois():
	form = WhoisForm()
	domain = None
	if form.validate_on_submit():
		domain = form.domain.data
		whoisout = sub(['whois ' + domain], shell=True).replace('\n', '<br />')
		return render_template('whois.html', form=form, output=whoisout, domain=domain)
	else:
		return render_template('whois.html', form=form, domain=domain)

@app.route('/traceroute', methods=('GET', 'POST'))
def traceroute():
	form = TracerouteForm()
	domain = None
	if form.validate_on_submit():
		domain = form.domain.data
		traceout = sub(['traceroute ' + domain], shell=True).replace('\n', '<br />')
		return render_template('traceroute.html', form=form, output=traceout, domain=domain)
	else:
		return render_template('traceroute.html', form=form, domain=domain)

if __name__ == '__main__':
        app.run(host='0.0.0.0', port=80, debug=True)
