import smtplib
from email.mime.text import MIMEText

#shld work with all
sender = "noreplyapp1001@gmail.com" #email we are using
password = "fmpt ugpt hhpp kvsw" #password for it

def send_liked_notification_gmail(recipient_email,customer_username):
    try:#just do dealer.get_email or smth
        msg = MIMEText(f"{customer_username} has liked your post!") #insert email content here
        msg['Subject'] = "Notification from freesell"
        msg['From'] = sender
        msg['To'] = recipient_email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, recipient_email, msg.as_string())
        print(f"Notification sent to {recipient_email}!")
    except:
        print("Error in sending email")

def send_signup_notification_gmail(recipient_email,recipient_username):
    try:
        msg = MIMEText(f"Welcome{recipient_username} to freesell!")
        msg['Subject'] = 'Notification from freesell'
        msg['From'] = sender
        msg['To'] = recipient_email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, recipient_email, msg.as_string())
        print(f"Notification sent to {recipient_email}!")
    except:
        print("Error in sending email")

def send_review_notifcation_gmail(recipient_email,recipient_username,reviewer_username,review_content):
    try:
        msg = MIMEText(f"{reviewer_username} left a review, {review_content}")
        msg['Subject'] = 'Notification from freesell'
        msg['From'] = sender
        msg['To'] = recipient_email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, recipient_email, msg.as_string())
        print(f"Notification sent to {recipient_email}!")
    except:
        print("Error in sending email")

def send_message_notifcation_gmail(recipient_email, recipient_username,sender_username,message_content):
    try:
        msg = MIMEText(f"{recipient_username}, you have 1 new message from {sender_username}:\n{message_content}")
        msg['From'] = sender
        msg['To'] = recipient_email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, recipient_email, msg.as_string())
        print(f"Notification sent to {recipient_email}!")
    except:
        print("Error in sending email")
def send_message_operator_OTP(recipient_email,OTP):
    try:
        msg = MIMEText(f"your one time password is {OTP}")
        msg['From'] = sender
        msg['To'] = recipient_email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, recipient_email, msg.as_string())
        print(f"Notification sent to {recipient_email}!")  
    except:
        print("Error in sending email")


