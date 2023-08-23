from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from .forms import CustomerCreateForm,PetForm,IndicatorsHealthForm,MedicalControlForm,HealthConditionForm,MonitoringConditionForm,DateRangeForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import LogoutView
from django.views.generic import ListView
from django.http import FileResponse
from django.template.loader import get_template
from django.template import Context
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from django.urls import reverse_lazy
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from .models import Animal, Pet,HealthCondition,MedicalControl,MonitoringCondition
from django.contrib.auth.models import User
from django.forms import formset_factory
# Create your views here.
@login_required
def generate_pdf_report(request, pet_id):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte.pdf"'
    user = request.user  # Get the currently logged-in user
    pets_with_conditions = Pet.objects.filter(owner=user, seguimiento_condiciones__diagnosis__isnull=False,controles_medicos__observation__isnull=False, id=pet_id).distinct()
    
    # Crear el documento PDF usando reportlab
    doc = SimpleDocTemplate(response, pagesize=letter)
    styles = getSampleStyleSheet()
    observation_style = ParagraphStyle(name='ObservationStyle', fontSize=12, leading=14)
    elements = []
        
    for pet in pets_with_conditions:
        if pet.image:
            pet_image = pet.image.path  # Use the path to the image
            img = Image(pet_image, width=100, height=100)
            elements.append(img)
        elements.append(Paragraph(f"<b>Name</b>: {pet.name}", styles['Normal']))
        elements.append(Paragraph(f"<b>Age</b>: {pet.age}", styles['Normal']))
        
        # Obtain health conditions related to the pet
        health_conditions = HealthCondition.objects.filter(pet=pet)
        if health_conditions.exists():
            elements.append(Paragraph("Healths Conditions", styles['Heading2']))
        for condition in health_conditions:
            elements.append(Paragraph(f"<b>Status</b>:{condition.health_type_condition} ", styles['Normal']))
            elements.append(Paragraph(f"<b>Recomendation</b>: {condition.health_condition} ", styles['Normal']))
            elements.append(Paragraph(f"<b>Date</b>: {condition.date}", styles['Normal']))
            # Add more details as needed
        
        # Obtain medical checks related to the pet
        medical_controls = MedicalControl.objects.filter(pet=pet)
        if medical_controls.exists():
            elements.append(Paragraph("Medicals Controls", styles['Heading2']))
        for control in medical_controls:
            elements.append(Paragraph("<b>Professional</b>: "+control.professional_name, styles['Normal']))
            elements.append(Paragraph(control.observation, styles['Normal']))
            elements.append(Paragraph(f"<b>Date</b>: {control.date}", styles['Normal']))
            elements.append(Spacer(1, 12))
            # Agregar más detalles según sea necesario
        
        # Obtener las condiciones de seguimiento relacionadas con la mascota
        monitoring_conditions = MonitoringCondition.objects.filter(pet=pet)
        for condition in monitoring_conditions:
            elements.append(Paragraph("Diagnosis", styles['Heading2']))  # Title
            elements.append(Paragraph(condition.diagnosis, styles['Normal']))  # Text
            elements.append(Paragraph(f"<b>Date</b>: {condition.date}", styles['Normal']))
            elements.append(Spacer(1, 12))
            # Add more details as needed
        
    doc.build(elements)

    return response
@login_required
def generate_pdf_reports_within_range(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reports_within_range.pdf"'
    
    # Get the date range from the form
    form = DateRangeForm(request.GET or None)
    if form.is_valid():
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        monitoring_conditions = MonitoringCondition.objects.filter(date__range=(start_date, end_date))
        
        
        monitoring_conditions_within_range = MonitoringCondition.objects.filter(date__range=(start_date, end_date))
        health_conditions_within_range = HealthCondition.objects.filter(date__range=(start_date, end_date))
        medical_controls_within_range = MedicalControl.objects.filter(date__range=(start_date, end_date))
        pets_within_range = Pet.objects.filter(seguimiento_condiciones__in=monitoring_conditions_within_range)
    
        elements = []
        styles = getSampleStyleSheet()
        
        for pet in pets_within_range:
            if pet.image:
                pet_image = pet.image.path  # Use the path to the image
                img = Image(pet_image, width=100, height=100)
                elements.append(img)
            elements.append(Paragraph(f"<b>Name</b>: {pet.name}", styles['Normal']))
            elements.append(Paragraph(f"<b>Age</b>: {pet.age}", styles['Normal']))

            health_conditions = health_conditions_within_range.filter(pet=pet)
            if health_conditions.exists():
                elements.append(Paragraph("<b>Health Conditions</b>", styles['Heading2']))
            for condition in health_conditions:
                elements.append(Paragraph(f"<b>Status</b>: {condition.health_type_condition}", styles['Normal']))
                elements.append(Paragraph(f"<b>Recomendation</b>: {condition.health_condition}", styles['Normal']))
                elements.append(Paragraph(f"<b>Date</b>: {condition.date}", styles['Normal']))
                elements.append(Spacer(1, 12))

            medical_controls = medical_controls_within_range.filter(pet=pet)
            if medical_controls.exists():
                elements.append(Paragraph("<b>Medical Controls</b>", styles['Heading2']))
            for control in medical_controls:
                elements.append(Paragraph(f"<b>Professional</b>: {control.professional_name}", styles['Normal']))
                elements.append(Paragraph(control.observation, styles['Normal']))
                elements.append(Paragraph(f"<b>Date</b>: {control.date}", styles['Normal']))
                elements.append(Spacer(1, 12))

            pet_monitoring_conditions = monitoring_conditions_within_range.filter(pet=pet)
            for condition in pet_monitoring_conditions:
                elements.append(Paragraph("<b>Diagnosis</b>", styles['Heading2']))
                elements.append(Paragraph(condition.diagnosis, styles['Normal']))
                elements.append(Paragraph(f"<b>Date</b>: {condition.date}", styles['Normal']))
                elements.append(Spacer(1, 12))

        doc = SimpleDocTemplate(response, pagesize=letter)
        doc.build(elements)

    return response
@login_required
def history_view(request):
    user = request.user  # Get the currently logged-in user

    # Filter pets owned by the logged-in user
    pets = Pet.objects.filter(owner=user)
    monitoring_conditions = MonitoringCondition.objects.all()
    
    form = DateRangeForm(request.GET or None)
    if form.is_valid():
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        monitoring_conditions = monitoring_conditions.filter(date__range=(start_date, end_date))
        
    context = {
        'pets': pets,
        'monitoring_conditions': monitoring_conditions,
        'form': form
    }
    return render(request, 'apps/history.html', context)

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
        return Pet.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_pet'] = PetForm()
        context['form_indicator'] = IndicatorsHealthForm()
        context['form_medical'] = MedicalControlForm()
        context['form_healt'] = HealthConditionForm()
        return context
    def post(self, request, *args, **kwargs):
        pet_pk_to_delete = request.POST.get('pet_to_delete')
        if pet_pk_to_delete:
            try:
                pet = Pet.objects.get(pk=pet_pk_to_delete, owner=request.user)
                pet.delete()
            except Pet.DoesNotExist:
                pass  # Handle the case if the pet does not exist

        return self.get(request, *args, **kwargs)
@method_decorator(login_required, name='dispatch')
class PetDeleteView(ListView):
    model = Pet
    success_url = reverse_lazy('home')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        # Elimina registros relacionados manualmente
        self.object.condiciones_salud.all().delete()
        self.object.indicadores_salud.all().delete()
        self.object.controles_medicos.all().delete()
        self.object.seguimiento_condiciones.all().delete()

        # Elimina la mascota
        self.object.delete()

        return redirect(self.get_success_url())
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
