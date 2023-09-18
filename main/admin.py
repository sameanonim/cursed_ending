from django.contrib import admin
from .models import Diagnosis, DiagnosticStudies, Doctor

class DiagnosisAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'date', 'complaints', 'objective_status', 'treatment', 'prognosis', 'diagnosticstudies']

    def get_diagnosticstudies(self, obj):
        return obj.diagnosticstudies.title
    get_diagnosticstudies.short_description = 'Диагностические исследования'

class DiagnosticStudiesAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'date']

class DoctorAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'middle_name', 'last_name', 'specialization']

class UserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'middle_name', 'last_name', 'email']

admin.site.register(Diagnosis, DiagnosisAdmin)
admin.site.register(DiagnosticStudies, DiagnosticStudiesAdmin)
admin.site.register(Doctor, DoctorAdmin)