from email.mime.text import MIMEText
from django.http import HttpResponse
import smtplib
import ssl
from django.shortcuts import render

from StudentEmployeeInformation.models import Students

# Create your views here.
def indexPageView(request):
    return render(request, 'StudentEmployeeInformation/index.html')

def addStudentEmployeeFormPageView(request):
    return render(request, 'StudentEmployeeInformation/add-user.html')

def storeStudentEmployeePageView(request):
  if request.method=='POST':
    new_employee=Students()
    new_employee.first_name = request.POST.get('inputFirstName')

    new_employee.save()

  return render(request, 'StudentEmployeeInformation/index.html')

def send_email(request):
    port = 465
    account = 'is405project@gmail.com'
    password = 'zacmtgcrbbndquhm'
    recipient = request.POST.get('recipient')
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
      server.login(account, password)
      message = request.POST.get('text')
      msg = MIMEText(message)
      msg['Subject'] = request.POST.get('subject')
      msg['To'] = recipient
      server.sendmail(account,recipient,msg.as_string())

    return HttpResponse("Email was sent!")