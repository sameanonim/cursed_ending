from django.conf import settings
from django.urls import path
from main.apps import MainConfig
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView
from main.views import AdminClickView, AdminSignupView, DoctorClickView, DoctorDashboardView, DoctorSignupView, HomeView, PatientClickView, PatientSignupView

app_name = MainConfig.name
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('adminclick/', AdminClickView.as_view(), name='adminclick'),
    path('doctorclick/', DoctorClickView.as_view(), name='doctorclick'),
    path('patientclick/', PatientClickView.as_view(), name='patientclick'),
    path('adminsignup/', AdminSignupView.as_view(), name='adminsignup'),
    path('doctorsignup/', DoctorSignupView.as_view(), name='doctorsignup'),
    path('patientsignup/', PatientSignupView.as_view(), name='patientsignup'),
    path('adminlogin', LoginView.as_view(template_name='hospital/adminlogin.html')),
    path('doctorlogin', LoginView.as_view(template_name='hospital/doctorlogin.html')),
    path('patientlogin', LoginView.as_view(template_name='hospital/patientlogin.html')),
    path('doctor-dashboard/<str:space_name>/', DoctorDashboardView.as_view(), name='doctor-dashboard'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)