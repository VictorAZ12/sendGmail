import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os
import time
# Configurations
sender_email = "yours@email.com"
sender_password = "your google app password"
attachment_path = "attachment.pdf"
template_path = "template.txt"
subject = "your email subject [substitution_string]"
substitution = "[substitution_string]"
recipient_path = "recipient.csv"
send_gap = 5.0
# construct email
def construct_email(substitution_str, recipient_name, recipient_email, sender_email, subject_str, template_str, attachment_path=None):
    # Create message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject_str.replace(substitution_str, recipient_name)
    message_content_html = template_str.replace(substitution_str, recipient_name)
    # Attach plain text and HTML versions of the message
    msg.attach(MIMEText(message_content_html, 'html'))

    # Attach the pdf file, if provided
    if attachment_path:
        with open(attachment_path, "rb") as attachment:
            attached_file = MIMEApplication(attachment.read(), _subtype="pdf")
            attached_file.add_header("content-disposition", f"attachment; filename={os.path.basename(attachment_path)}")
            msg.attach(attached_file)

    return msg.as_string()


def main():
    # read in recipients
    with open(recipient_path, "r") as f:
        recipients = [line.rstrip() for line in f.readlines()] 
    # read in email template
    with open(template_path, "r") as f:
        template = f.read()
    
    try:
        # sender mail login
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            for recipient in recipients:
                recipient_name = recipient.split(",")[0]
                recipient_email = recipient.split(",")[1]
                personalized_email = construct_email(
                    substitution_str = substitution,
                    recipient_name = recipient_name,
                    recipient_email = recipient_email,
                    sender_email = sender_email,
                    subject_str = subject,
                    template_str = template, 
                    attachment_path = attachment_path
                )
                server.sendmail(sender_email, recipient_email, personalized_email)
                print(f"Email sent to {recipient_name} at {recipient_email}. Next email to be sent in {send_gap} seconds.")
                time.sleep(send_gap)
            print("All eamils sent.")
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    main()
