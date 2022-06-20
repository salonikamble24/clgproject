from math import trunc
from sqlite3 import Timestamp
from django.db import models
from users.models import User

# Create your models here.
class Vendor(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    company_name=models.CharField(max_length=70)
    company_address=models.CharField(max_length=70)
    material_name=models.CharField(max_length=70)
    phone_no=models.CharField(max_length=10)
    timestamp=models.DateTimeField(auto_now_add=True, null=True, blank=True)
    