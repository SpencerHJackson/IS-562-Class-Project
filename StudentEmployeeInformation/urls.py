from django.urls import path
from .views import indexPageView, send_email

urlpatterns = [
    path('', indexPageView, name="index"),
    path('sendEmail/', send_email, name="sendEmail")
]
