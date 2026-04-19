import smtplib
import ssl
import csv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# --- CONFIGURATION ---
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "xxxxxxxxxxxxxxxxxxxx"
SENDER_PASSWORD = "xxxxxxxxxxxxxxxxx"  # Use the App Password here

def send_automated_emails(csv_file, subject, resume_path=None):
    # Create a secure SSL context
    context = ssl.create_default_context()

    try:
        # 1. Connect to the server
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls(context=context) # Secure the connection
        server.login(SENDER_EMAIL, SENDER_PASSWORD)

        # 2. Open and read the CSV
        with open(csv_file, mode='r') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                recipient_name = row['name']
                recipient_email = row['email']
                company_name = row['company']

                # 3. Create the "Envelope" (MIME object)
                message = MIMEMultipart()
                message["From"] = SENDER_EMAIL
                message["To"] = recipient_email
                message["Subject"] = subject

                # 4. Personalize the body
                body = f"""
                Hi {recipient_name},

                I am reaching out to express my interest in potential opportunities at {company_name}.
                Please find my resume attached for your review.

                Best regards,
                Your Name
                """
                message.attach(MIMEText(body, "plain"))

                # 5. Attach a file (Optional)
                if resume_path:
                    with open(resume_path, "rb") as f:
                        attachment = MIMEApplication(f.read(), _subtype="pdf")
                        attachment.add_header('Content-Disposition', 'attachment', filename="Resume.pdf")
                        message.attach(attachment)

                # 6. Send the email
                server.sendmail(SENDER_EMAIL, recipient_email, message.as_string())
                print(f"Successfully sent to {recipient_name} at {company_name}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        server.quit()

# --- RUN THE SYSTEM ---
send_automated_emails("contacts.csv", "Inquiry regarding opportunities", "myresume.pdf")
