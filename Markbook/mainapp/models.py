from django.db import models

class Student(models.Model):
    firstname = models.CharField(max_length=20)
    secondname= models.CharField(max_length=20)
    thirdname = models.CharField(max_length=20)
    code = models.CharField(max_length = 6, unique=True)