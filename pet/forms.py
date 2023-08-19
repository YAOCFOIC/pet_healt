from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Pet,HealthCondition,IndicatorsHealth,MedicalControl,MonitoringCondition
from django.core.validators import FileExtensionValidator
from account.models import CustomUser
class DateInput(forms.DateInput):
    input_type = 'date'
    
class CustomerCreateForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username','first_name','last_name','email','phone','password1','password2']

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        """
        fields ='__all__'
        """
        image = forms.ImageField(validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])])
        exclude = ['owner', ]
        
        widgets = {
            'owner': forms.HiddenInput(),
            # ...
        }
        
class IndicatorsHealthForm(forms.ModelForm):
    class Meta:
        model = IndicatorsHealth
        exclude = ['pet', ]
        
        widgets = {
            'pet': forms.HiddenInput(),
            # ...
        }
        
        
        
class MedicalControlForm(forms.ModelForm):
    class Meta:
        model = MedicalControl
        exclude = ['pet', ]
        
        widgets = {
            'date': DateInput(attrs={'class': 'form-control form-control-lg'}),
            'professional_name': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'observation': forms.Textarea(attrs={'class': 'form-control'}),
        }
    
class HealthConditionForm(forms.ModelForm):
    class Meta:
        model = HealthCondition
        exclude = ['pet']
        
        widgets = {
            'health_type_condition': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'date': DateInput(attrs={'class': 'form-control form-control-lg'}),
        }
        
class MonitoringConditionForm(forms.ModelForm):
     class Meta:
        model = MonitoringCondition
        exclude = ['pet']
        
        widgets = {
            'date': DateInput(attrs={'class': 'form-control form-control-lg'}),
        }

class DateRangeForm(forms.Form):
    start_date = forms.DateField(label='Start Date', widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(label='End Date', widget=forms.DateInput(attrs={'type': 'date'}))