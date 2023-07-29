from django.contrib import admin
from .models import Pet,Animal
# Register your models here.
@admin.register(Animal)
class AppointmentAdmin(admin.ModelAdmin):
    list_per_page = 3
    def datas(self, obj):
        return obj.nombre.upper()
@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_per_page = 3
    def datas(self, obj):
     return obj.nombre.upper()
