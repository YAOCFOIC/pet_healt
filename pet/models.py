from django.db import models
from django.contrib.auth.models import User
# Create your models here.
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
    imagen = models.ImageField(upload_to="pets", null=True)
    def full_name(self):
        return "{}".format(self.name)
    def __str__(self):
        return self.full_name()
    class Meta:
        verbose_name = 'Pet'
        verbose_name_plural = 'Pets'
        db_table='pet'
        ordering=['name','age']