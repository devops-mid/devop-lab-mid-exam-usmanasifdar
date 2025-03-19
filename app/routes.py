import re
from flask import render_template, request, redirect, url_for, flash
from app import app, db
from app.models import User

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    phone = request.form.get('phone', '')

    # Validate email format
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        flash("Invalid email format.", "error")
        return redirect(url_for('index'))

    # Validate phone number (exactly 10 digits, numeric)
    phone_pattern = r'^\d{10}$'
    if not re.match(phone_pattern, phone):
        flash("Phone number must be exactly 10 digits.", "error")
        return redirect(url_for('index'))

    # Save user to database
    user = User(name=name, email=email, phone=phone)
    db.session.add(user)
    db.session.commit()

    flash("User added successfully!", "success")
    return redirect(url_for('index'))
