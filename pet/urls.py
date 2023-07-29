from django.urls import path
from .views import register,index,HomeView,LogoutView,register_pet

urlpatterns = [
   path('register/',register,name="register"),
   path('',index,name='index'),
   path('registerPet/',register_pet,name="registerPet"),
   path('home/',HomeView.as_view(),name='home'),
   path('logout/', LogoutView.as_view(next_page='login'),name='logout'),
]