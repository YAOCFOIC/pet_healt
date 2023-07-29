from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Pet

class CustomerCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','password2']

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        """
        fields ='__all__'
        """
        exclude = ['owner', ]
        
        widgets = {
            'owner': forms.HiddenInput(),
            # ...
        }
        