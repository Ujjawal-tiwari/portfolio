from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from data.portfolio_data import portfolio_data
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime
import uuid

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Required for flash messages

# Email configuration
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USER = 'your-email@gmail.com'  # Your Gmail address
EMAIL_PASSWORD = 'your-app-password'  # Your Gmail app password

def send_email(name, email, message):
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USER
        msg['To'] = EMAIL_USER  # Sending to yourself
        msg['Subject'] = f"Portfolio Contact from {name}"

        # Email body
        body = f"""
        You have received a new message from your portfolio website:

        Name: {name}
        Email: {email}
        Message:
        {message}
        """
        msg.attach(MIMEText(body, 'plain'))

        # Create SMTP session
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)

        # Send email
        text = msg.as_string()
        server.sendmail(EMAIL_USER, EMAIL_USER, text)
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

@app.route('/')
def home():
    return render_template('index.html', data=portfolio_data)

@app.route('/about')
def about():
    return render_template('about.html', data=portfolio_data)

@app.route('/projects')
def projects():
    return render_template('projects.html', data=portfolio_data)

@app.route('/skills')
def skills():
    return render_template('skills.html', data=portfolio_data)

@app.route('/experience')
def experience():
    return render_template('experience.html', data=portfolio_data)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        if name and email and message:
            if send_email(name, email, message):
                flash('Your message has been sent successfully!', 'success')
            else:
                flash('There was an error sending your message. Please try again.', 'error')
        else:
            flash('Please fill in all fields.', 'error')
        
        return redirect(url_for('contact'))
    
    return render_template('contact.html', data=portfolio_data)

@app.route('/communities')
def communities():
    return render_template('communities.html', data=portfolio_data)

@app.route('/side-hustles')
def side_hustles():
    return render_template('side_hustles.html', data=portfolio_data)

@app.route('/send-chess-challenge', methods=['POST'])
def send_chess_challenge():
    try:
        challenger_name = request.form.get('challenger_name')
        challenger_email = request.form.get('challenger_email')
        time_control = request.form.get('time_control')
        
        # Generate a unique game ID
        game_id = str(uuid.uuid4())[:8]
        
        # Create Lichess challenge link (you'll need to set this up with Lichess API)
        lichess_username = portfolio_data['chess_profile']['lichess_username']
        challenge_link = f"https://lichess.org/?user={lichess_username}#friend"
        
        # Email content
        subject = f"New Chess Challenge from {challenger_name}"
        body = f"""
        You have a new chess challenge!
        
        Challenger: {challenger_name}
        Email: {challenger_email}
        Time Control: {time_control}
        Game ID: {game_id}
        
        Challenge Link: {challenge_link}
        
        Respond to accept the challenge!
        """
        
        # Send email
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USER
        msg['To'] = EMAIL_USER  # Sending to yourself
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        return jsonify({
            'success': True,
            'message': 'Challenge sent successfully! Check your email for the game link.'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Error sending challenge. Please try again.'
        }), 500

if __name__ == '__main__':
    app.run(debug=True) 