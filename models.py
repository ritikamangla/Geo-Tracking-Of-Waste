from datetime import datetime
from VT import db,login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Truck(db.Model, UserMixin):
	truck_id=db.Column(db.Integer,primary_key=True)
	truck_type = db.Column(db.String(20), unique=False, nullable=False)
	truck_time=db.Column(db.String(20), nullable=True, unique=False, default=datetime.utcnow)
	#truck_track=db.Column(db.String(20), unique=False, nullable=True)

	def __repr__(self):
		return f"Truck('{self.truck_id}','{self.truck_type}','{self.truck_time}')"

	
class Waste(db.Model,UserMixin):
	__tablename__= 'waste'
	id=db.Column(db.Integer,primary_key=True)
	waste_id=db.Column(db.Integer,db.ForeignKey('truck.truck_id'),nullable=False)
	truck_dry=db.Column(db.Integer, unique=False, nullable=True)
	truck_wet=db.Column(db.Integer, unique=False, nullable=True)
	truck_time=db.Column(db.DateTime,nullable=True,default=datetime.utcnow)
	truck_loc=db.Column(db.String(20), unique=False, nullable=True)

	def __repr__(self):
		return f"Waste('{self.id}','{self.waste_id}','{self.truck_dry}',{self.truck_wet}',{self.truck_time}',{self.truck_loc}')"



class ConGrievance(db.Model,UserMixin):
	id=db.Column(db.Integer,primary_key=True)
	grieve=db.Column(db.String(100), unique=False, nullable=True)

	def __repr__(self):
		return f"Waste('{self.id}','{self.grieve}')"
