from django.shortcuts import render, redirect
from .forms import CustomerCreateForm,PetForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView
from django.views.generic import ListView
from .models import Animal, Pet
from django.contrib.auth.models import User
# Create your views here.

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