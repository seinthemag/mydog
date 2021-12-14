from django.db import models

# Create your models here.
class Owner(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=100)
    age = models.IntegerField()

    class Meta:
        db_table = "owners"


class Dog(models.Model):
    owner = models.ForeignKey('Owner', on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    age = models.IntegerField()

    class Meta:
        db_table = "dogs"

