from django.urls import path
from . import views
urlpatterns = [
    path('contractor/login/', views.contractor_login, name="contractor_login"),
    path('contractor/reg/', views.contractor_reg, name="contractor_reg"),
    path('contractor/firstpage/', views.cfirstpage, name="dashboard"),
]