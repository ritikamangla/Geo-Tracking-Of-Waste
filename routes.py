import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect,request
from VT import app,db,bcrypt
from VT.models import User,Truck,Waste,ConGrievance
from VT.forms import LoginForm,StatusForm,UpdateForm,GrievanceForm,AddtruckForm
from flask_login import login_user, current_user,logout_user,login_required
import datetime

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='Home')

@app.route("/login", methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('status'))
	form = LoginForm()
	if form.validate_on_submit():
		user= User.query.filter_by(email=form.email.data).first()
		if user and user.password==form.password.data:
			login_user(user,remember=form.remember.data)
			next_page=request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('status'))
		else:
			flash('Login Unsuccessful. Please check email and password', 'danger')
	return render_template('login.html', title='Login', form=form)                	   
    
@app.route("/status",methods=['GET','POST'])
def status():
	form = StatusForm(request.form)
	trucks=Truck.query.all()
	#trucks=db.session.query("SELECT * FROM TRUCK")
	if request.method=='POST':
		return redirect(url_for('track'))
	
	return render_template('status.html', trucks=trucks,form=form)

@app.route("/update",methods=['GET', 'POST'])
def update():
	form = UpdateForm(request.form)
	if form.validate_on_submit():
		waste = Waste(waste_id=form.waste_id.data, truck_dry=form.truck_dry.data, truck_wet=form.truck_wet.data,truck_loc=form.truck_loc.data)
		db.session.add(waste)
		db.session.commit()
		flash(f'Success! Please fill in the remaining details', 'success')

		db.session.query(Truck).filter(Truck.truck_id == form.waste_id.data).\
		update({Truck.truck_time:datetime.datetime.now()}, synchronize_session = False)
		#veh=Truck.query.filter_by(truck_id=1)
		#veh.truck_time=datetime.datetime.now()
		db.session.commit()
		
		return redirect(url_for('status'))
	return render_template('update.html', title='Update',form=form)


@app.route("/track",methods=['GET', 'POST'])
def track():
	#wastes = db.session.query(Waste).filter(Waste.waste_id == waste_id)
	#wastes=Waste.query.filter_by(Waste.waste_id == 1).first()
	return render_template('track.html', title='Track')

@app.route("/grievance",methods=['GET', 'POST'])
def grievance():
	form = GrievanceForm(request.form)
	if form.validate_on_submit():
		text = ConGrievance(grieve=form.grieve.data)
		db.session.add(text)
		db.session.commit()
		return redirect(url_for('home'))

	return render_template('grievance.html', title='Consumer Grievance',form=form)


@app.route("/dashboard")
def dashboard():
	return render_template('dashboard.html', title='Dashboard')

"""@app.route("/addtruck",methods=['GET', 'POST'])
def addtruck():
	form=AddtruckForm(request.form)
	if form.validate_on_submit():
		truck = Truck(truck_id=form.truck_id.data, truck_type=form.truck_type.data)
		db.session.add(truck)
		db.session.commit()
		return redirect(url_for('status'))

	return render_template('addtruck.html', title='Add Truck',form=form)"""

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))