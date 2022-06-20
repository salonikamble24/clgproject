from django.urls import path
from . import views
urlpatterns = [
    path('vendor/login/', views.vendor_login, name="vendor_login"),
    path('vendor/reg/', views.vendor_reg, name="vendor_reg"),
    path('vendor/firstpage/', views.vfirstpage, name="dashboard1"),
    #  path('vendor/firstpage/', views.vfirstpage, name="dashboard1"),
    
]