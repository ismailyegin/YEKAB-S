from django.db import models


class Products(models.Model):
    RAKET = 'RAKET'
    TOPLAR = 'TOPLAR'
    AYAKKABI = 'AYAKKABI'
    CANTA = 'CANTA'
    AKSESUAR = 'AKSESUAR'
    GRİP = 'GRİP'
    KORDAJ = 'KORDAJ'
    EKİPMAN = 'EKİPMAN'
    KIYAFET = 'KIYAFET'
    TISORT = 'TISORT'
    KITAP = 'KITAP'


    Category = (
        (RAKET, 'RAKET'),
        (TOPLAR, 'TOPLAR'),
        (AYAKKABI, 'AYAKKABI'),
        (CANTA, 'ÇANTA'),
        (AKSESUAR, 'AKSESUAR'),
        (GRİP, 'GRİP'),
        (KORDAJ, 'KORDAJ'),
        (EKİPMAN, 'EKİPMAN'),
        (KIYAFET, 'KIYAFET'),
        (TISORT, 'TISORT'),
        (KITAP, 'KİTAP')

    )

    creationDate = models.DateTimeField(auto_now_add=True)
    operationDate = models.DateTimeField(auto_now=True)


    name = models.CharField(max_length=120, null=False, blank=False)
    category = models.CharField(max_length=128, verbose_name='category', choices=Category, null=True, blank=True)
    stock = models.IntegerField(null=True, blank=True)
    suppeliers = models.CharField(max_length=120, null=True, blank=True)
    description = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return '%s ' % self.name
