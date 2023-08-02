from django.db import models
from django.contrib.auth.models import User
from functools import partial
# Create your models here.
def make_filepath(field_name, instance, filename):
    '''
        Produces a unique file path for the upload_to of a FileField.

        The produced path is of the form:
        "[model name]/[field name]/[random name].[filename extension]".
    '''
    new_filename = "%s.%s" % (User.objects.make_random_password(10),
                             filename.split('.')[-1])
    return '/'.join([instance.__class__.__name__.lower(),
                     field_name, new_filename])
class Animal(models.Model):
    type_animal = models.CharField(max_length=20, verbose_name= "Type Of Pet")
    def full_name(self):
        return "{}".format(self.type_animal)
    def __str__(self):
        return self.full_name()
    class Meta:
        verbose_name = 'Animal'
        verbose_name_plural = 'Animals'
        db_table='animal'
        ordering=['type_animal']
class Pet(models.Model): 
    name = models.CharField(max_length=20, verbose_name= "Name Of Pet")
    age = models.IntegerField(blank=True, null=True)
    animal = models.ForeignKey(Animal,null=True,on_delete=models.CASCADE)
    type_food= models.CharField(max_length=20, verbose_name= "type the food")
    owner = models.ForeignKey(User,null=True,on_delete=models.CASCADE)
    image = models.ImageField(upload_to=partial(make_filepath,'pets'), null=True)
    color = models.CharField(max_length=20, verbose_name= "Color Of Pet")
    size = models.IntegerField(blank=True, null=True)
    def full_name(self):
        return "{}".format(self.name)
    def __str__(self):
        return self.full_name()
    class Meta:
        verbose_name = 'Pet'
        verbose_name_plural = 'Pets'
        db_table='pet'
        ordering=['name','age']
        
class HealthConditions(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='condiciones_salud')
    date = models.DateField()
    health_condition = models.TextField()

class VeterinaryProcedures(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='procedimientos_veterinarios')
    date = models.DateField()
    description = models.TextField()
    image = models.ImageField(upload_to=partial(make_filepath,'procedures'), null=True, blank=True)

class IndicatorsHealth(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='indicadores_salud')
    indicator_type = models.CharField(max_length=100)
    value = models.CharField(max_length=50)

class MedicalControls(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='controles_medicos')
    date = models.DateField()
    professional_name = models.CharField(max_length=100)
    observation = models.TextField()

class MonitoringConditions(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='seguimiento_condiciones')
    date = models.DateField()
    diagnosis = models.TextField()
    treatment = models.TextField()
    evolution = models.TextField()
