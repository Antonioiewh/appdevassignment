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

def send_review_notifcation_gmail():
    pass

send_liked_notification_gmail("240582Q@mymail.nyp.edu.sg","hermos")