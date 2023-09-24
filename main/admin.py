from django.contrib import admin
from .models import Appointment, Diagnosis, DiagnosticStudies, Doctor


class DiagnosisAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'description', 'date', 'complaints',
        'objective_status', 'treatment', 'prognosis',
        'diagnosticstudies'
    )


class DiagnosticStudiesAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'date')


class DoctorAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'first_name', 'middle_name', 'last_name',
        'email', 'specialization'
    )


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'doctor', 'date')


admin.site.register(Diagnosis, DiagnosisAdmin)
admin.site.register(DiagnosticStudies, DiagnosticStudiesAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Appointment, AppointmentAdmin)
