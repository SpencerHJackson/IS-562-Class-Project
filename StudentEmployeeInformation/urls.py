from django.urls import path
from .views import indexPageView, send_email, addStudentEmployeeFormPageView, storeStudentEmployeePageView

urlpatterns = [
    path('', indexPageView, name="index"),
    path('addStudentEmployee/', addStudentEmployeeFormPageView, name="addStudentEmployeeForm"),
    path('storeEmployee/', storeStudentEmployeePageView, name="storeStudentEmployee"),
    path('sendEmail/', send_email, name="sendEmail")
]
