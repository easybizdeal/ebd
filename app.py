from flask import Flask, render_template, request, redirect, url_for, flash, session
from config import Config
from models import db, User
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail, Message
from flask_login import login_user, logout_user, login_required
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Extensions
db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
mail = Mail(app)
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create tables
with app.app_context():
    db.create_all()

# === HOMEPAGE ===
@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and user.password and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash("✅ Login successful!", "success")
            return redirect(url_for('dashboard'))  # Update this if your route name is different
        else:
            flash("❌ Invalid email or password", "danger")
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('✅ You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first = request.form['first_name']
        last = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        country = request.form['country']
        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered", "danger")
            return redirect(url_for('signup'))

        new_user = User(first_name=first, last_name=last, email=email,
                        password=hashed_pw, country=country, is_verified=False)
        db.session.add(new_user)
        db.session.commit()

        # Generate verification token
        token = s.dumps(email, salt='email-confirm')
        link = url_for('verify_email', token=token, _external=True)

        # Send verification email
        msg = Message('Verify your Easy Biz Deal email', recipients=[email])
        msg.html = render_template('email_verification.html', user=new_user, verification_link=link)
        mail.send(msg)

        # Auto login user after signup
        login_user(new_user)

        # Redirect to dashboard with verification prompt
        return redirect(url_for('dashboard', show='verify_email'))

    return render_template('signup.html')


@app.route('/verify/<token>')
def verify_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600)
    except:
        return "⛔ Invalid or expired token."

    user = User.query.filter_by(email=email).first()
    if user:
        user.is_verified = True
        db.session.commit()
        # Redirect to dashboard with verified message
        return redirect(url_for('dashboard', show='verified'))

    return "❌ User not found."


@app.route('/dashboard')
@login_required
def dashboard():
    show = request.args.get('show')
    show_verify_popup = False
    show_verified_popup = False

    if show == 'verify_email':
        show_verify_popup = True
    elif show == 'verified':
        show_verified_popup = True

    return render_template('dashboard.html',
                           show_verify_popup=show_verify_popup,
                           show_verified_popup=show_verified_popup)

@app.route('/my-crm')
@login_required
def my_crm():
    return "My CRM page will be here soon."

    # ✅ App Run
if __name__ == '__main__':
    import socket
    try:
        app.run(debug=True, use_reloader=False)
    except socket.error as e:
        print("Socket error on restart:", e)