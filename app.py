from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

app = Flask(__name__)
# Use a persistent path if possible, or ensure it recreates
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'rent_tracker.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Tenant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    building_loc = db.Column(db.String(100))
    town = db.Column(db.String(100))
    apt_type = db.Column(db.String(50))
    rent_total = db.Column(db.Float)
    amount_paid = db.Column(db.Float)
    move_in_date = db.Column(db.Date)
    expiry_date = db.Column(db.Date)

    @property
    def outstanding_balance(self):
        return (self.rent_total or 0) - (self.amount_paid or 0)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', tenants=Tenant.query.all())

@app.route('/add', methods=['POST'])
def add():
    # Use .get() to prevent 'Bad Request' if a field is missing
    name = request.form.get('name')
    phone = request.form.get('phone')
    loc = request.form.get('loc')
    town = request.form.get('town')
    apt_type = request.form.get('type')
    total = float(request.form.get('total', 0))
    paid = float(request.form.get('paid', 0))
    move = datetime.strptime(request.form.get('move'), '%Y-%m-%d')
    exp = datetime.strptime(request.form.get('exp'), '%Y-%m-%d')
    
    t = Tenant(name=name, phone=phone, building_loc=loc, town=town, 
               apt_type=apt_type, rent_total=total, amount_paid=paid, 
               move_in_date=move, expiry_date=exp)
    db.session.add(t)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
