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
  csv = 'teacher_first, teacher_last, student_first, spencer_last, internation_student, gender, email, phone, byu_id, position_id, employee_record, supervisor_id, hire_date, pay_rate, last_pay_increase, pay_increase_amount, increase_input_date\n';   
  csv2 = 'first_name, last_name, internation_student, gender, email, phone, byu_id, position_id, employee_record, supervisor_id, hire_date, pay_rate, last_pay_increase, pay_increase_amount, increase_input_date\n';  
  csv3 = 'first_name, last_name, internation_student, gender, email, phone, byu_id, position_id, employee_record, supervisor_id, hire_date, pay_rate, last_pay_increase, pay_increase_amount, increase_input_date\n';   
 
  mydb = mysql.connector.connect(host="rds-terraform.ccme3kf5lctp.us-east-2.rds.amazonaws.com", user="admin", password="is562section2classproject", database="BYUIS")
  query = "select is_staff.first_name, is_staff.last_name, student_employee.* from is_staff inner join student_assignment on is_staff.id = student_assignment.supervisor_id  inner join student_employee_work_assignments on student_assignment.id = student_employee_work_assignments.studentassignment_id inner join student_employee on student_employee_work_assignments.student_id = student_employee.byu_id where is_terminated is false order by supervisor_id"
  # df_query = pd.read_sql(query, mydb)
  cursor = mydb.cursor(prepared=True)
  cursor.execute(query)
  records = cursor.fetchall()
  
  # cursor = mydb.cursor(prepared=True)
  for row in records:
    csv += row[0] + ", " + row[1] + ', ' + str(row[2]) + ', ' + str(row[3]) + ', ' + str(row[4]) + ', ' + str(row[5]) + ', ' + str(row[6]) + ', ' + str(row[7]) + ', ' + str(row[8]) + ', ' + str(row[9]) + ', ' + str(row[10]) + ', ' + str(row[11]) + ', ' + str(row[12]) + ', ' + str(row[13]) + ", " + str(row[14]) + ", " + str(row[15]) + ", " + str(row[16]) + ", " + str(row[17]) + ", " + str(row[18]) + ", " + str(row[19]) + ", " + str(row[20]) + ", " + str(row[21]) + ", " + str(row[22]) + ", " + str(row[23]) + ", " + str(row[24]) + ", " + str(row[25]) + "\r\n"
  
  csvfixed = str(csv)

  query2 = "select * from student_employee where is_terminated is false"
  # df_query = pd.read_sql(query, mydb)
  cursor2 = mydb.cursor(prepared=True)
  cursor2.execute(query2)
  records2 = cursor2.fetchall()

  for row in records2:
    csv2 += row[0] + ", " + row[1] + ', ' + str(row[2]) + ', ' + str(row[3]) + ', ' + str(row[4]) + ', ' + str(row[5]) + ', ' + str(row[6]) + ', ' + str(row[7]) + ', ' + str(row[8]) + ', ' + str(row[9]) + ', ' + str(row[10]) + ', ' + str(row[11]) + ', ' + str(row[12]) + ', ' + str(row[13]) + ", " + str(row[14]) + ", " + str(row[15]) + ", " + str(row[16]) + ", " + str(row[17]) + ", " + str(row[18]) + ", " + str(row[19]) + ", " + str(row[20]) + ", " + str(row[21]) + ", " + str(row[22]) + ", " + str(row[23]) + ", " + str(row[24]) + ", " + str(row[25]) + "\r\n"

  csvfixed2 = str(csv2)

  query3 = "select * from student_employee"
  # df_query = pd.read_sql(query, mydb)
  cursor3 = mydb.cursor(prepared=True)
  cursor3.execute(query3)
  records3 = cursor3.fetchall()

  for row in records3:
    csv3 += row[0] + ", " + row[1] + ', ' + str(row[2]) + ', ' + str(row[3]) + ', ' + str(row[4]) + ', ' + str(row[5]) + ', ' + str(row[6]) + ', ' + str(row[7]) + ', ' + str(row[8]) + ', ' + str(row[9]) + ', ' + str(row[10]) + ', ' + str(row[11]) + ', ' + str(row[12]) + ', ' + str(row[13]) + ", " + str(row[14]) + ", " + str(row[15]) + ", " + str(row[16]) + ", " + str(row[17]) + ", " + str(row[18]) + ", " + str(row[19]) + ", " + str(row[20]) + ", " + str(row[21]) + ", " + str(row[22]) + ", " + str(row[23]) + ", " + str(row[24]) + ", " + str(row[25]) + "\r\n"

  csvfixed3 = str(csv3)

  studentRecords = Student.objects.all()
  


  context = {
    'studentRecords' : studentRecords,
    'loadcsv1' : csvfixed, 
    'loadcsv2' : csvfixed2,
    'loadcsv3' : csvfixed3
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

    if request.POST.get('lastPayRaise') == "":
      lastPayRaiseCleaned = None
    else:
      lastPayRaiseCleaned = request.POST.get('lastPayRaise')
      


    if request.POST.get('increase_input_date') == "":
      inputRateIncrease = None
    else:
      inputRateIncrease = request.POST.get('increase_input_date')



    if request.POST.get('authSent') == "":
      authSentClean = None
    else:
      authSentClean = request.POST.get('authSent')



    if request.POST.get('eformDate') == "":
      eFormClean = None
    else:
      eFormClean = request.POST.get('eformDate')
      


    if request.POST.get('terminatedDate') == "":
      TermDateCleaned = None
    else:
      TermDateCleaned = request.POST.get('terminatedDate')



    if request.POST.get('payRateIncrease') == "":
     payRateIncreaseCleaned = None
    else:
     payRateIncreaseCleaned = request.POST.get('payRateIncrease')



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
    new_employee.last_pay_increase = lastPayRaiseCleaned
    new_employee.pay_increase_amount = payRateIncreaseCleaned
    new_employee.increase_input_date = inputRateIncrease
    sYear = request.POST.get('yearInProgram')
    new_employee.year_in_program = YearInProgram.objects.get(student_year=sYear)
    new_employee.pay_grad_tuition = request.POST.get('paidTuition')
    new_employee.is_terminated = request.POST.get('Terminated')
    new_employee.terminated_date = TermDateCleaned
    new_employee.qualtrics_sent = request.POST.get('qualtricssent')
    new_employee.eform = request.POST.get('eForm')
    new_employee.eform_date = eFormClean
    new_employee.workauth = request.POST.get('authorized')
    new_employee.workauth_date = authSentClean
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
    target_record['eform_date'] = str(target_record['eform_date']) if target_record['eform_date'] is not None else '0001-01-01'
    target_record['increase_input_date'] = str(target_record['increase_input_date']) if target_record['increase_input_date'] is not None else '0001-01-01'
    target_record['last_pay_increase'] = str(target_record['last_pay_increase']) if target_record['last_pay_increase'] is not None else '0001-01-01'
    target_record['pay_rate'] = str(target_record['pay_rate']) if target_record['pay_rate'] is not None else '0'
    target_record['pay_increase_amount'] = str(target_record['pay_increase_amount']) if target_record['pay_increase_amount'] is not None else '0'
    target_record['workauth_date'] = str(target_record['workauth_date']) if target_record['workauth_date'] is not None else '0001-01-01'
    target_record['terminated_date'] = str(target_record['terminated_date']) if target_record['terminated_date'] is not None else '0001-01-01'
    target_record['gender'] = '' if target_record['gender'] is None else target_record['gender'] 
    target_record['employee_record'] = '' if target_record['employee_record'] is None else target_record['employee_record']
    
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
  target_record.expected_hours = request.POST.get('expected_hours')
  target_record.increase_input_date = request.POST.get('increase_input_date')
  target_record.eform_date = request.POST.get('eformDate')
  sYear = request.POST.get('yearInProgram')
  target_record.year_in_program = YearInProgram.objects.get(id=sYear)
# Some of these are off. We need to verify the fields we are entering are correct
  target_record.save()
  text={}
  text['alert'] = 'Update success!' 
  return render(request, 'StudentEmployeeInformation/search_byuid.html', text)


def loginView(request):
    return render(request, 'StudentEmployeeInformation/login.html')
    

def addloginView(request):
    return render(request, 'StudentEmployeeInformation/newlogin.html')