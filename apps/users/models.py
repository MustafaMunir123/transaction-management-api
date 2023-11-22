# Third Party Imports
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, null=False, blank=False)
    is_admin = models.BooleanField(default=False, null=False, blank=False)

    def __str__(self) -> str:
        return f"{self.username} {self.email}"

    REQUIRED_FIELDS = ["email"]
