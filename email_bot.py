import smtplib
import json
from email.mime.text import MIMEText

# Load SMTP config
with open('config.json', 'r') as f:
    config = json.load(f)

smtp_server = config.get('smtp_server', 'smtp.example.com')
smtp_port = config.get('smtp_port', 587)
smtp_user = config.get('smtp_user', 'user@example.com')
smtp_password = config.get('smtp_password', 'password')

# Load email list
with open('email_list.txt', 'r') as f:
    emails = [line.strip() for line in f if line.strip()]

subject = "Automated Outreach"
body = "Hello, this is an automated email from our AI-driven lead system."

msg = MIMEText(body)
msg['Subject'] = subject
msg['From'] = smtp_user

server = smtplib.SMTP(smtp_server, smtp_port)
server.starttls()
server.login(smtp_user, smtp_password)

for email in emails:
    msg['To'] = email
    server.sendmail(smtp_user, email, msg.as_string())
    print(f"Email sent to {email}")

server.quit()
