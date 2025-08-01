import smtplib
from email.mime.text import MIMEText
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("SMPTSender")

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "krishnabudumuru7@gmail.com"
APP_PASSWORD = "YOUR_OWN_APP_PASSWORD"

@mcp.tool()
def send_email(to, subject, body):
    """Send an email using SMTP"""
    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = SENDER_EMAIL
        msg["To"] = to

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.send_message(msg)

        return {"status": "success", "message": f"Email sent to {to}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
if __name__ == '__main__':
    mcp.run(transport='stdio')
