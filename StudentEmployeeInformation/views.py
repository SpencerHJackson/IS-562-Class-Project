from email.mime.text import MIMEText
from django.http import HttpResponse
import smtplib
import ssl
from django.shortcuts import render
import mysql.connector
import pandas as pd

from StudentEmployeeInformation.models import Student

# Create your views here.
def indexPageView(request):

  studentRecords = Student.objects.all()

  context = {
    'studentRecords' : studentRecords,
  }

  return render(request, 'StudentEmployeeInformation/index.html', context)

def addStudentEmployeeFormPageView(request):
    return render(request, 'StudentEmployeeInformation/add-user.html')

def storeStudentEmployeePageView(request):
  if request.method=='POST':
    new_employee=Student()
    new_employee.first_name = request.POST.get('inputFirstName')
    new_employee.last_name = request.POST.get('inputLastName')
    new_employee.international_student = request.POST.get('international')
    new_employee.gender = request.POST.get('gender')
    new_employee.email = request.POST.get('inputEmail')
    #new_employee.semester = request.POST.get('semester') This will be replaced
    #new_employee.calendar_year = request.POST.get('year') This will be replaced
    new_employee.phone = request.POST.get('phoneNumber')
    new_employee.byu_id = request.POST.get('BYUID')
    #new_employee.position = request.POST.get('positionType') changed
    #new_employee.class_code = request.POST.get('classCode') this will be replaced
    new_employee.employee_record = request.POST.get('employeeRecord')
    #new_employee.supervisor = request.POST.get('inputFirstName') changed
    new_employee.hire_date = request.POST.get('hireDate')
    new_employee.pay_rate = request.POST.get('payRate')
    new_employee.last_pay_increase = request.POST.get('lastPayRaise')
    new_employee.pay_increase_amount = request.POST.get('payRateIncrease')
    new_employee.increase_input_date = request.POST.get('inputFirstName')
    #new_employee.year_in_program = request.POST.get('yearInProgram') changed
    new_employee.pay_grad_tuition = request.POST.get('paidTuition')
    new_employee.is_terminated = request.POST.get('Terminated')
    new_employee.terminated_date = request.POST.get('terminatedDate')
    new_employee.qualtrics_sent = request.POST.get('qualtrics')
    new_employee.eform = request.POST.get('eForm')
    new_employee.eform_date = request.POST.get('inputFirstName')
    new_employee.workauth = request.POST.get('authorized')
    new_employee.workauth_date = request.POST.get('authSent')

# Some of these are off. We need to verify the fields we are entering are correct
    new_employee.save()
    send_email(request)

  return render(request, 'StudentEmployeeInformation/index.html')

def send_email(request):
    port = 465
    account = 'is405project@gmail.com'
    password = 'zacmtgcrbbndquhm'
    recipient = request.POST.get('inputEmail')
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
      server.login(account, password)
      message = request.POST.get('messageText')
      msg = MIMEText(message)
      msg['Subject'] = request.POST.get('messageSubject')
      msg['To'] = recipient
      server.sendmail(account,recipient,msg.as_string())

def tableauView(request):
    return render(request, 'StudentEmployeeInformation/tableau.html')

    
def query(query):
  mydb = mysql.connector.connect(host="rds-terraform.ccme3kf5lctp.us-east-2.rds.amazonaws.com", user="admin", password="is562section2classproject")
  df_query = pd.read_sql(query, mydb)
  return df_query

def search_byuid(request):
  return render(request, 'StudentEmployeeInformation/search_byuid.html')

def edit_record(request):
  df_query = query(f"SELECT * FROM BYUIS.students where byuid = '{request.POST.get('byuid')}';")
  if len(df_query) < 1:
    text = {}
    text['alert'] = f"We don't have any student with BYU ID: {request.POST.get('byuid')}"
    return render(request, 'StudentEmployeeInformation/search_byuid.html', text)
  else:
    target_record = df_query.iloc[0].to_dict()
    target_record['calendaryear'] = target_record['calendaryear'][0:4]
    target_record['hiredate'] = str(target_record['hiredate'])
    target_record['lastpayincrease'] = str(target_record['lastpayincrease'])
    target_record['workauthdate'] = str(target_record['workauthdate'])
    target_record['terminateddate'] = str(target_record['terminateddate']) if target_record['terminateddate'] is not None else '0000-00-00'
    #target_record['semester'] = '' if target_record['semester'] is None else target_record['semester'] 
    #target_record['calendaryear'] = '' if target_record['calendaryear'] is None else target_record['calendaryear'] 
    target_record['gender'] = '' if target_record['gender'] is None else target_record['gender'] 
    target_record['yearinprogram'] = '' if target_record['yearinprogram'] is None else target_record['yearinprogram']
    #target_record['class_code'] = '' if target_record['class_code'] is None else target_record['class_code']
    target_record['employee_record'] = '' if target_record['employee_record'] is None else target_record['employee_record']
    #target_record['position'] = '' if target_record['position'] is None else target_record['position'] changed
    return render(request, 'StudentEmployeeInformation/edit-user.html', target_record)

def save_record(request):
  print(request.POST.get('BYUID'))
  df_query = query(f"SELECT id FROM BYUIS.students where byuid = '{request.POST.get('BYUID')}';")
  target_record = Student.objects.get(byuid=request.POST.get('BYUID'))
  target_record.first_name = request.POST.get('inputFirstName')
  target_record.last_name = request.POST.get('inputLastName')
  target_record.international_student = request.POST.get('international')
  target_record.gender = request.POST.get('gender')
  target_record.email = request.POST.get('inputEmail')
  #target_record.semester = request.POST.get('semester')
  #target_record.calendar_year = request.POST.get('year')
  target_record.phone = request.POST.get('phoneNumber')
  target_record.byu_id = request.POST.get('BYUID')
  #target_record.position = request.POST.get('positionType') changed
  #target_record.class_code = request.POST.get('classCode')
  target_record.employee_record = request.POST.get('employeeRecord')
  #target_record.supervisor = request.POST.get('inputFirstName') changed
  target_record.hire_date = request.POST.get('hireDate')
  target_record.pay_rate = request.POST.get('payRate')
  target_record.last_pay_increase = request.POST.get('lastPayRaise')
  target_record.pay_increase_amount = request.POST.get('payRateIncrease')
  target_record.increase_input_date = request.POST.get('inputFirstName')
  #target_record.year_in_program = request.POST.get('yearInProgram') changed
  target_record.pay_grad_tuition = request.POST.get('paidTuition')
  target_record.is_terminated = request.POST.get('Terminated')
  target_record.terminated_date = request.POST.get('terminatedDate')
  target_record.qualtrics_sent = request.POST.get('qualtrics')
  target_record.eform = request.POST.get('eForm')
  target_record.eform_date = request.POST.get('inputFirstName')
  target_record.workauth = request.POST.get('authorized')
  target_record.workauth_date = request.POST.get('authSent')

# Some of these are off. We need to verify the fields we are entering are correct
  target_record.save()
  text={}
  text['alert'] = 'Update success!' 
  return render(request, 'StudentEmployeeInformation/search_byuid.html', text)


def loginView(request):
    return render(request, 'StudentEmployeeInformation/login.html')
    

def addloginView(request):
    return render(request, 'StudentEmployeeInformation/newlogin.html')