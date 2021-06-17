from django.db import models


class AdminProfiles(models.Model):
    user_id = models.PositiveIntegerField(primary_key=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    profile_image = models.TextField(blank=True, null=True)
    profile_id = models.IntegerField(blank=True, null=True)
    profile_tip = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'admin_profiles'


class AutoPopulate(models.Model):
    vehicle_id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=5)
    make = models.CharField(max_length=36)
    model = models.CharField(max_length=36)
    color = models.CharField(max_length=36)

    class Meta:
        managed = False
        db_table = 'auto_populate'


class CategoryMenu(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=56)
    parent_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'category_menu'


class CiSessions(models.Model):
    session_id = models.CharField(primary_key=True, max_length=40)
    ip_address = models.CharField(max_length=45)
    user_agent = models.CharField(max_length=120)
    last_activity = models.PositiveIntegerField()
    user_data = models.TextField()

    class Meta:
        managed = False
        db_table = 'ci_sessions'


class CustomUploaderTable(models.Model):
    user_id = models.PositiveIntegerField(primary_key=True)
    images_data = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'custom_uploader_table'


class CustomerProfiles(models.Model):
    user_id = models.PositiveIntegerField(primary_key=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    street_address = models.CharField(max_length=60)
    city = models.CharField(max_length=60)
    state = models.CharField(max_length=50)
    zip = models.CharField(max_length=10)
    profile_image = models.TextField(blank=True, null=True)
    profile_id = models.IntegerField(blank=True, null=True)
    profile_tip = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customer_profiles'


class DeniedAccess(models.Model):
    ip_address = models.CharField(db_column='IP_address', max_length=45)  # Field name made lowercase.
    time = models.IntegerField()
    reason_code = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'denied_access'


class Egitim(models.Model):
    egitimid = models.IntegerField(primary_key=True)
    egitimadi = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'egitim'


class HakemKademeleri(models.Model):
    hakemkademeid = models.AutoField(primary_key=True)
    hakemkademeadi = models.CharField(max_length=120)

    class Meta:
        managed = False
        db_table = 'hakem_kademeleri'


class Iller(models.Model):
    ilid = models.IntegerField(primary_key=True)
    iladi = models.CharField(max_length=40)

    class Meta:
        managed = False
        db_table = 'iller'


class IpsOnHold(models.Model):
    ip_address = models.CharField(db_column='IP_address', max_length=45)  # Field name made lowercase.
    time = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ips_on_hold'


class KanGruplari(models.Model):
    kangrubu = models.CharField(primary_key=True, max_length=5)

    class Meta:
        managed = False
        db_table = 'kan_gruplari'


class Kategoriler(models.Model):
    kategoriid = models.IntegerField(primary_key=True)
    kategoriadi = models.CharField(max_length=20, blank=True, null=True)
    erkek = models.IntegerField(blank=True, null=True)
    bayan = models.IntegerField(blank=True, null=True)
    sayi = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'kategoriler'


class KulupTmp(models.Model):
    adi = models.CharField(max_length=200, blank=True, null=True)
    turadi = models.CharField(max_length=20, blank=True, null=True)
    turid = models.IntegerField(blank=True, null=True)
    tesciltarihi = models.DateField(blank=True, null=True)
    telefon = models.CharField(max_length=20, blank=True, null=True)
    iladi = models.CharField(max_length=60, blank=True, null=True)
    ilid = models.IntegerField(blank=True, null=True)
    kulupno = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'kulup_tmp'


class KulupTurleri(models.Model):
    kulupturid = models.AutoField(primary_key=True)
    kulupturadi = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'kulup_turleri'


class Kulupler(models.Model):
    kulupid = models.AutoField(primary_key=True)
    kulupadi = models.CharField(max_length=120)
    ilid = models.ForeignKey(Iller, models.DO_NOTHING, db_column='ilid', blank=True, null=True)
    kurulustarihi = models.DateField(blank=True, null=True)
    renk = models.CharField(max_length=120, blank=True, null=True)
    aktif = models.IntegerField()
    adres1 = models.CharField(max_length=400, blank=True, null=True)
    adres2 = models.CharField(max_length=400, blank=True, null=True)
    telefon = models.CharField(max_length=120, blank=True, null=True)
    ceptel = models.CharField(max_length=120, blank=True, null=True)
    kulupno = models.CharField(max_length=20)
    kulupturid = models.ForeignKey(KulupTurleri, models.DO_NOTHING, db_column='kulupturid', blank=True, null=True)
    faks = models.CharField(max_length=120, blank=True, null=True)
    eposta = models.CharField(max_length=120, blank=True, null=True)
    bankahesapno = models.CharField(max_length=120, blank=True, null=True)
    webadresi = models.CharField(max_length=120, blank=True, null=True)
    vd = models.CharField(max_length=120, blank=True, null=True)
    vdno = models.CharField(max_length=120, blank=True, null=True)
    yerlesim = models.CharField(max_length=200, blank=True, null=True)
    tesciltarihi = models.DateField(blank=True, null=True)
    aciklama = models.CharField(max_length=800, blank=True, null=True)
    rec_version = models.IntegerField(blank=True, null=True)
    insuser = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True,related_name='+')
    instime = models.DateTimeField(blank=True, null=True)
    upduser = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True,related_name='+')
    updtime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'kulupler'


class LoginErrors(models.Model):
    username_or_email = models.CharField(max_length=255)
    ip_address = models.CharField(db_column='IP_address', max_length=45)  # Field name made lowercase.
    time = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'login_errors'


class MalzHareket(models.Model):
    malzhareketid = models.AutoField(primary_key=True)
    tarih = models.DateField()
    aciklama = models.CharField(max_length=400, blank=True, null=True)
    malzemeid = models.ForeignKey('Malzemeler', models.DO_NOTHING, db_column='malzemeid')
    kulupid = models.ForeignKey(Kulupler, models.DO_NOTHING, db_column='kulupid')
    teslimalan = models.CharField(max_length=150, blank=True, null=True)
    miktar = models.DecimalField(max_digits=10, decimal_places=0)
    rec_version = models.IntegerField(blank=True, null=True)
    insuser_id = models.PositiveIntegerField(blank=True, null=True)
    instime = models.DateTimeField(blank=True, null=True)
    upduser_id = models.PositiveIntegerField(blank=True, null=True)
    updtime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'malz_hareket'


class Malzemeler(models.Model):
    malzemeid = models.AutoField(primary_key=True)
    malzemeadi = models.CharField(max_length=250, blank=True, null=True)
    aciklama = models.CharField(max_length=400, blank=True, null=True)
    kategori = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'malzemeler'


class ManagerProfiles(models.Model):
    user_id = models.PositiveIntegerField(primary_key=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    license_number = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=20)
    profile_image = models.TextField(blank=True, null=True)
    profile_id = models.IntegerField(blank=True, null=True)
    profile_tip = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'manager_profiles'


class Raporlar(models.Model):
    raporid = models.AutoField(primary_key=True)
    auth_user_id = models.IntegerField(blank=True, null=True)
    auth_profile_id = models.IntegerField(blank=True, null=True)
    komut = models.CharField(max_length=4000, blank=True, null=True)
    auth_level = models.IntegerField(blank=True, null=True)
    sporcuid = models.IntegerField(blank=True, null=True)
    zaman = models.DateTimeField(blank=True, null=True)
    durum = models.IntegerField(blank=True, null=True)
    prm1 = models.IntegerField(blank=True, null=True)
    prm2 = models.IntegerField(blank=True, null=True)
    prm3 = models.IntegerField(blank=True, null=True)
    prm4 = models.IntegerField(blank=True, null=True)
    prm5 = models.IntegerField(blank=True, null=True)
    sprm1 = models.CharField(max_length=400, blank=True, null=True)
    sprm2 = models.CharField(max_length=400, blank=True, null=True)
    sprm3 = models.CharField(max_length=400, blank=True, null=True)
    sprm4 = models.CharField(max_length=400, blank=True, null=True)
    sprm5 = models.CharField(max_length=400, blank=True, null=True)
    raporadi = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'raporlar'


class Registration(models.Model):
    reg_mode = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'registration'


class SporcuPuanlari(models.Model):
    sporcupuanid = models.AutoField(primary_key=True)
    sporcuid = models.ForeignKey('Sporcular', models.DO_NOTHING, db_column='sporcuid',related_name='+')
    turnuvaid = models.ForeignKey('Turnuvalar', models.DO_NOTHING, db_column='turnuvaid')
    kategoriid = models.ForeignKey(Kategoriler, models.DO_NOTHING, db_column='kategoriid')
    sira = models.IntegerField(blank=True, null=True)
    puan = models.IntegerField(blank=True, null=True)
    antrenorid2 = models.ForeignKey('Sporcular', models.DO_NOTHING, db_column='antrenorid2', blank=True, null=True,related_name='+')
    antrenorid1 = models.ForeignKey('Sporcular', models.DO_NOTHING, db_column='antrenorid1', blank=True, null=True,related_name='+')
    kulupid = models.ForeignKey(Kulupler, models.DO_NOTHING, db_column='kulupid', blank=True, null=True)
    siragrup = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'sporcu_puanlari'
        unique_together = (('sporcuid', 'kategoriid', 'turnuvaid'),)


class Sporcular(models.Model):
    sporcuid = models.AutoField(primary_key=True)

    # user
    adi = models.CharField(max_length=200)
    soyadi = models.CharField(max_length=200)
    eposta = models.CharField(max_length=200, blank=True, null=True)

    # person
    anneadi = models.CharField(max_length=200, blank=True, null=True)
    babaadi = models.CharField(max_length=200, blank=True, null=True)
    tcno = models.CharField(unique=True, max_length=11, blank=True, null=True)
    uyrukid = models.CharField(max_length=10, blank=True, null=True)
    dogumyeri = models.CharField(max_length=200, blank=True, null=True)
    dogumtarihi = models.DateField(blank=True, null=True)
    nufus_ilid = models.ForeignKey(Iller, models.DO_NOTHING, db_column='nufus_ilid', blank=True, null=True)
    nufus_ilce = models.CharField(max_length=100, blank=True, null=True)
    nufus_mahkoy = models.CharField(max_length=120, blank=True, null=True)
    nufus_ciltno = models.CharField(max_length=20, blank=True, null=True)
    nufus_ailesirano = models.CharField(max_length=20, blank=True, null=True)
    nufus_sirano = models.CharField(max_length=20, blank=True, null=True)
    kangrubu = models.CharField(max_length=5, blank=True, null=True)
    meslek = models.CharField(max_length=120, blank=True, null=True)
    kurum = models.CharField(max_length=120, blank=True, null=True)
    is_unvani = models.CharField(max_length=120, blank=True, null=True)
    is_adresi = models.CharField(max_length=200, blank=True, null=True)
    evtel = models.CharField(max_length=40, blank=True, null=True)
    istel = models.CharField(max_length=40, blank=True, null=True)
    ceptel = models.CharField(max_length=40, blank=True, null=True)
    ev_adresi = models.CharField(max_length=400, blank=True, null=True)

    # lisans
    lisansno = models.CharField(max_length=80, blank=True, null=True)
    antrenorid = models.ForeignKey('self', models.DO_NOTHING, db_column='antrenorid', blank=True, null=True,related_name='+')
    antrenorid2 = models.ForeignKey('self', models.DO_NOTHING, db_column='antrenorid2', blank=True, null=True,
                                    related_name='+')
    lisanstarihi = models.DateField(blank=True, null=True)
    kulupid = models.ForeignKey(Kulupler, models.DO_NOTHING, db_column='kulupid', blank=True, null=True)

    vize = models.DateField(blank=True, null=True)

    egitimid = models.PositiveIntegerField(blank=True, null=True)
    bankahesapno = models.CharField(max_length=120, blank=True, null=True)

    # roller
    sporcu = models.IntegerField()
    antrenor = models.IntegerField()
    hakem = models.IntegerField(blank=True, null=True)

    # Hakem

    hakemvize = models.DateField(blank=True, null=True)
    hakemkademeid = models.ForeignKey(HakemKademeleri, models.DO_NOTHING, db_column='hakemkademeid', blank=True,
                                      null=True)

    # antrenor

    antrenorkademeid = models.PositiveIntegerField(blank=True, null=True)
    antrenorvize = models.DateField(blank=True, null=True)


    yerlesimyeri = models.CharField(max_length=200, blank=True, null=True)
    rec_version = models.IntegerField()
    resim = models.CharField(max_length=800, blank=True, null=True)
    insuser_id = models.PositiveIntegerField(blank=True, null=True)
    instime = models.DateTimeField(blank=True, null=True)
    upsuser_id = models.PositiveIntegerField(blank=True, null=True)
    updtime = models.DateTimeField(blank=True, null=True)

    hakemvizetipi = models.PositiveIntegerField(blank=True, null=True)
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    mezunokul = models.CharField(max_length=200, blank=True, null=True)
    fedkayitno = models.PositiveIntegerField(blank=True, null=True)

    ayakkabi = models.CharField(max_length=120, blank=True, null=True)
    esofman = models.CharField(max_length=120, blank=True, null=True)
    tshirt = models.CharField(max_length=120, blank=True, null=True)
    raket = models.CharField(max_length=120, blank=True, null=True)

    cinsiyet = models.IntegerField(blank=True, null=True)
    yerlesim_ilid = models.IntegerField(blank=True, null=True)
    urlpart = models.CharField(max_length=2000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sporcular'


class TempRegistrationData(models.Model):
    reg_id = models.PositiveIntegerField()
    reg_time = models.IntegerField()
    user_name = models.CharField(max_length=12)
    user_pass = models.TextField()
    user_salt = models.CharField(max_length=32)
    user_email = models.CharField(max_length=255)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    street_address = models.CharField(max_length=60)
    city = models.CharField(max_length=60)
    state = models.CharField(max_length=50)
    zip = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'temp_registration_data'


class TmpSporcular(models.Model):
    sporcuid = models.PositiveIntegerField()
    adi = models.CharField(max_length=200)
    soyadi = models.CharField(max_length=200)
    anneadi = models.CharField(max_length=200, blank=True, null=True)
    babaadi = models.CharField(max_length=200, blank=True, null=True)
    tcno = models.CharField(max_length=11, blank=True, null=True)
    uyrukid = models.CharField(max_length=10, blank=True, null=True)
    dogumyeri = models.CharField(max_length=200, blank=True, null=True)
    dogumtarihi = models.DateField(blank=True, null=True)
    nufus_ilid = models.IntegerField(blank=True, null=True)
    nufus_ilce = models.CharField(max_length=100, blank=True, null=True)
    nufus_mahkoy = models.CharField(max_length=120, blank=True, null=True)
    nufus_ciltno = models.CharField(max_length=20, blank=True, null=True)
    nufus_ailesirano = models.CharField(max_length=20, blank=True, null=True)
    nufus_sirano = models.CharField(max_length=20, blank=True, null=True)
    kangrubu = models.CharField(max_length=5, blank=True, null=True)
    meslek = models.CharField(max_length=120, blank=True, null=True)
    kurum = models.CharField(max_length=120, blank=True, null=True)
    is_unvani = models.CharField(max_length=120, blank=True, null=True)
    is_adresi = models.CharField(max_length=200, blank=True, null=True)
    evtel = models.CharField(max_length=40, blank=True, null=True)
    istel = models.CharField(max_length=40, blank=True, null=True)
    ceptel = models.CharField(max_length=40, blank=True, null=True)
    ev_adresi = models.CharField(max_length=400, blank=True, null=True)
    eposta = models.CharField(max_length=200, blank=True, null=True)
    lisansno = models.CharField(max_length=80, blank=True, null=True)
    antrenorid = models.PositiveIntegerField(blank=True, null=True)
    lisanstarihi = models.DateField(blank=True, null=True)
    vize = models.DateField(blank=True, null=True)
    egitimid = models.PositiveIntegerField(blank=True, null=True)
    bankahesapno = models.CharField(max_length=120, blank=True, null=True)
    sporcu = models.IntegerField()
    antrenor = models.IntegerField()
    yerlesimyeri = models.CharField(max_length=200, blank=True, null=True)
    rec_version = models.IntegerField()
    resim = models.CharField(max_length=800)
    insuser_id = models.PositiveIntegerField(blank=True, null=True)
    instime = models.DateTimeField(blank=True, null=True)
    upsuser_id = models.PositiveIntegerField(blank=True, null=True)
    updtime = models.DateTimeField(blank=True, null=True)
    hakemkademeid = models.PositiveIntegerField(blank=True, null=True)
    kulupid = models.PositiveIntegerField(blank=True, null=True)
    hakem = models.IntegerField(blank=True, null=True)
    hakemvize = models.DateField(blank=True, null=True)
    antrenorkademeid = models.PositiveIntegerField(blank=True, null=True)
    antrenorvize = models.DateField(blank=True, null=True)
    hakemvizetipi = models.PositiveIntegerField(blank=True, null=True)
    user_id = models.PositiveIntegerField(blank=True, null=True)
    mezunokul = models.CharField(max_length=200, blank=True, null=True)
    fedkayitno = models.PositiveIntegerField(blank=True, null=True)
    ayakkabi = models.CharField(max_length=120, blank=True, null=True)
    esofman = models.CharField(max_length=120, blank=True, null=True)
    tshirt = models.CharField(max_length=120, blank=True, null=True)
    raket = models.CharField(max_length=120, blank=True, null=True)
    antrenorid2 = models.PositiveIntegerField(blank=True, null=True)
    cinsiyet = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tmp_sporcular'


class TurnDurumKodlari(models.Model):
    durumid = models.IntegerField(primary_key=True)
    durumadi = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'turn_durum_kodlari'


class TurnHakemleri(models.Model):
    turnhakemid = models.AutoField(primary_key=True)
    turnuvaid = models.ForeignKey('Turnuvalar', models.DO_NOTHING, db_column='turnuvaid')
    hakemid = models.ForeignKey(Sporcular, models.DO_NOTHING, db_column='hakemid')
    insuser_id = models.PositiveIntegerField(blank=True, null=True)
    instime = models.DateTimeField(blank=True, null=True)
    upduser_id = models.PositiveIntegerField(blank=True, null=True)
    updtime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'turn_hakemleri'


class TurnKategorileri(models.Model):
    turnkategoriid = models.AutoField(primary_key=True)
    turnuvaid = models.ForeignKey('Turnuvalar', models.DO_NOTHING, db_column='turnuvaid')
    kategoriid = models.ForeignKey(Kategoriler, models.DO_NOTHING, db_column='kategoriid')

    class Meta:
        managed = False
        db_table = 'turn_kategorileri'
        unique_together = (('kategoriid', 'turnuvaid'),)


class TurnKulupleri(models.Model):
    turnkulupid = models.IntegerField(primary_key=True)
    turnuvaid = models.ForeignKey('Turnuvalar', models.DO_NOTHING, db_column='turnuvaid')
    kulupid = models.ForeignKey(Kulupler, models.DO_NOTHING, db_column='kulupid')

    class Meta:
        managed = False
        db_table = 'turn_kulupleri'


class TurnSporcuAntrenorleri(models.Model):
    turnsporcuantrenorid = models.AutoField(primary_key=True)
    turnsporcuid = models.ForeignKey('TurnSporculari', models.DO_NOTHING, db_column='turnsporcuid')
    antrenorid = models.ForeignKey(Sporcular, models.DO_NOTHING, db_column='antrenorid')
    sira = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'turn_sporcu_antrenorleri'
        unique_together = (('turnsporcuid', 'antrenorid', 'sira'),)


class TurnSporculari(models.Model):
    turnsporcuid = models.AutoField(primary_key=True)
    antrenorid = models.IntegerField(blank=True, null=True)
    kulupid = models.IntegerField(blank=True, null=True)
    sporcuid = models.ForeignKey(Sporcular, models.DO_NOTHING, db_column='sporcuid')
    turnuvaid = models.ForeignKey('Turnuvalar', models.DO_NOTHING, db_column='turnuvaid')
    insuser_id = models.PositiveIntegerField(blank=True, null=True)
    instime = models.DateTimeField(blank=True, null=True)
    upduser_id = models.PositiveIntegerField(blank=True, null=True)
    updtime = models.DateTimeField(blank=True, null=True)
    kategoriid = models.ForeignKey(Kategoriler, models.DO_NOTHING, db_column='kategoriid')
    sira = models.IntegerField(blank=True, null=True)
    grupid = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'turn_sporculari'
        unique_together = (('turnuvaid', 'kategoriid', 'sporcuid'),)


class Turnuvalar(models.Model):
    turnuvaid = models.AutoField(primary_key=True)
    turnuvaadi = models.CharField(max_length=400, blank=True, null=True)
    basltarihi = models.DateField()
    bitistarihi = models.DateField()
    durumid = models.IntegerField(blank=True, null=True)
    aciklama = models.CharField(max_length=20, blank=True, null=True)
    kategoriid = models.ForeignKey(Kategoriler, models.DO_NOTHING, db_column='kategoriid', blank=True, null=True)
    rec_version = models.IntegerField(blank=True, null=True)
    insuser_id = models.PositiveIntegerField(blank=True, null=True)
    instime = models.DateTimeField(blank=True, null=True)
    upsuser_id = models.PositiveIntegerField(blank=True, null=True)
    updtime = models.DateTimeField(blank=True, null=True)
    basvurubasltarihi = models.DateField()
    basvurubitistarihi = models.DateField()
    mintarih = models.DateField(blank=True, null=True)
    maxtarih = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'turnuvalar'


class UserYetkiKodlari(models.Model):
    useryetkikodu = models.CharField(primary_key=True, max_length=21)
    useryetkiadi = models.CharField(max_length=40)

    class Meta:
        managed = False
        db_table = 'user_yetki_kodlari'


class UserYetkileri(models.Model):
    useryetkiid = models.AutoField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    useryetkikodu = models.ForeignKey(UserYetkiKodlari, models.DO_NOTHING, db_column='useryetkikodu')

    class Meta:
        managed = False
        db_table = 'user_yetkileri'
        unique_together = (('user', 'useryetkikodu'),)


class UsernameOrEmailOnHold(models.Model):
    username_or_email = models.CharField(max_length=255)
    time = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'username_or_email_on_hold'


class Users(models.Model):
    user_id = models.PositiveIntegerField(primary_key=True)
    user_name = models.CharField(unique=True, max_length=12)
    user_email = models.CharField(unique=True, max_length=255, blank=True, null=True)
    user_pass = models.CharField(max_length=60)
    user_salt = models.CharField(max_length=32)
    user_last_login = models.IntegerField(blank=True, null=True)
    user_login_time = models.IntegerField(blank=True, null=True)
    user_session_id = models.CharField(max_length=40, blank=True, null=True)
    user_date = models.IntegerField()
    user_modified = models.IntegerField()
    user_agent_string = models.CharField(max_length=32, blank=True, null=True)
    user_level = models.PositiveIntegerField()
    user_banned = models.CharField(max_length=1)
    passwd_recovery_code = models.CharField(max_length=60, blank=True, null=True)
    passwd_recovery_date = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'


class Vizeler(models.Model):
    vizeid = models.AutoField(primary_key=True)
    sporcuid = models.ForeignKey(Sporcular, models.DO_NOTHING, db_column='sporcuid')
    belgetarihi = models.DateField(blank=True, null=True)
    gecerliliktarihi = models.DateField()
    aciklama = models.CharField(max_length=200, blank=True, null=True)
    upduser_id = models.PositiveIntegerField(blank=True, null=True)
    updtime = models.DateTimeField(blank=True, null=True)
    insuser_id = models.PositiveIntegerField(blank=True, null=True)
    instime = models.DateTimeField(blank=True, null=True)
    vizetipi = models.IntegerField()
    rec_version = models.IntegerField()
    seviye = models.IntegerField()
    kayittipi = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'vizeler'