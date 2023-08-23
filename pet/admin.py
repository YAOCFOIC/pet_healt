from django.contrib import admin
from .models import Pet,Animal,HealthCondition,IndicatorsHealth,MedicalControl,MonitoringCondition,Breed
# Register your models here.
@admin.register(Animal)
class AppointmentAdmin(admin.ModelAdmin):
    search_fields = ('type_animal',)
    list_filter = ('type_animal',)
    list_per_page = 10
    list_display = ('id','type_animal')
    def datas(self, obj):
        return obj.nombre.upper()
@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_per_page = 10
    search_fields = ('name',)
    list_filter = ('name',)
    list_display = ('id','name','owner')
    def datas(self, obj):
     return obj.nombre.upper()
@admin.register(HealthCondition)
class HealthConditionAdmin(admin.ModelAdmin):
    list_per_page = 10
    search_fields = ('indicator_type','date')
    list_filter = ('health_type_condition',)
    list_display = ('id','date','health_type_condition')
    def datas(self, obj):
        return obj.nombre.upper()
@admin.register(IndicatorsHealth)
class IndicatorsHealthAdmin(admin.ModelAdmin):
    list_per_page = 10
    search_fields = ('indicator_type',)
    list_filter = ('indicator_type',)
    list_display = ('pet','indicator_type','value')
    def datas(self, obj):
     return obj.nombre.upper()
 
@admin.register(MedicalControl)
class MedicalControlAdmin(admin.ModelAdmin):
    list_per_page = 10
    search_fields = ('professional_name','date')
    list_filter = ('professional_name',)
    list_display = ('pet','professional_name','date')
    def datas(self, obj):
        return obj.nombre.upper()
@admin.register(MonitoringCondition)
class MonitoringConditionAdmin(admin.ModelAdmin):
    list_per_page = 10
    search_fields = ('date',)
    list_display = ('pet','date')
    list_filter=('pet',)
    def datas(self, obj):
     return obj.nombre.upper()
@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_filter=('name',)
    list_per_page = 10
    list_display = ('id','name')
    def datas(self, obj):
     return obj.nombre.upper()