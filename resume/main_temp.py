

# Initialize the database with the app
db.init_app(app)

# Create tables before first request
@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def home():
    return render_template("index.html")

def login():
    
        
        # Check if user exists
        
        if user and user.check_password(password):
            # Set session data for logged in user
            return redirect(url_for('resume_template'))
        else:
    

def signup():
    
        
        # Check if passwords match
        
        # Check if username or email already exists
        
        if existing_user:
        elif existing_email:
        else:
            # Create new user
            new_user.set_password(password)
            
            db.session.add(new_user)
            db.session.commit()
            
    

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

def generate_resume_pdf():
    try:
        else:
        
        # Get form data
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
        for key in request.form:
            if key.startswith('education['):
                
                    education.append({})
                
        
        
        # Process achievements
        
        # Process skills
        
        # Import our PDF utility
        
        # Generate PDF
        
        # Create response
        
        return response
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def preview_resume():
    else:
    
    # Get form data
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
    for key in request.form:
        if key.startswith('education['):
            
                education.append({})
            
    
    
    # Process achievements
    
    # Process skills
    
    # Render the template with data

