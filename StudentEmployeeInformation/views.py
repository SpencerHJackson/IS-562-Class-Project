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
    new_employee.last_name = request.POST.get('inputLastName')
    new_employee.international = request.POST.get('international')
    new_employee.gender = request.POST.get('gender')
    new_employee.email = request.POST.get('inputEmail')
    new_employee.semester = request.POST.get('semester')
    new_employee.calendaryear = request.POST.get('year')
    new_employee.phone = request.POST.get('phoneNumber')
    new_employee.byuid = request.POST.get('BYUID')
    new_employee.position = request.POST.get('positionType')
    new_employee.class_code = request.POST.get('classCode')
    new_employee.employee_record = request.POST.get('employeeRecord')
    new_employee.supervisor = request.POST.get('inputFirstName')
    new_employee.hiredate = request.POST.get('hireDate')
    new_employee.payrate = request.POST.get('payRate')
    new_employee.lastpayincrease = request.POST.get('lastPayRaise')
    new_employee.payincreaseamount = request.POST.get('payRateIncrease')
    new_employee.increaseinputdate = request.POST.get('inputFirstName')
    new_employee.yearinprogram = request.POST.get('yearInProgram')
    new_employee.paygradtuition = request.POST.get('paidTuition')
    new_employee.isterminated = request.POST.get('Terminated')
    new_employee.terminateddate = request.POST.get('terminatedDate')
    new_employee.qualtricssent = request.POST.get('qualtrics')
    new_employee.eform = request.POST.get('eForm')
    new_employee.eformdate = request.POST.get('inputFirstName')
    new_employee.workauth = request.POST.get('authorized')
    new_employee.workauthdate = request.POST.get('authSent')

# Some of these are off. We need to verify the fields we are entering are correct
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