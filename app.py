from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'rent_tracker.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Tenant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    location = db.Column(db.String(100))
    town = db.Column(db.String(100))
    apt_no = db.Column(db.String(50))
    apt_type = db.Column(db.String(50))
    rent_total = db.Column(db.Float)
    amount_paid = db.Column(db.Float)
    sec_dep = db.Column(db.String(10))
    status = db.Column(db.String(20))
    payment_date = db.Column(db.Date)
    next_due = db.Column(db.Date)

    @property
    def outstanding(self):
        return (self.rent_total or 0) - (self.amount_paid or 0)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', tenants=Tenant.query.all())

@app.route('/add', methods=['POST'])
def add():
    t = Tenant(
        name=request.form.get('name'), phone=request.form.get('phone'),
        location=request.form.get('loc'), town=request.form.get('town'),
        apt_no=request.form.get('apt_no'), apt_type=request.form.get('type'),
        rent_total=float(request.form.get('total', 0)),
        amount_paid=float(request.form.get('paid', 0)),
        sec_dep=request.form.get('sec_dep'), status=request.form.get('status'),
        payment_date=datetime.strptime(request.form.get('pay_date'), '%Y-%m-%d'),
        next_due=datetime.strptime(request.form.get('next_due'), '%Y-%m-%d')
    )
    db.session.add(t)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
