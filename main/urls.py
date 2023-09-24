from django.conf import settings
from django.urls import path

from main.apps import MainConfig
from main.views import (
    CreateAppointmentView,
    DiagnosticStudiesDetailView,
    DiagnosticStudiesListView,
    DoctorDetailView,
    DoctorListView,
    home
)
from django.conf.urls.static import static

app_name = MainConfig.name
urlpatterns = [

    path('', home, name='home'),
    path('diagnostic_studies/', DiagnosticStudiesListView.as_view(),
         name='diagnostic_studies_list'),
    path('diagnostic_studies_detail/<int:pk>/',
         DiagnosticStudiesDetailView.as_view(),
         name='diagnostic_studies_detail'),
    path('doctors/', DoctorListView.as_view(), name='doctors_list'),
    path('doctor/<int:pk>/', DoctorDetailView.as_view(), name='doctor_detail'),
    path('create_appointment/<int:pk>', CreateAppointmentView.as_view(),
         name='create_appointment'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
