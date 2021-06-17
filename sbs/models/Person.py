from django.db import models
from sbs.models.Document import Document
from sbs.models.Penal import Penal
from sbs.models.Material import Material
from sbs.models.Nationnality import Nationnality

from unicode_tr import unicode_tr

class Person(models.Model):
    ILKOKUL = 10
    lISE = 15
    UNİVERİSTE = 25
    YUKSEKLİSANS = 30
    YUKSEKOKUL = 20

    JOP = (
        (ILKOKUL, 'İlkokul'),
        (lISE, 'Lise'),
        (UNİVERİSTE, 'Üniversite(Lisans)'),
        (YUKSEKLİSANS, 'Yüksek Lisans'),
        (YUKSEKOKUL, 'Yüksek Okul'),
    )

    MALE = 1
    FEMALE = 2

    AB1 = 'AB(+)'
    AB2 = 'AB(-)'
    A1 = 'A(+)'
    A2 = 'A(-)'
    B1 = 'B(+)'
    B2 = 'B(-)'
    O1 = '0(+)'
    O2 = '0(-)'

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
    # AB1 = 'AB Rh+'
    # AB2 = 'AB Rh-'
    # A1 = 'A Rh+'
    # A2 = 'A Rh-'
    # B1 = 'B Rh+'
    # B2 = 'B Rh-'
    # O1 = '0 Rh+'
    # O2 = '0 Rh-'
    #
    # GENDER_CHOICES = (
    #     (MALE, 'Erkek'),
    #     (FEMALE, 'Kadın'),
    # )
    #
    # BLOODTYPE = (
    #     (AB1, 'AB Rh+'),
    #     (AB2, 'AB Rh-'),
    #     (A1, 'A Rh+'),
    #     (A2, 'A Rh-'),
    #     (B1, 'B Rh+'),
    #     (B2, 'B Rh-'),
    #     (O1, '0 Rh+'),
    #     (O2, '0 Rh-'),
    #
    # )
    tc = models.CharField(max_length=120, null=True, blank=True)
    height = models.CharField(max_length=120, null=True, blank=True)
    weight = models.CharField(max_length=120, null=True, blank=True)
    birthplace = models.CharField(max_length=120, null=True, blank=True, verbose_name='Doğum Yeri')
    motherName = models.CharField(max_length=120, null=True, blank=True, verbose_name='Anne Adı')
    fatherName = models.CharField(max_length=120, null=True, blank=True, verbose_name='Baba Adı')
    profileImage = models.ImageField(upload_to='profile/', null=True, blank=True, default='profile/user.png',
                                     verbose_name='Profil Resmi')

    birthDate = models.DateField(null=True, blank=True, verbose_name='Doğum Tarihi')
    bloodType = models.CharField(max_length=128, verbose_name='Kan Grubu', choices=BLOODTYPE, null=True, blank=True)
    gender = models.IntegerField(choices=GENDER_CHOICES, blank=True, null=True)


    document = models.ManyToManyField(Document)
    penal = models.ManyToManyField(Penal)

    # badminton database add festportal

    uyrukid = models.ForeignKey(Nationnality, models.CASCADE, blank=True, null=True)
    nufus_ailesirano = models.CharField(max_length=20, blank=True, null=True)
    nufus_sirano = models.CharField(max_length=20, blank=True, null=True)
    nufus_ciltno = models.CharField(max_length=20, blank=True, null=True)

    meslek = models.CharField(max_length=120, blank=True, null=True)
    kurum = models.CharField(max_length=120, blank=True, null=True)
    is_unvani = models.CharField(max_length=120, blank=True, null=True)

    education = models.IntegerField(choices=JOP, null=True, blank=True)
    mezunokul = models.CharField(max_length=200, blank=True, null=True)

    material = models.ForeignKey(Material, models.CASCADE, blank=True, null=True)



    # class Meta:
    #     default_permissions = ()

    def save(self, force_insert=False, force_update=False):
        if self.birthplace:
            self.birthplace = unicode_tr(self.birthplace)
            self.birthplace = self.birthplace.upper()
        if self.motherName:
            self.motherName = unicode_tr(self.motherName)
            self.motherName = self.motherName.upper()
        if self.fatherName:
            self.fatherName = unicode_tr(self.fatherName)
            self.fatherName = self.fatherName.upper()
        super(Person, self).save(force_insert, force_update)
