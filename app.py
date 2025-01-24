from flask import Flask, render_template, request, flash, redirect, url_for, jsonify, abort
from data.portfolio_data import portfolio_data
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime
import uuid
import requests

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
def index():
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

@app.route('/send_chess_challenge', methods=['POST'])
def send_chess_challenge():
    data = request.json
    platform = data.get('platform')
    time_control = data.get('timeControl')
    challenger_username = data.get('challenger_username')

    # Your Chess.com username
    your_username = "your_chess_com_username"  # Replace with your username
    
    # Create challenge URL for Chess.com
    challenge_url = f"https://www.chess.com/play/online/new?opponent={your_username}"
    
    # Send email notification
    sender_email = "your_email@gmail.com"  # Replace with your Gmail
    sender_password = "your_app_password"   # Use Gmail App Password
    receiver_email = "your_email@gmail.com" # Your notification email

    # Email content
    subject = "New Chess Challenge!"
    body = f"""
    You have a new chess challenge!
    
    Challenger: {challenger_username}
    Platform: Chess.com
    Time Control: {time_control}
    
    Click here to accept the challenge: {challenge_url}
    """

    try:
        # Create message
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject

        # Add body to email
        message.attach(MIMEText(body, "plain"))

        # Create SMTP session
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(message)

        return jsonify({
            'success': True,
            'challenge_url': challenge_url,
            'message': 'Challenge sent! Check your email for notification.'
        })

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({
            'success': False,
            'message': 'Failed to send challenge. Please try again.'
        })

def get_time_control(time_control):
    time_controls = {
        'blitz': 300,      # 5 minutes
        'rapid': 600,      # 10 minutes
        'classical': 1800  # 30 minutes
    }
    return time_controls.get(time_control, 300)

@app.route('/education/<int:edu_index>')
def education_journey(edu_index):
    try:
        education = portfolio_data['education'][edu_index]
        return render_template('education_journey.html', 
                             education=education,
                             data=portfolio_data)
    except IndexError:
        return "Education entry not found", 404

if __name__ == '__main__':
    app.run(debug=True) 