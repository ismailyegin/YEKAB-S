from django.db import models
from sbs.models.City import City
from sbs.models.Country import Country
from sbs.models.SportClubUser import SportClubUser
from sbs.models.Coach import Coach
from sbs.models.ClubRole import ClubRole
from sbs.models.CategoryItem import CategoryItem



class PreRegistration(models.Model):
    MALE = 'Erkek'
    FEMALE = 'Kadın'

    AB1 = 'AB Rh+'
    AB2 = 'AB Rh-'
    A1 = 'A Rh+'
    A2 = 'A Rh-'
    B1 = 'B Rh+'
    B2 = 'B Rh-'
    O1 = 'AB Rh+'
    O2 = 'AB Rh+'

    GENDER_CHOICES = (
        (MALE, 'Erkek'),
        (FEMALE, 'Kadın'),
    )
    IsFormal = (
        (True, 'Spor Kulubü'),
        (False, 'Diger(Özel Salon-Dojo-Sportif Dernek)'),
    )

    IsCoach = (
        (True, 'Evet '),
        (False, 'Hayır'),
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
    WAITED = 'Beklemede'
    APPROVED = 'Onaylandı'
    PROPOUND = 'Onaya Gönderildi'
    DENIED = 'Reddedildi'

    STATUS_CHOICES = (
        (APPROVED, 'Onaylandı'),
        (PROPOUND, 'Onaya Gönderildi'),
        (DENIED, 'Reddedildi'),
        (WAITED, 'Beklemede'),
    )
    status = models.CharField(max_length=128, verbose_name='Onay Durumu', choices=STATUS_CHOICES, default=WAITED)

    # person form
    tc = models.CharField(max_length=120, null=True, blank=True)
    height = models.CharField(max_length=120, null=True, blank=True)
    weight = models.CharField(max_length=120, null=True, blank=True)
    birthplace = models.CharField(max_length=120, null=True, blank=True, verbose_name='Doğum Yeri')
    motherName = models.CharField(max_length=120, null=True, blank=True, verbose_name='Anne Adı')
    fatherName = models.CharField(max_length=120, null=True, blank=True, verbose_name='Baba Adı')
    profileImage = models.ImageField(upload_to='profile/', null=False, blank=False, verbose_name='Profil Resmi')
    birthDate = models.DateField(null=True, blank=True, verbose_name='Doğum Tarihi')
    bloodType = models.CharField(max_length=128, verbose_name='Kan Grubu', choices=BLOODTYPE, null=True, blank=True)
    gender = models.CharField(max_length=128, verbose_name='Cinsiyeti', choices=GENDER_CHOICES, default=MALE)
    # communicationform
    postalCode = models.CharField(max_length=120, null=True, blank=True)
    phoneNumber = models.CharField(max_length=120, null=True, blank=True)
    phoneNumber2 = models.CharField(max_length=120, null=True, blank=True)
    address = models.TextField(blank=True, null=True, verbose_name='Adres')
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='İl', related_name='user_city')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name='Ülke', related_name='user_country')

    # sportClup
    name = models.CharField(blank=True, null=True, max_length=120)
    shortName = models.CharField(blank=True, null=True, max_length=120)
    foundingDate = models.DateField(blank=True, null=True, max_length=120, verbose_name='Kuruluş Tarihi')
    clubMail = models.CharField(blank=True, null=True, max_length=120)
    logo = models.ImageField(upload_to='club/', null=True, blank=True, verbose_name='Kulüp Logo')

    creationDate = models.DateTimeField(auto_now_add=True)
    modificationDate = models.DateTimeField(auto_now=True)
    isFormal = models.BooleanField(default=True, choices=IsFormal)

    clubpostalCode = models.CharField(max_length=120, null=True, blank=True)
    clubphoneNumber = models.CharField(max_length=120, null=True, blank=True)
    clubphoneNumber2 = models.CharField(max_length=120, null=True, blank=True)
    clubaddress = models.TextField(blank=True, null=True, verbose_name='Adres')
    clubcity = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='İl')
    clubcountry = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name='Ülke')

    isCoach = models.BooleanField(default=False, choices=IsCoach)

    # userForm
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(max_length=254, blank=True)
    is_staff = models.BooleanField(default=False,
                                   help_text=('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(default=False,
                                    help_text=('Designates whether this user should be treated as active. '))

    # gerekli evraklar
    dekont = models.FileField(upload_to='dekont/', null=True, blank=True, verbose_name='Dekont ')
    petition = models.FileField(upload_to='dekont/', null=False, blank=False, verbose_name='Antrenör Yetki Belgesi  ')
    # Sportclup user
    role = models.ForeignKey(ClubRole, on_delete=models.DO_NOTHING, verbose_name='Üye Rolü')

    kademe_definition = models.CharField(null=True, blank=True, max_length=150)
    kademe_startDate = models.DateField(null=True, blank=True, verbose_name='Başlangıç Tarihi ')
    kademe_belge = models.FileField(upload_to='dekont/', null=True, blank=True, verbose_name='Belge')
    iban = models.CharField(max_length=120, null=True, blank=True, verbose_name='İban Adresi')

    # class Meta:
    #     default_permissions = ()

    # def save(self, force_insert=False, force_update=False):
    #     self.birthplace = self.birthplace.upper()
    #     self.motherName = self.motherName.upper()
    #     self.fatherName = self.fatherName.upper()
    #
    #     # self.first_name = self.first_name.upper()
    #     # self.last_name = self.last_name.upper()
    #     self.name = self.name.upper()
    #
    #     self.shortName = self.shortName.upper()
    #     super(PreRegistration, self).save(force_insert, force_update)
