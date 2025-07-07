import smtplib
from email.message import EmailMessage

msg = EmailMessage()
msg.set_content("This is a standalone test email from test_email_send.py.")
msg['Subject'] = "Test Email"
msg['From'] = "noreeynoor@gmail.com"
msg['To'] = "mahnoorsaleemmahnoor7@gmail.com"  # ← apna doosra email yahan daalo

try:
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login("noreeynoor@gmail.com", "fpzbvlwykiiomdjg")  # 👈 paste app password here
        server.send_message(msg)
    print("✅ Email sent successfully.")

except smtplib.SMTPAuthenticationError as e:
    print("❌ SMTP AUTH ERROR:", e.smtp_error.decode())
except Exception as ex:
    print("❌ GENERAL ERROR:", str(ex))
