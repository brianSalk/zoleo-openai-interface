import imaplib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import email
from os import getenv
from openai import OpenAI


from email.utils import parseaddr

client = OpenAI(api_key=getenv("OPENAI_KEY"))

def get_ai_response(prompt: str, model_name: str) -> str:
    completion = client.chat.completions.create(
          model=model_name,
          messages=[
            {"role": "system", "content": "You are accurate and keep all answers as short as possible."},
            {"role": "user", "content": prompt}
          ]
    )
    return completion.choices[0].message


def extract_sender_email(raw_email_data):
    """
    Extract the sender's email address from raw email data.

    :param raw_email_data: The raw email data as bytes.
    :return: Sender's email address.
    """
    # Parse the raw email data
    msg = email.message_from_bytes(raw_email_data)

    # Extract the 'From' header
    from_header = msg["From"]
    if from_header:
        # Parse the address to extract just the email
        sender_name, sender_email = parseaddr(from_header)
        return sender_email
    return None


# Example usage
raw_email = b"""From: John Doe <johndoe@example.com>
To: Your Name <yourname@example.com>
Subject: Test Email

This is a test email.
"""
print(extract_sender_email(raw_email))  # Output: johndoe@example.com



# Email credentials
EMAIL = getenv('EMAIL')
PASSWORD = getenv('PASSWORD')
IMAP_SERVER = "imap.gmail.com"  # e.g., "imap.gmail.com" for Gmail
SMTP_SERVER = "smtp.gmail.com"  # e.g., "smtp.gmail.com" for Gmail
SMTP_PORT = 587  # For TLS

def read_emails():
    """Reads unread emails."""
    try:
        # Connect to the IMAP server
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL, PASSWORD)
        mail.select("inbox")  # Connect to the inbox
        print('connected successfully')
        # Search for unread emails
        status, messages = mail.search(None, 'UNSEEN')
        email_ids = messages[0].split()
        emails = []
        for email_id in email_ids:
            # Fetch the email
            status, msg_data = mail.fetch(email_id, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject = msg["subject"]
                    sender = msg["from"]

                    # Get the email body
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                body = part.get_payload(decode=True).decode()
                                break
                    else:
                        body = msg.get_payload(decode=True).decode()

                    emails.append({
                        "subject": subject,
                        "sender": sender,
                        "body": body,
                    })
                    print(f"Email from {sender} with subject '{subject}': {body}")

        mail.logout()
        return emails

    except Exception as e:
        print(f"Error reading emails: {e}")
        return []

def send_email(to_email, subject, body):
    """Sends an email."""
    try:
        # Connect to the SMTP server
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL, PASSWORD)

        # Create the email
        message = MIMEMultipart()
        message["From"] = EMAIL
        message["To"] = to_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        # Send the email
        server.sendmail(EMAIL, to_email, message.as_string())
        server.quit()
        print(f"Email sent to {to_email}")

    except Exception as e:
        print(f"Error sending email: {e}")

def main():
    # Step 1: Read unread emails
    emails = read_emails()
    # Step 2: Respond programmatically
    print(f'{emails=}')
    for email in emails:
        sender = email["sender"]

        subject = email["subject"]
        body = email["body"]

        # Create a response if it is from a zoleo account
        if 'zoleo' in sender.lower():
            response_subject = ""
            #response_body = get_ai_response(body)
            response_body = f"this is a test email from chatman"

        # Send the response
        send_email(sender, response_subject, response_body)

if __name__ == "__main__":
    main()
