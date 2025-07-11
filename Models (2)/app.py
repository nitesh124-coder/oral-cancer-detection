from flask import Flask, render_template, request, jsonify, redirect, url_for, session, send_from_directory, send_file
import os
import numpy as np
from werkzeug.utils import secure_filename
import random
from functools import wraps
from datetime import datetime
import json
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# Create Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['HISTORY_FOLDER'] = 'history/'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}
app.config['SECRET_KEY'] = 'your_secret_key_here'

# Create necessary folders
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['HISTORY_FOLDER'], exist_ok=True)

# Initialize history storage
HISTORY_FILE = os.path.join(app.config['HISTORY_FOLDER'], 'analysis_history.json')

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    return []

def save_history(history):
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def generate_pdf_report(analysis_data, image_path):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30
    )
    story.append(Paragraph("Oral Cancer Detection Analysis Report", title_style))
    story.append(Spacer(1, 20))

    # Image
    if os.path.exists(image_path):
        img = Image(image_path, width=400, height=300)
        story.append(img)
        story.append(Spacer(1, 20))

    # Analysis Results
    story.append(Paragraph("Analysis Results", styles['Heading2']))
    story.append(Spacer(1, 10))

    # Result details
    details = [
        ("Prediction", analysis_data['prediction']),
        ("Confidence", f"{analysis_data['confidence']*100:.1f}%"),
        ("Message", analysis_data['message']),
        ("Date", analysis_data['date'])
    ]

    for label, value in details:
        story.append(Paragraph(f"<b>{label}:</b> {value}", styles['Normal']))
        story.append(Spacer(1, 10))

    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer

# Simple prediction function (no imports needed)
def get_prediction(image_path):
    # This is a simplified version that doesn't rely on external imports
    # In a real app, this would process the image and use a trained model
    
    # Simulated prediction values for demo
    predictions = {
        "normal": random.uniform(0, 0.4),
        "benign": random.uniform(0, 0.3),
        "potentially_malignant": random.uniform(0, 0.7),
        "malignant": random.uniform(0, 0.6)
    }
    
    # Find the class with highest probability
    max_class = max(predictions, key=predictions.get)
    confidence = predictions[max_class]
    
    # Generate appropriate response based on prediction
    if max_class == "normal":
        prediction = "Normal tissue"
        message = "No abnormal features detected. Regular check-ups recommended."
    elif max_class == "benign":
        prediction = "Benign abnormality"
        message = "Non-cancerous abnormality detected. Follow-up may be recommended."
    elif max_class == "potentially_malignant":
        prediction = "Potentially cancerous"
        message = "Potentially cancerous features detected. Clinical evaluation strongly recommended."
    else:  # malignant
        prediction = "Highly suspicious for cancer"
        message = "Features highly suggestive of cancer. Immediate clinical evaluation required."
    
    return {
        "prediction": prediction,
        "confidence": confidence,
        "message": message
    }

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('logged_in') != True:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/about')
def about():
    return render_template('about.html', logged_in=session.get('logged_in'))

@app.route('/predict', methods=['POST'])
@login_required
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Get prediction
        result = get_prediction(file_path)
        
        # Add timestamp
        result['date'] = datetime.now().strftime("%Y-%m-%d %H:%M")
        result['image_path'] = file_path
        
        return jsonify(result)
    
    return jsonify({'error': 'File type not allowed'})

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Simple hardcoded check (replace with proper authentication)
        if username == 'admin' and password == 'password':
            session['logged_in'] = True
            return redirect(url_for('analyze'))
        else:
            return render_template('login.html', error='Invalid credentials', logged_in=session.get('logged_in'))
            
    return render_template('login.html', logged_in=session.get('logged_in'))

@app.route('/analyze')
@login_required
def analyze():
    return render_template('analyze.html', logged_in=session.get('logged_in'))

# Route to serve images from the 'images' directory
@app.route('/images/<filename>')
def serve_image(filename):
    return send_from_directory('images', filename)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Basic validation
        if not username or not email or not password or not confirm_password:
            return render_template('signup.html', error='All fields are required', logged_in=session.get('logged_in'))
        
        if password != confirm_password:
            return render_template('signup.html', error='Passwords do not match', logged_in=session.get('logged_in'))
        
        # Here you would typically:
        # 1. Check if username/email already exists
        # 2. Hash the password
        # 3. Store in database
        # For now, we'll just redirect to login
        return redirect(url_for('login'))
            
    return render_template('signup.html', logged_in=session.get('logged_in'))

@app.route('/history')
@login_required
def get_history():
    history = load_history()
    return jsonify(history)

@app.route('/history/add', methods=['POST'])
@login_required
def add_to_history():
    data = request.json
    history = load_history()
    
    # Add new analysis to history
    analysis_entry = {
        'id': len(history) + 1,
        'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
        'prediction': data['prediction'],
        'confidence': data['confidence'],
        'message': data['message'],
        'image_path': data['image_path']
    }
    
    history.append(analysis_entry)
    save_history(history)
    
    return jsonify({'success': True, 'id': analysis_entry['id']})

@app.route('/history/delete/<int:analysis_id>', methods=['DELETE'])
@login_required
def delete_from_history(analysis_id):
    history = load_history()
    history = [item for item in history if item['id'] != analysis_id]
    save_history(history)
    return jsonify({'success': True})

@app.route('/history/filter/<filter_type>')
@login_required
def filter_history(filter_type):
    history = load_history()
    if filter_type != 'all':
        filtered = [item for item in history if filter_type.lower() in item['prediction'].lower()]
        return jsonify(filtered)
    return jsonify(history)

@app.route('/compare/<int:current_id>/<int:previous_id>')
@login_required
def compare_analyses(current_id, previous_id):
    history = load_history()
    current = next((item for item in history if item['id'] == current_id), None)
    previous = next((item for item in history if item['id'] == previous_id), None)
    
    if current and previous:
        return jsonify({
            'current': current,
            'previous': previous
        })
    return jsonify({'error': 'Analyses not found'}), 404

@app.route('/report/<int:analysis_id>')
@login_required
def generate_report(analysis_id):
    history = load_history()
    analysis = next((item for item in history if item['id'] == analysis_id), None)
    
    if analysis:
        pdf_buffer = generate_pdf_report(analysis, analysis['image_path'])
        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name=f"analysis_report_{analysis_id}.pdf",
            mimetype='application/pdf'
        )
    return jsonify({'error': 'Analysis not found'}), 404

if __name__ == '__main__':
    port = 8000
    print(f"Starting app on port {port}...")
    app.run(debug=True, host='0.0.0.0', port=port) 