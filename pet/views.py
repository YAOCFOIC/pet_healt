from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import CustomerCreateForm,PetForm,IndicatorsHealthForm,MedicalControlForm,HealthConditionForm,MonitoringConditionForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import LogoutView
from django.views.generic import ListView
from .models import Animal, Pet
from django.contrib.auth.models import User
from django.forms import formset_factory
# Create your views here.
@login_required
def inidicator_view(request,id):
    data = {
        'form': IndicatorsHealthForm()
    }
    if request.method == 'POST':
        send_form = IndicatorsHealthForm(data=request.POST)
        if send_form.is_valid():
            indicators_health = send_form.save(commit=False)
            indicators_health.pet_id = id  # Assign the pet instance related to the form
            indicators_health.save()
            #messages.success(request,"Success Register")
            return redirect(to="home")
        else:
            form = IndicatorsHealthForm()
    return render(request,'apps/indicator.html',data)

@login_required
def medical_view(request,id):
    data = {
        'form': MedicalControlForm()
    }
    if request.method == 'POST':
        send_form = MedicalControlForm(data=request.POST)
        print(send_form)
        if send_form.is_valid():
            medical_control = send_form.save(commit=False)
            medical_control.pet_id = id  # Assign the pet instance related to the form
            medical_control.save()
            #messages.success(request,"Success Register")
            return redirect(to="home")
        else:
            form = MedicalControlForm()
    return render(request,'apps/medical.html',data)

@login_required
def health_view(request,id):
    data = {
        'form': HealthConditionForm()
    }
    if request.method == 'POST':
        send_form = HealthConditionForm(data=request.POST)
        print(send_form)
        if send_form.is_valid():
            medical_control = send_form.save(commit=False)
            medical_control.pet_id = id  # Assign the pet instance related to the form
            medical_control.save()
            #messages.success(request,"Success Register")
            return redirect(to="home")
        else:
            form = HealthConditionForm()
    return render(request,'apps/health.html',data)

@login_required
def condition_view(request,id):
    data = {
        'form': MonitoringConditionForm()
    }
    if request.method == 'POST':
        send_form = MonitoringConditionForm(data=request.POST)
        print(send_form)
        if send_form.is_valid():
            medical_control = send_form.save(commit=False)
            medical_control.pet_id = id  # Assign the pet instance related to the form
            medical_control.save()
            #messages.success(request,"Success Register")
            return redirect(to="home")
        else:
            form = MonitoringConditionForm()
    return render(request,'apps/monitoring.html',data)

@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            # Redirect to a success page or wherever you want after changing the password
            return redirect('password_change_done')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {'form': form})

def index(request):
    return render(request,'index.html')

def register(request):
    data = {
        'form': CustomerCreateForm()
    }
    if request.method == 'POST':
        send_form = CustomerCreateForm(data=request.POST)
        if send_form.is_valid():
            send_form.save()
            user = authenticate(username=send_form.cleaned_data["username"],password=send_form.cleaned_data["password1"])
            login(request, user)
            #messages.success(request,"Success Register")
            return redirect(to="home")
        data["form"] = send_form
    return render(request,"registration/register.html",data)
@method_decorator(login_required, name='dispatch')
class HomeView(ListView):
    model = Pet
    template_name = 'apps/home.html'

    def get_queryset(self):
        return Pet.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_pet'] = PetForm()
        context['form_indicator'] = IndicatorsHealthForm()
        context['form_medical'] = MedicalControlForm()
        context['form_healt'] = HealthConditionForm()
        return context
    
def register_pet(request):
    if request.method == "POST":
        form = PetForm(request.POST,request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.owner = request.user
            form.save()

        return redirect(to='home')

    else:
        print("error")
    
    return render(request,'apps/home.html')
"""

    

def deletCourse(request, id):
    course = Course.objects.get(id=id)
    course.delete()

    return redirect('/')
"""