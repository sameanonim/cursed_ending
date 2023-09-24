from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views import View

from blog.models import Post
from .models import Appointment, Diagnosis, DiagnosticStudies, Doctor
from .forms import AppointmentForm


def home(request):
    """Вывод основной страницы"""
    extra_context = {
        'post_list': Post.objects.order_by("-view_count")[0:1],
        'post_list_2': Post.objects.order_by("-view_count")[1:3],
        'main_post': Post.objects.order_by('-view_count').first(),
        'main_posts': Post.objects.order_by('-view_count')[1:],
        'other_posts': Post.objects.order_by('-view_count')
    }
    return render(request, 'main/home.html', extra_context)


class DiagnosisDetailView(DetailView):
    model = Diagnosis
    template_name = "diagnosis_detail.html"


class DiagnosticStudiesListView(ListView):
    model = DiagnosticStudies
    template_name = "diagnostic_studies_list.html"
    paginate_by = 10
    ordering = ["-date"]


class DiagnosticStudiesDetailView(DetailView):
    model = DiagnosticStudies
    template_name = 'main/diagnostic_studies_detail.html'


class DoctorListView(ListView):
    model = Doctor
    template_name = 'doctors_list.html'
    context_object_name = 'doctors'


class DoctorDetailView(DetailView):
    model = Doctor
    template_name = 'main/doctor_detail.html'
    context_object_name = 'doctor'

    def get_object(self, queryset=None):
        return get_object_or_404(Doctor, id=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AppointmentForm(initial={'doctor': self.object})
        return context


class AppointmentView(View):
    template_name = 'main/doctor_detail.html'

    def post(self, request, *args, **kwargs):
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            if request.user.is_authenticated:
                appointment.patient = request.user
                appointment.save()
                return redirect('appointments')
            else:
                return redirect('login')
        else:
            return render(request, self.template_name, {'form': form})

    def confirm_appointment(self, request, *args, **kwargs):
        appointment_id = request.POST.get('appointment_id')
        appointment = get_object_or_404(Appointment, id=appointment_id)
        if request.user.is_authenticated and \
                request.user == appointment.doctor:
            appointment.confirmed = True
            appointment.save()
            return redirect('appointments')
        else:
            return redirect('login')


class CreateAppointmentView(View):
    model = Appointment
    template_name = 'main/confirm_appointment.html'

    def post(self, request, *args, **kwargs):
        doctor = get_object_or_404(Doctor, id=self.kwargs.get('pk'))
        form = AppointmentForm(request.POST)
        if form.is_valid() and doctor:
            appointment = form.save(commit=False)
            appointment.doctor = doctor
            if request.user.is_authenticated:
                appointment.patient = request.user
                appointment.save()
                return redirect('appointments')
            else:
                return redirect('login')
        else:
            return render(request, 'main/doctor_detail.html',
                          {'form': form, 'doctor': doctor})
