import os
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import g4f

# 1. SETUP
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'nes_secret_123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'nes_mainframe.db')
db = SQLAlchemy(app)

# 2. DATABASE MODELS
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

# 3. LOGIN SYSTEM
login_manager = LoginManager(app)
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id)) # Modern SQLAlchemy Fix

# 4. ROUTES (Home & AI)
@app.route('/')
def home():
    return "<h1>NES 24/7 System Online</h1><p>The server is running perfectly.</p>"

@app.route('/ai', methods=['POST'])
@login_required
def ai():
    user_message = request.json.get('message')
    try:
        # Fixed AI Provider List for 2026
        response = g4f.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": user_message}],
            provider=g4f.Provider.PollinationsAI # Most stable for 24/7
        )
        return jsonify({"reply": response})
    except Exception as e:
        return jsonify({"reply": f"AI Error: {str(e)}"}), 500

# 5. START SERVER (Waitress for 24/7)
if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Automatically creates the .db file
    
    from waitress import serve
    print("🚀 NES Server Starting 24/7...")
    serve(app, host='0.0.0.0', port=int(os.environ.get("PORT", 5500)))