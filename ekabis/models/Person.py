from django.contrib.auth.models import User
from django.db import models
from ekabis.models.BaseModel import BaseModel


class Person(BaseModel):
    MALE = 0
    FEMALE = 1

    AB1 = 'AB Rh+'
    AB2 = 'AB Rh-'
    A1 = 'A Rh+'
    A2 = 'A Rh-'
    B1 = 'B Rh+'
    B2 = 'B Rh-'
    O1 = '0 Rh+'
    O2 = '0 Rh-'

    GENDER_CHOICES = (
        (MALE, 'Erkek'),
        (FEMALE, 'Kadın'),
    )

    BLOODTYPE = (
        (AB1, 'AB Rh+'),
        (AB2, 'AB Rh-'),
        (A1, 'A Rh+'),
        (A2, 'A Rh-'),
        (B1, 'B Rh+'),
        (B2, 'B Rh-'),
        (O1, '0 Rh+'),
        (O2, '0 Rh-'),

    )

    tc = models.CharField(max_length=120, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_column='user', null=True, blank=True)
    phoneNumber = models.CharField(max_length=11, null=False, blank=False)
    address = models.CharField(max_length=250,blank=True, null=True, verbose_name='Adres')
    height = models.CharField(max_length=120, null=True, blank=True)
    weight = models.CharField(max_length=120, null=True, blank=True)
    birthplace = models.CharField(max_length=120, null=True, blank=True, verbose_name='Doğum Yeri')
    motherName = models.CharField(max_length=120, null=True, blank=True, verbose_name='Anne Adı')
    fatherName = models.CharField(max_length=120, null=True, blank=True, verbose_name='Baba Adı')
    profileImage = models.ImageField(upload_to='profile/', null=True, blank=True, default='profile/user.png',
                                     verbose_name='Profil Resmi')
    birthDate = models.DateField(null=True, blank=True, verbose_name='Doğum Tarihi')
    bloodType = models.CharField(max_length=128, verbose_name='Kan Grubu', choices=BLOODTYPE, default=AB1, null=True,
                                 blank=True)
    gender = models.IntegerField(blank=True, null=True, choices=GENDER_CHOICES)
    failed_login = models.IntegerField(null=True, blank=True, default=0)
    failed_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        default_permissions = ()
