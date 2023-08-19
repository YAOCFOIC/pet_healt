from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from account.models import CustomUser
from functools import partial
from .choices import indicator_types,health_type_condition
# Create your models here.
def make_filepath(field_name, instance, filename):
    '''
        Produces a unique file path for the upload_to of a FileField.

        The produced path is of the form:
        "[model name]/[field name]/[random name].[filename extension]".
    '''
    new_filename = "%s.%s" % (CustomUser.objects.make_random_password(10),
                             filename.split('.')[-1])
    return '/'.join([instance.__class__.__name__.lower(),
                     field_name, new_filename])

class Breed(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Animal(models.Model):
    type_animal = models.CharField(max_length=20, verbose_name= "Type Of Pet")
    breed = models.ForeignKey(Breed,null=True, on_delete=models.CASCADE)
    def full_name(self):
        text = "{0} {1}"
        return text.format(self.type_animal, self.breed)
    def __str__(self):
        return self.full_name()
    class Meta:
        verbose_name = 'Animal'
        verbose_name_plural = 'Animals'
        db_table='animal'
        ordering=['type_animal']

class Pet(models.Model): 
    name = models.CharField(max_length=50, verbose_name= "Name Of Pet")
    age = models.IntegerField(blank=True, null=True)
    animal = models.ForeignKey(Animal,null=True,on_delete=models.CASCADE)
    type_food= models.CharField(max_length=50, verbose_name= "type the food")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,on_delete=models.CASCADE)
    image = models.ImageField(upload_to=partial(make_filepath,'pets'), null=True)
    color = models.CharField(max_length=50, verbose_name= "Color Of Pet")
    def full_name(self):
        text = "{0} {1} {2}"
        return text.format(self.name, self.age, self.owner)
    def __str__(self):
        return self.full_name()
    class Meta:
        verbose_name = 'Pet'
        verbose_name_plural = 'Pets'
        db_table='pet'
        ordering=['name','age']


class HealthCondition(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='condiciones_salud')
    date = models.DateField()
    health_type_condition = models.CharField(max_length=100,choices=health_type_condition, default='unknown')
    health_condition = models.TextField()
    def full_name(self):
        text = "{0} {1} "
        return text.format(self.date, self.health_type_condition)
    def __str__(self):
        return self.full_name()

class IndicatorsHealth(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='indicadores_salud')
    indicator_type = models.CharField(max_length=100, choices=indicator_types)
    value = models.CharField(max_length=50)
    def full_name(self):
        return "{}".format(self.indicator_type)
    def __str__(self):
        return self.full_name()

class MedicalControl(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='controles_medicos')
    date = models.DateField()
    professional_name = models.CharField(max_length=100)
    observation = models.TextField()
    def full_name(self):
        return "{}".format(self.professional_name)
    def __str__(self):
        return self.full_name()

class MonitoringCondition(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='seguimiento_condiciones')
    date = models.DateField()
    diagnosis = models.TextField()
    treatment = models.TextField()
    evolution = models.TextField()
    size = models.IntegerField(blank=True, null=True)
    description = models.TextField()
    image = models.ImageField(upload_to=partial(make_filepath,'procedures'), null=True, blank=True)
    def full_name(self):
        return "{}".format(self.diagnosis)
    def __str__(self):
        return self.full_name()
