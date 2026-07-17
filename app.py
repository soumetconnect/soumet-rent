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
    building_loc = db.Column(db.String(100))
    town = db.Column(db.String(100))
    apt_type = db.Column(db.String(50))
    rent_total = db.Column(db.Float)
    amount_paid = db.Column(db.Float)
    move_in_date = db.Column(db.Date)
    expiry_date = db.Column(db.Date)

    @property
    def outstanding_balance(self):
        return self.rent_total - self.amount_paid

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html', tenants=Tenant.query.all())

@app.route('/add', methods=['POST'])
def add():
    t = Tenant(
        name=request.form['name'], phone=request.form['phone'],
        building_loc=request.form['loc'], town=request.form['town'],
        apt_type=request.form['type'], rent_total=float(request.form['total']),
        amount_paid=float(request.form['paid']),
        move_in_date=datetime.strptime(request.form['move'], '%Y-%m-%d'),
        expiry_date=datetime.strptime(request.form['exp'], '%Y-%m-%d')
    )
    db.session.add(t)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/receipt/<int:id>')
def receipt(id):
    t = Tenant.query.get_or_404(id)
    return render_template('receipt.html', t=t)

if __name__ == '__main__':
    app.run()
