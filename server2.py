from flask import Flask,render_template,url_for,request,redirect,session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail
import json




with open('config.json','r')as c:
	params=json.load(c)["params"]

app=Flask(__name__)
app.config.update(
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT='465',
	MAIL_USE_SSL=True,
	MAIL_USERNAME=params["gmail_user"],
	MAIL_PASSWORD=params["gmail_password"]
	)
mail=Mail(app)
app.secret_key="196137"
app.config['SQLALCHEMY_DATABASE_URI']='mysql://sql12360313:Ccz38MRRDL@sql12.freesqldatabase.com/sql12360313'
db=SQLAlchemy(app)



class Userdetails(db.Model):
    email= db.Column(db.String(120), unique=False, nullable=False)
    instausername= db.Column(db.String(120), unique=False, nullable=False)
    sno= db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)
    date= db.Column(db.String(12), unique=False, nullable=True)


class Reports(db.Model):
	sno= db.Column(db.Integer, primary_key=True)
	user= db.Column(db.String(120), unique=False, nullable=False)
	report= db.Column(db.String(120), unique=False, nullable=False)





@app.route('/')
def hello():
	return render_template('createaccount.html')


@app.route('/login.html')
def getintry():
	return render_template('login.html')

@app.route('/createaccount.html')
def nice():
	return render_template('createaccount.html')

@app.route('/alreadytaken.html')
def goo():
	return render_template('alreadytaken.html')

@app.route('/<string:pagename>')
def pagename(pagename):
	if "username" in session:
		try:
			return render_template(pagename)
		except:
			return redirect('feeder.html')
	else:
		return redirect(url_for('checker'))
	





def save(data):
	username=data["username"]
	password=data["password"]
	email=data['email']
	instausername=data["instausername"]
	entry=Userdetails(email=email,instausername=instausername, username=username,password=password,date=datetime.now())
	db.session.add(entry)
	db.session.commit()
	mail.send_message('NEW USER IN APP',sender=email,recipients=[params["gmail_user"]],body= email +"\n"+username+"\n"+instausername )
	mail.send_message('Welcome ',sender=params["gmail_user"],recipients=[email],body= 'hello there '+username +"\n"+'Welcome to Regale.com'+"\n"+'Enjoy writing and publishing with us in Regale.com'+"\n"+'we make sure that our users enjoy maximum privacy and safe promotions' )
	




def namecheck(name):
	num=Userdetails.query.filter_by(username=name).count()
	if num>0:
		return False
	else:
		return True


def passcheck(peru,passu):
	val=Userdetails.query.filter_by(username=peru).first()
	if(val.password==passu):
		return True
	else:
		return False
	
	
		



@app.route('/login',methods=['POST','GET'])
def login():
	if(request.method=='POST'):
		data=request.form.to_dict()
		if(namecheck(data["username"])):
			if data["check"]==data["password"]:
				save(data)
				return redirect('login.html')
			else:
			    return redirect('createaccount.html')
		else:
			return redirect('alreadytaken.html')


@app.route('/checklogin',methods=['POST','GET'])
def checker():
	if(request.method=='POST'):
		data1=request.form.to_dict()
		if(namecheck(data1["username"])):
			return render_template('createagain.html')
		else:
			if(passcheck(data1["username"],data1["password"])):
				session["username"]=data1["username"]
				return redirect('feeder.html')
			else:
				return render_template('createagain.html')
	else:
		if "username" in session:
			return redirect(url_for("checker"))
			
		return render_template('login.html')

   
class Articles(db.Model):
	sno = db.Column(db.Integer, primary_key=True)
	title= db.Column(db.String(120), unique=False, nullable=False)
	article= db.Column(db.String(120), unique=False, nullable=False)
	theme= db.Column(db.String(120), unique=False, nullable=False)
	date= db.Column(db.String(12), unique=False, nullable=True)
	username= db.Column(db.String(120), unique=False, nullable=False)
	slug= db.Column(db.String(120), unique=False, nullable=False)
	

@app.route("/article/<string:post_slug>",methods=['GET'])
def view(post_slug):
	if "username" in session:
		article=Articles.query.filter_by(slug=post_slug).first()
		inst=article.username
		writer=Userdetails.query.filter_by(username=inst).first()
		return render_template('view.html',article=article,writer=writer)
	else:
		return redirect(url_for("checker"))

	


@app.route("/feeder.html")
def large():
	if "username" in session:
		post=Articles.query.filter_by().all()
		return render_template('feeder.html',post=post)
	else:
		return redirect(url_for("checker"))

def saver():
	title=session["articlename"]
	article=session["article"]
	theme=session["theme"]
	username=session["username"]
	slug=session["username"]+session["articlename"]
	art=Articles(slug=slug,title=title,article=article,theme=theme,username=username,date=datetime.now())
	db.session.add(art)
	db.session.commit()
	


@app.route('/article',methods=['POST','GET'])
def poster():
	if(request.method=='POST'):
		articledata=request.form.to_dict()
		session["articlename"]=articledata["articlename"]
		session["article"]=articledata["article"]
		session["theme"]=articledata["theme"]
		
		return render_template('article.html',theme=articledata["theme"],articlename=articledata["articlename"],article=articledata["article"],username=session["username"])

	else:
		if "username" in session:
			return render_template('create.html')
	return redirect(url_for('checker'))

@app.route('/addit',methods=['POST','GET'])
def adder():
	
	if(request.method=='POST'):
		saver()
		return redirect('feeder.html')
	else:
		if "username" in session:
			return render_template('create.html')
	return redirect(url_for('checker'))

@app.route('/report',methods=['POST','GET'])
def reportit():
	if(request.method=='POST'):
		report=request.form.to_dict()
		user=report["user"]
		reports=report["reason"]
		complain=Reports(user=user,report=reports)
		db.session.add(complain)
		db.session.commit()
		mail.send_message('REPORT ON A USER',sender=params["gmail_user"],recipients=[params["gmail_user"]],body=user +"\n"+reports+"\n" )
		return redirect('feeder.html')
	else:
		if "username" in session:
			return render_template('report.html')
	return redirect(url_for('checker'))
	

@app.route('/addinstagram',methods=['POST','GET'])
def settings():
	if(request.method=='POST'):
		changes=request.form.to_dict()
		warn='password incorrect'
		guy=Userdetails.query.filter_by(username=session["username"]).first()
		if(changes["pass"]==guy.password):
			guy.instausername=changes["instagram"]
			db.session.commit()
			return redirect('feeder.html')
		else:
			return render_template('walter.html',warn=warn)
	else:
		if "username" in session:
			return render_template('settings.html')
	return redirect(url_for('checker'))

@app.route('/addmailid',methods=['POST','GET'])
def letitgo():
	if(request.method=='POST'):
		jesse=request.form.to_dict()
		warn='password incorrect'
		thegod=Userdetails.query.filter_by(username=session["username"]).first()
		if(jesse["pass"]==thegod.password):
			thegod.email=jesse["emailid"]
			db.session.commit()
			return redirect('feeder.html')
		else:
			return render_template('walter.html',warn=warn)

	else:
		if "username" in session:
			return render_template('settings.html')
	return redirect(url_for('checker'))

@app.route('/logout')
def logout():
	session.clear()
	return redirect('login.html')


app.run(debug=True)


