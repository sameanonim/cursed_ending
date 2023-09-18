from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView
from django.views.generic import ListView, TemplateView
from users.models import User
from .models import Diagnosis, DiagnosticStudies, Doctor
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import View
from . import forms
from django.contrib.auth.models import Group
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class DiagnosisListView(ListView):
    model = Diagnosis
    template_name = 'diagnosis_list.html'
    context_object_name = 'diagnosis'


class DiagnosticStudiesListView(ListView):
    model = DiagnosticStudies
    template_name = 'diagnostic_studies_list.html'
    context_object_name = 'studies'


class DoctorListView(ListView):
    model = Doctor
    template_name = 'doctor_list.html'
    context_object_name = 'doctors'

class AboutUsView(TemplateView):
    template_name = 'about_us.html'

class ContactUsView(TemplateView):
    template_name = 'contact_us.html'

class HomeView(View):
    def get(self, request):
            return render(request, 'hospital/index.html')
        
class AdminClickView(HomeView):
    def get(self, request):
        return render(request, 'hospital/adminclick.html')

class DoctorClickView(HomeView):
    def get(self, request):
        return render(request, 'hospital/doctorclick.html')

class PatientClickView(HomeView):
    def get(self, request):
        return render(request, 'hospital/patientclick.html')

class AdminSignupView(View):
    def get(self, request):
        form = forms.AdminSigupForm()
        return render(request, 'hospital/adminsignup.html', {'form': form})

    def post(self, request):
        form = forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)
            return HttpResponseRedirect('adminlogin')

def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()

def is_doctor(user):
    return user.groups.filter(name='DOCTOR').exists()

def is_patient(user):
    return user.groups.filter(name='PATIENT').exists()

class AfterLoginView(View):
    def get(self, request):
        if is_admin(request.user):
            return redirect('admin-dashboard')
        elif is_doctor(request.user):
            accountapproval = Doctor.objects.all().filter(user_id=request.user.id, status=True)
            if accountapproval:
                return redirect('doctor-dashboard')
            else:
                return render(request, 'hospital/doctor_wait_for_approval.html')
        elif is_patient(request.user):
            accountapproval = Patient.objects.all().filter(user_id=request.user.id, status=True)
            if accountapproval:
                return redirect('patient-dashboard')
            else:
                return render(request, 'hospital/patient_wait_for_approval.html')
            
from django.views import View
from django.shortcuts import render, redirect
from .forms import AdminSigupForm, DoctorUserForm, PatientUserForm

class AdminSignupView(View):
    def get(self, request):
        form = AdminSigupForm()
        return render(request, 'hospital/adminsignup.html', {'form': form})

    def post(self, request):
        form = AdminSigupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.cleaned_data.get('password'))
            user.save()
            return redirect('adminlogin')

class DoctorSignupView(View):
    def get(self, request):
        form = DoctorUserForm()
        return render(request, 'hospital/doctorsignup.html', {'form': form})

    def post(self, request):
        form = DoctorUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.cleaned_data.get('password'))
            user.save()
            return redirect('doctorlogin')

class PatientSignupView(View):
    def get(self, request):
        form = PatientUserForm()
        return render(request, 'hospital/patientsignup.html', {'form': form})

    def post(self, request):
        form = PatientUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.cleaned_data.get('password'))
            user.save()
            return redirect('patientlogin')
        


class DoctorDashboardView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    login_url = 'doctorlogin'
    template_name = 'hospital/doctor_dashboard.html'
    context_object_name = 'get_place'

    def test_func(self):
        # check if the user is a doctor
        return is_doctor(self.request.user)

    def get_context_data(self, **kwargs):
        # get extra context data
        context = super().get_context_data(**kwargs)
        place = self.get_object()
        context['patientcount'] = User.objects.all().filter(status=True, assignedDoctorId=self.request.user.id).count()
        context['doctor'] = Doctor.objects.get(user_id=self.request.user.id) #for profile picture of doctor in sidebar
        return context
