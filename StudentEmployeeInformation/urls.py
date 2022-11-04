from django.urls import path
from .views import *

urlpatterns = [
    path('', indexPageView, name="index"),
    path('addStudentEmployee/', addStudentEmployeeFormPageView, name="addStudentEmployeeForm"),
    path('storeEmployee/', storeStudentEmployeePageView, name="storeStudentEmployee"),
    path('sendEmail/', send_email, name="sendEmail"),
    path('searchbyuid/', search_byuid, name="searchbyuid"),
    path('editrecord/', edit_record, name="editrecord"),
    path('saverecord/', save_record, name="saverecord"),
    path('tableau/', tableauView, name="TableauGraphs")
]
