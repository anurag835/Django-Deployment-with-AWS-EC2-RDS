from django.db import models

class Logo(models.Model):
    image = models.ImageField(upload_to='logos/', null=True, blank=True)

class UserData(models.Model):
    roll = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100)
    parentName = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    branch = models.CharField(max_length=100)
    logo = models.OneToOneField(Logo, on_delete=models.SET_NULL, null=True, blank=True)


class UserInput(models.Model):
    roll = models.CharField(max_length=100, primary_key=True)
    subject1 = models.CharField(max_length=100)
    maxMarkSub1 = models.IntegerField()
    markObSub1 = models.IntegerField()
    subject2 = models.CharField(max_length=100)
    maxMarkSub2 = models.IntegerField()
    markObSub2 = models.IntegerField()
    subject3 = models.CharField(max_length=100)
    maxMarkSub3 = models.IntegerField()
    markObSub3 = models.IntegerField()
    subject4 = models.CharField(max_length=100)
    maxMarkSub4 = models.IntegerField()
    markObSub4 = models.IntegerField()
    subject5 = models.CharField(max_length=100)
    maxMarkSub5 = models.IntegerField()
    markObSub5 = models.IntegerField()
    subject6 = models.CharField(max_length=100)
    maxMarkSub6 = models.IntegerField()
    markObSub6 = models.IntegerField()
    userdata = models.ForeignKey(
        UserData, on_delete=models.CASCADE, blank=True, null=True)
