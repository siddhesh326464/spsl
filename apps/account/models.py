from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Account(AbstractUser):
    class Meta:
        db_table = "account"
        verbose_name = "Accounts"
        verbose_name_plural = "Account"

    STATUS = [
        ('1','ACTIVE'),
        ('2','INACTIVE')
    ]

    ROLE = [
        ('1','COMPANY USER'),
        ('2','COMPANY MANAGER'),
        ('3','ADDNECTAR ARTIST'),
        ('4','ADDNECTAR MANAGER'),
    ]

    email = models.EmailField(max_length=100,unique=True)
    name = models.CharField(max_length=30)
    username = models.CharField(max_length=30,unique=True)
    rep_no = models.CharField(max_length=100,null=True,blank=True)
    role = models.CharField(choices=ROLE,max_length=10)
    status = models.CharField(choices=STATUS,max_length=20)
    contact_no = models.CharField(max_length=20,null=True,blank=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name