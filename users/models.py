from django.db import models
from datetime import datetime

# Create your models here.

from django.contrib.auth.models import AbstractUser

class BlogUser(AbstractUser):
    nikename = models.CharField('nikename', max_length=20, default='')

#email validation model
class EmailVerifyRecord(models.Model):
    code = models.CharField(verbose_name="verification code",max_length=50,default='')
    email = models.EmailField(max_length=50,verbose_name="email address")
    send_type = models.CharField(verbose_name="the type of verification code",choices=(("register","register"),("forget","retrieve password"),("update_email","modify email address")), max_length=30)
    send_time = models.DateTimeField(verbose_name="transmission time",default=datetime.now)

    class Meta:
        verbose_name = "verification code received by email"
        verbose_name_plural = verbose_name

    def __str__(arg):
        return '{0}({1})'.format(self.code,self.email)
