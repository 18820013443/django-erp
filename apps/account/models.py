from django.db import models

# Create your models here.


class UserInfo(models.Model):
    username = models.CharField(max_length=12, unique= True)
    password = models.CharField(max_length=250)
    phone = models.CharField(max_length=11)
    wechat = models.CharField(max_length=60)


class UserToken(models.Model):
    userinfo = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    token = models.CharField(max_length= 250)