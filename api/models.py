from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class Users(AbstractUser):
    pass


class ToDoLists(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)

    name = models.CharField(max_length=10, blank=False, editable=False, unique=True)
    body = models.CharField(max_length=700, blank=True)

    created_on = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    priority = models.IntegerField(default=0)

    def __str__(self):
        return self.name
