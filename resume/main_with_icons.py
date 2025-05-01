from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
import io
from models import db, User
import base64
from icons_pdf import create_professional_resume

app = Flask(__name__) #creating flask app name
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the app
db.init_app(app)

# Create tables before first request
@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    success = None
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Check if user exists
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            # Set session data for logged in user
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('resume_template'))
        else:
            error = 'Invalid username or password. Please try again.'
    
    return render_template('login.html', error=error, success=success)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Check if passwords match
        if password != confirm_password:
            error = 'Passwords do not match.'
            return render_template('signup.html', error=error)
        
        # Check if username or email already exists
        existing_user = User.query.filter_by(username=username).first()
        existing_email = User.query.filter_by(email=email).first()
        
        if existing_user:
            error = 'Username already exists.'
        elif existing_email:
            error = 'Email already in use.'
        else:
            # Create new user
            new_user = User(username=username, email=email)
            new_user.set_password(password)
            
            db.session.add(new_user)
            db.session.commit()
            
            return redirect(url_for('login', success='Account created successfully! Please log in.'))
    
    return render_template('signup.html', error=error)

@app.route('/logout')
def logout():
    # Clear session data
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/resume_template')
def resume_template():
    # Check if user is logged in
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template("resume_template.html")

@app.route('/resume_1')
def resume_1():
    # Check if user is logged in
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template("resume_1.html")

@app.route('/resume_2')
def resume_2():
    # Check if user is logged in
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template("resume_2.html")

@app.route('/generate_resume_pdf', methods=['POST'])
def generate_resume_pdf():
    try:
        template_type = request.form.get('template_type')
        if template_type == '1':
            filename = "resume_1_{}.pdf".format(datetime.now().strftime("%Y%m%d%H%M%S"))
        else:
            filename = "resume_2_{}.pdf".format(datetime.now().strftime("%Y%m%d%H%M%S"))
        
        # Get form data
        data = {
            'name': request.form.get('name', ''),
            'dob': request.form.get('dob', ''),
            'email': request.form.get('email', ''),
            'phnum': request.form.get('phnum', ''),
            'city': request.form.get('city', ''),
            'state': request.form.get('state', ''),
            'ucareerob': request.form.get('ucareerob', ''),
            'uaboutself': request.form.get('uaboutself', ''),
            'fname': request.form.get('fname', ''),
            'mname': request.form.get('mname', ''),
            'paddress': request.form.get('paddress', ''),
        }
        
        # Process education items
        education = []
        for key in request.form:
            if key.startswith('education['):
                index = key.split('[')[1].split(']')[0]
                field = key.split('][')[1].split(']')[0]
                
                while len(education) <= int(index):
                    education.append({})
                
                education[int(index)][field] = request.form[key]
        
        data['education'] = education
        
        # Process achievements
        achievements = request.form.getlist('achievements[]')
        data['achievements'] = achievements
        
        # Process skills
        skills = request.form.getlist('skills[]')
        data['skills'] = skills
        
        # Generate PDF with icons that match the example resume design
        pdf_buffer = create_professional_resume(data)
        
        # Create response
        response = make_response(pdf_buffer.getvalue())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        return response
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/preview_resume', methods=['POST'])
def preview_resume():
    template_type = request.form.get('template_type')
    if template_type == '1':
        template = 'resume_1_pdf.html'
    else:
        template = 'resume_2_pdf.html'
    
    # Get form data
    data = {
        'name': request.form.get('name', ''),
        'dob': request.form.get('dob', ''),
        'email': request.form.get('email', ''),
        'phnum': request.form.get('phnum', ''),
        'city': request.form.get('city', ''),
        'state': request.form.get('state', ''),
        'ucareerob': request.form.get('ucareerob', ''),
        'uaboutself': request.form.get('uaboutself', ''),
        'fname': request.form.get('fname', ''),
        'mname': request.form.get('mname', ''),
        'paddress': request.form.get('paddress', ''),
    }
    
    # Process education items
    education = []
    for key in request.form:
        if key.startswith('education['):
            index = key.split('[')[1].split(']')[0]
            field = key.split('][')[1].split(']')[0]
            
            while len(education) <= int(index):
                education.append({})
            
            education[int(index)][field] = request.form[key]
    
    data['education'] = education
    
    # Process achievements
    achievements = request.form.getlist('achievements[]')
    data['achievements'] = achievements
    
    # Process skills
    skills = request.form.getlist('skills[]')
    data['skills'] = skills
    
    # Render the template with data
    return render_template(template, data=data)

if __name__ == "__main__":
    app.run(debug=True)
