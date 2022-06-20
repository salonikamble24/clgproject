from django.db import models
from django.contrib.auth.models import AbstractUser



USER_TYPE = (
    ("user", "user"),
    ("vendor", "vendor"),
    ("contractor", "contractor"),
)

class User(AbstractUser):
    contact_no = models.CharField(max_length=20, unique=True)
    area_code=models.IntegerField(null=True, blank=True)
    user_type = models.CharField(
        max_length = 20,
        choices = USER_TYPE,
        default = 'user'
        )
    def __str__(self):
        return f"{self.email}"