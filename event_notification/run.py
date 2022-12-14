import imp
import json
import queue
import mysql.connector
from datetime import datetime
import smtplib, ssl
from email.mime.text import MIMEText
import pandas as pd
import os

class Db:
  def __init__(self):
    self.mydb = mysql.connector.connect(host="rds-terraform.ccme3kf5lctp.us-east-2.rds.amazonaws.com", user="admin", password="is562section2classproject")
  
  def send_email(self, subject, text):
    port = 465
    account = 'is405project@gmail.com'
    password = 'zacmtgcrbbndquhm'
    recipient = 'is405project@gmail.com'
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
      server.login(account, password)
      message = text
      msg = MIMEText(message)
      msg['Subject'] = subject
      msg['To'] = recipient
      server.sendmail(account,recipient,msg.as_string())
      
  def query_Db(self, query):
    df_query = pd.read_sql(query, self.mydb)
    return df_query
  
  def update_tracker(self, query, tracker_name, subject):
    df_query = self.query_Db(query)
    if len(df_query) > 0:
      root_dir = os.path.dirname(os.path.abspath(__file__))
      file_path = os.path.join(root_dir, 'json_tracker', f'{tracker_name}')
      with open(file_path) as json_file:
        tracker = json.load(json_file)

      for byu_id in df_query['byu_id']:
        if str(byu_id) in tracker:
          tracker[str(byu_id)] += 1
        else:
          tracker[str(byu_id)] = 1

      email_id_list = []
      for x in tracker:
         if tracker[x] > 7:
          email_id_list.append(x)
          tracker[x] = 0
      
      if len(email_id_list) > 0:
        email_text = ""
        df_filterd_email = df_query[df_query.byu_id.isin([str(x) for x in email_id_list])]
        for index, row in df_filterd_email.iterrows():
          temp_fistname = df_filterd_email.loc[index, 'first_name']
          temp_lastname = df_filterd_email.loc[index, 'last_name']
          temp_byuid = df_filterd_email.loc[index, 'byu_id']
          email_text += temp_byuid + ": " + temp_fistname + " " + temp_lastname + "\n"
        self.send_email(subject=subject, text=email_text)
      with open(file_path, "w") as outfile:
        outfile.write(json.dumps(tracker))

def run():
  Db_svc = Db()
  today = datetime.today
  if (datetime.now().day == 30 and datetime.now().month == 8) or (datetime.now().day == 1 and datetime.now().month == 1):
    try:
      Db_svc.send_email(subject='Pay Increase Reminder', text="It's time to increase pay for the employees")
    except Exception as e:
      print('failed at sending notification of increase pay')
      pass
  
  try:
    query = "SELECT byu_id, first_name, last_name FROM BYUIS.student_employee where workauth = 0;"
    subject = "Alert! You have employees who haven't been authorized to work for a week"
    Db_svc.update_tracker(query=query, tracker_name="workauth_tracker.json", subject=subject)
  except Exception as e:
    print('failed at sending notification that are not authorized to work for a week')  
    pass  
  
  try:
    query = "SELECT  byu_id, first_name, last_name FROM BYUIS.student_employee where qualtrics_sent = 1 and eform = 0;"
    subject = "Alert! You have employees who signed Qualtrics Form but haven't signed E-Form for a week "
    Db_svc.update_tracker(query=query, tracker_name="eform_tracker.json", subject=subject)
  except:
    print('failed at sending notification that are has qualtrics survey but never fills out e-form for a week')
    pass
    
if __name__== '__main__':
  run()