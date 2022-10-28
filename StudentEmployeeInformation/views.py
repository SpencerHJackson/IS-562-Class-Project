from email.mime.text import MIMEText
import smtplib
import ssl
from django.shortcuts import render

# Create your views here.
def indexPageView(request):
    return render(request, 'StudentEmployeeInformation/index.html')

def send_email(self, subject, text):
    port = 465
    account = 'is405project@gmail.com'
    password = 'zacmtgcrbbndquhm'
    recipient = 'spencerhyrumjackson@gmail.com'
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
      server.login(account, password)
      message = text
      msg = MIMEText(message)
      msg['Subject'] = subject
      msg['To'] = recipient
      server.sendmail(account,recipient,msg.as_string())