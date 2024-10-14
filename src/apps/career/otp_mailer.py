import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
import random


company_email = 'tashwani475' 
company_password = 'snabaglflmfwpmje'   

# Gmail SMTP server configuration
smtp_server = 'smtp.gmail.com'
smtp_port = 587

# Function to generate OTP
def generate_otp():
    otp = random.randint(100000, 999999)
    return otp

# Function to send OTP via email
def send_otp_mail(employee_name, to_email, otp, company_name):
    subject = "Your OTP Code"
    
    body = f"""
    Dear {employee_name},<br><br>

    Your One-Time Password (OTP) for verification is: <strong>{otp}</strong>.<br><br>

    Please enter this OTP to complete your verification process. The OTP is valid for 10 minutes.<br><br>

    If you did not request this, please ignore this email.<br><br>

    Best regards,<br>
    <strong>{company_name}</strong><br>
    
    """

    # Create message container
    msg = MIMEMultipart()
    msg['From'] = formataddr(("Ashwani Tripathi", company_email))
    msg['To'] = to_email
    msg['Subject'] = subject

    
    msg.attach(MIMEText(body, 'html'))

   
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(company_email, company_password)
        text = msg.as_string()
        server.sendmail(company_email, to_email, text)
        server.quit()
        print(f"OTP email sent to {employee_name} at {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")


# Test the OTP email functionality
if __name__ == "__main__":
    employee_name = "John Doe"
    to_email = "subodhmishra015@gmail.com"
    otp = generate_otp()
    company_name = "Mutaengine"
    send_otp_mail(employee_name, to_email, otp, company_name)


