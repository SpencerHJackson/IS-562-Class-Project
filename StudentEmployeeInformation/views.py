from email.mime.text import MIMEText
from django.http import HttpResponse
import smtplib
import ssl
from django.shortcuts import render, redirect
import mysql.connector
import pandas as pd

from StudentEmployeeInformation.models import Student, Semester, YearInProgram, UniveristyClass, StudentEmployeePosition, ISStaffMember, StudentAssignment

# Create your views here.
def indexPageView(request):

  studentRecords = Student.objects.all()

  context = {
    'studentRecords' : studentRecords,
  }

  return render(request, 'StudentEmployeeInformation/index.html', context)

def addStudentEmployeeFormPageView(request):
  semester = Semester.objects.all()
  yearInProgram = YearInProgram.objects.all()
  univeristyClass = UniveristyClass.objects.all()

  context = {
    'semester' : semester,
    'yearInProgram' : yearInProgram,
    'univeristyClass' : univeristyClass,

  }
  return render(request, 'StudentEmployeeInformation/add-user.html', context)

def addWorkAssignmentView(request, byuNumber):
  semester = Semester.objects.all()
  univeristyClass = UniveristyClass.objects.all()
  position = StudentEmployeePosition.objects.all()
  supervisor = ISStaffMember.objects.all()

  student = Student.objects.get(byu_id=byuNumber)

  context = {
    'semester' : semester,
    'univeristyClass' : univeristyClass,
    'position' : position,
    'supervisor' : supervisor,
    'student' : student,
  }

  return render(request, 'StudentEmployeeInformation/add-work-assignment.html', context)

def storeWorkAssignment(request):
  if request.method=='POST':
    byuIDNumber = request.POST.get('BYUID')
    student = Student.objects.get(byu_id=byuIDNumber)

    new_assignment=StudentAssignment()
    semesterID = request.POST.get('semester')
    new_assignment.semester = Semester.objects.get(id=semesterID)
    classID = request.POST.get('classCode')
    new_assignment.class_code = UniveristyClass.objects.get(id=classID)
    positionID = request.POST.get('positionType')
    new_assignment.position = StudentEmployeePosition.objects.get(id=positionID)
    supervisorID = request.POST.get('supervisor')
    new_assignment.supervisor = ISStaffMember.objects.get(id=supervisorID)

    new_assignment.save()

    student.work_assignments.add(new_assignment)

    return redirect('index')

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
    new_employee.increase_input_date = request.POST.get('increase_input_date')
    sYear = request.POST.get('yearInProgram')
    new_employee.year_in_program = YearInProgram.objects.get(student_year=sYear)
    new_employee.pay_grad_tuition = request.POST.get('paidTuition')
    new_employee.is_terminated = request.POST.get('Terminated')
    new_employee.terminated_date = request.POST.get('terminatedDate')
    new_employee.qualtrics_sent = request.POST.get('qualtrics')
    new_employee.eform = request.POST.get('eForm')
    new_employee.eform_date = request.POST.get('eformDate')
    new_employee.workauth = request.POST.get('authorized')
    new_employee.workauth_date = request.POST.get('authSent')
    new_employee.expected_hours = request.POST.get('expected_hours')
    new_employee.name_change = request.POST.get('nameChange')
    new_employee.byu_name = request.POST.get('inputBYUName')

# Some of these are off. We need to verify the fields we are entering are correct
    new_employee.save()
    send_email(request)

  return redirect('index')

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
  df_query = query(f"SELECT * FROM BYUIS.student_employee where byu_id = '{request.POST.get('byuid')}';")
  if len(df_query) < 1:
    text = {}
    text['alert'] = f"We don't have any student with BYU ID: {request.POST.get('byuid')}"
    return render(request, 'StudentEmployeeInformation/search_byuid.html', text)
  else:
    target_record = df_query.iloc[0].to_dict()
    target_record['phone'] = str(target_record['phone']) if target_record['phone'] is not None else 'xxx-xxx-xxxx'
    target_record['hire_date'] = str(target_record['hire_date']) if target_record['hire_date'] is not None else '0001-01-01'
    target_record['last_pay_increase'] = str(target_record['last_pay_increase']) if target_record['last_pay_increase'] is not None else '0001-01-01'
    target_record['pay_rate'] = str(target_record['pay_rate']) if target_record['pay_rate'] is not None else '0'
    target_record['pay_increase_amount'] = str(target_record['pay_increase_amount']) if target_record['pay_increase_amount'] is not None else '0'
    target_record['workauth_date'] = str(target_record['workauth_date']) if target_record['workauth_date'] is not None else '0001-01-01'
    target_record['terminated_date'] = str(target_record['terminated_date']) if target_record['terminated_date'] is not None else '0001-01-01'
    target_record['gender'] = '' if target_record['gender'] is None else target_record['gender'] 
    target_record['employee_record'] = '' if target_record['employee_record'] is None else target_record['employee_record']
    if target_record['position_id'] == 1:
      target_record['position_id'] = 'TA'
    elif target_record['position_id'] == 2:
      target_record['position_id'] = 'RA'
    elif target_record['position_id'] == 3:
      target_record['position_id'] = 'Office'
    elif target_record['position_id'] == 4:
      target_record['position_id'] = 'Student Instructor'
    elif target_record['position_id'] == 5:
      target_record['position_id'] = 'Other'
    else:
      target_record['position_id'] = ''
    
    if target_record['year_in_program_id'] == 1:
      target_record['year_in_program_id'] = 'MISM'
    elif target_record['year_in_program_id'] == 2:
      target_record['year_in_program_id'] = 'MBA'
    elif target_record['year_in_program_id'] == 3:
      target_record['year_in_program_id'] = 'MPA'
    elif target_record['year_in_program_id'] == 4:
      target_record['year_in_program_id'] = 'MAcc'
    elif target_record['year_in_program_id'] == 5:
      target_record['year_in_program_id'] = 'Other Major'
    else:
      target_record['year_in_program_id'] = ''

    return render(request, 'StudentEmployeeInformation/edit-user.html', target_record)

def save_record(request):
  target_record = Student.objects.get(byu_id=request.POST.get('BYUID'))
  target_record.first_name = request.POST.get('inputFirstName')
  target_record.last_name = request.POST.get('inputLastName')
  target_record.international_student = request.POST.get('international')
  target_record.gender = request.POST.get('gender')
  target_record.email = request.POST.get('inputEmail')
  target_record.phone = request.POST.get('phoneNumber')
  target_record.byu_id = request.POST.get('BYUID')
  target_record.employee_record = request.POST.get('employeeRecord')
  target_record.hire_date = request.POST.get('hireDate')
  target_record.pay_rate = request.POST.get('payRate')
  target_record.last_pay_increase = request.POST.get('lastPayRaise')
  target_record.pay_increase_amount = request.POST.get('payRateIncrease')
  # target_record.increase_input_date = request.POST.get('inputFirstName')
  target_record.pay_grad_tuition = request.POST.get('paidTuition')
  target_record.is_terminated = request.POST.get('Terminated')
  target_record.terminated_date = request.POST.get('terminatedDate')
  target_record.qualtrics_sent = request.POST.get('qualtrics')
  target_record.eform = request.POST.get('eForm')
  #target_record.eform_date = request.POST.get('inputFirstName')
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