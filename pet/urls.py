from django.urls import path
from .views import register,index,HomeView,LogoutView,register_pet,change_password_view,inidicator_view,medical_view,condition_view,health_view,history_view,generate_pdf_report,generate_pdf_reports_within_range
from .views import PetDeleteView
urlpatterns = [
   path('register/',register,name="register"),
   path('pet/<int:pk>/delete/', PetDeleteView.as_view(), name='pet_delete'),
   path('',index,name='index'),
   path('registerPet/',register_pet,name="registerPet"),
   path('home/',HomeView.as_view(),name='home'),
   path('inidicator/<int:id>/',inidicator_view,name='inidicator'),
   path('medicalrecord/<int:pet_id>/',generate_pdf_report,name='pdf'),
   path('generate_pdf_reports_within_range/', generate_pdf_reports_within_range, name='generate_pdf_reports_within_range'),
   path('history/',history_view,name='history'),
   path('health/<int:id>/',health_view,name='health'),
   path('medical/<int:id>/',medical_view,name='medical'),
   path('condition/<int:id>/',condition_view,name='condition'),
   path('change-password/', change_password_view, name='change_password'),
   path('logout/', LogoutView.as_view(next_page='login'),name='logout'),
]