from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name="home"),
    path('about_us', views.about_us, name="about_us"),
    path('user/login/', views.user_login, name="user_login"),
    path('user/reg/', views.user_reg, name="user_reg"),
    path('user/firstpage/', views.firstpage, name="dashboard"),
    path('user/estimate/', views.estimate, name="estimate"),
    path('user/estimatedcost/', views.estimatedcost, name="estimatedcost"),
    path('user/tender/', views.tender, name="tender"),


]