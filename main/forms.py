from django import forms
from users.models import User
from .models import Diagnosis, DiagnosticStudies, Doctor

class FormStyleMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class BaseModelForm(FormStyleMixin, forms.ModelForm):
    pass

class DiagnosisForm(BaseModelForm):
    class Meta:
        model = Diagnosis
        fields = '__all__'

class DiagnosticStudiesForm(BaseModelForm):
    class Meta:
        model = DiagnosticStudies
        fields = '__all__'

class DoctorForm(BaseModelForm):
    class Meta:
        model = Doctor
        fields = '__all__'

class UserForm(BaseModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
            'password': forms.PasswordInput()
        }

class AdminSigupForm(UserForm):
    pass

class DoctorUserForm(UserForm):
    pass

class PatientUserForm(UserForm):
    pass

class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))