from django.db import models


class Group(models.Model):
    groupname = models.CharField(max_length=10)


class Student(models.Model):
    firstname = models.CharField(max_length=20)
    secondname= models.CharField(max_length=20)
    thirdname = models.CharField(max_length=20)
    code = models.CharField(max_length = 6, unique=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

class Lesson(models.Model):
    name = models.CharField(max_length=100)
    start_time = models.CharField(max_length=20)
    end_time = models.CharField(max_length=20)
    day_of_Week = models.CharField(max_length=2)
    time = models.CharField(max_length=20)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
