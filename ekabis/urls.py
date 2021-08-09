from django.urls import path
from ekabis.Views import DashboardViews, ClaimView, LogViews, AdminViews, HelpViews, DirectoryViews, UserViews, \
    CompanyView, EmployeeViews, GroupView, SettingsViews, ConnectionRegionViews, YekaViews, BusinessBlogViews, \
    ExtraTimeViews, APIViews, CityViews, VacationDayViews, YekaCompetitionViews

app_name = 'ekabis'
urlpatterns = [
    path('anasayfa/maintenance-page/', AdminViews.viewRepairPage, name='view_repair_page'),
    # Dashboard
    path('anasayfa/admin/', DashboardViews.return_admin_dashboard, name='view_admin'),
    path('anasayfa/federasyon/', DashboardViews.return_directory_dashboard, name='view_federasyon'),
    path('anasayfa/personel/', DashboardViews.return_personel_dashboard, name='view_personel'),

    # Takvim notları
    path('anasayfa/takvim-not-ekle/', DashboardViews.add_calendarName, name='add_calendarName'),
    path('yeka/tatil-gunleri/', VacationDayViews.return_vacation_day, name='vacation_days'),
    path('yeka/tatil-gunu-ekle/', VacationDayViews.add_vacation_day, name='add_vacation_day'),
    path('yeka/tatil-gunu-sil/', VacationDayViews.delete_vacation_date, name='delete_vacation_day'),
    path('yeka/tatil-gunu-guncelle/<uuid:uuid>', VacationDayViews.update_vacation_date, name='update_vacation_day'),

    # Anasayfa Takvim notlar kaydet
    path('anasayfa/takvim-not-ekle/', DashboardViews.add_calendar, name='add_calendarfdk'),

    # profil güncelle
    path('admin/admin-profil-guncelle/', AdminViews.updateProfile,
         name='admin-profil-guncelle'),

    path('yonetim/yonetim-kurul-profil-guncelle/', DirectoryViews.updateDirectoryProfile,
         name='yonetim-kurul-profil-guncelle'),

    path('personel/personel-profil-guncelle/', EmployeeViews.updateRefereeProfile, name='personel-profil-guncelle'),

    # Yönetim
    path('kurul/kurul-uyeleri/', DirectoryViews.return_directory_members, name='view_directoryMember'),
    path('kurul/kurul-uyesi-ekle/', DirectoryViews.add_directory_member, name='add_directorymember'),
    path('kurul/kurul-uyesi-duzenle/<uuid:uuid>/', DirectoryViews.update_directory_member,
         name='change_directorymember'),
    path('kurul/kurul-uyeleri/sil/', DirectoryViews.delete_directory_member, name='delete_directorymember'),

    # yönetim rol
    path('kurul/kurul-uye-rolleri/', DirectoryViews.return_member_roles, name='view_directorymemberrole'),
    path('kurul/kurul-uye-rolleri/sil/', DirectoryViews.delete_member_role,
         name='delete_directorymemberrole'),
    path('kurul/kurul-uye-rol-duzenle/<uuid:uuid>/', DirectoryViews.update_member_role,
         name='change_directorymemberrole'),
    # yönetim kurul

    path('kurul/kurul-listesi', DirectoryViews.return_commissions, name='view_directorycommission'),
    path('kurul/kurul-sil/', DirectoryViews.delete_commission, name='delete_directorycommission'),
    path('kurul/kurul-duzenle/<uuid:pk>/', DirectoryViews.update_commission, name='change_directorycommission'),

    # Kullanıcılar
    path('kullanici/kullanicilar/', UserViews.return_users, name='view_user'),
    path('kullanici/kullanici-duzenle/<int:pk>/', UserViews.update_user, name='change_user'),
    path('kullanici/kullanicilar/aktifet<int:pk>/', UserViews.active_user, name='view_status'),
    path('kullanici/kullanici-mail-gonder/<int:pk>/', UserViews.send_information, name='view_email'),
    path('kullanici/kullanici-group-guncelle/<int:pk>/', UserViews.change_group_function, name='change_user_group'),

    # Personeller
    path('api-personel-listesi/', APIViews.GetEmployee.as_view(), name='view_employee_api'),
    path('personel/personel-listesi/', EmployeeViews.return_employees, name='view_employee'),
    path('personel/personel-ekle/', EmployeeViews.add_employee, name='add_employee'),
    path('personel/personel-duzenle/<uuid:pk>/', EmployeeViews.edit_employee, name='change_employee'),
    path('personel/personel-sil/', EmployeeViews.delete_employee, name='delete_employee'),

    path('personel/unvan-listesi/', EmployeeViews.return_workdefinitionslist, name='view_categoryitem'),
    path('personel/Unvan-duzenle/<uuid:uuid>/', EmployeeViews.edit_workdefinitionUnvan, name='change_categoryitem'),
    path('personel/Unvan-sil/', EmployeeViews.delete_employeetitle, name='delete_categoryitem'),

    #   log kayıtlari
    path('log/log-kayitlari/', LogViews.return_log, name='view_logs'),

    # activ grup  güncelle
    path('rol/guncelle/<int:pk>/', DashboardViews.activeGroup, name='change_activegroup'),

    # guruplar arasında tasıma işlemi
    path('rol/degisitir/<int:pk>/', AdminViews.activeGroup, name='sporcu-aktive-group'),

    #     destek ve talep

    path('destek/destek-talep-listesi/', ClaimView.return_claim, name='view_claim'),
    path('destek/destek/Destek-Ekle', ClaimView.claim_add, name='add_claim'),
    path('destek/destek/destek-sil/', ClaimView.delete_claim, name='delete_claim'),
    path('destek/destek/destek-guncelle/<uuid:uuid>/', ClaimView.claim_update, name='change_claim'),

    #     Yardım
    path('destek/yardim', HelpViews.help, name='view_help'),

    # firma
    path('firma/firma-ekle/', CompanyView.return_add_Company, name='add_company'),
    path('firma/firma-listesi/', CompanyView.return_list_Company, name='view_company'),
    path('firma/konsorsiyum-firma-ekle/', CompanyView.add_consortium, name='add_consortium'),
    path('firma/konsorsiyum/', CompanyView.view_consortium, name='view_consortium'),
    path('firma/konsorsiyum-guncelle/<uuid:uuid>/', CompanyView.return_update_consortium, name='change_consortium'),

    path('firma/api-firma-listesi/', APIViews.GetCompany.as_view(), name='view_company-api'),
    path('firma/firma-guncelle/<uuid:uuid>/', CompanyView.return_update_Company, name='change_company'),
    path('firma/firma-sil/', CompanyView.delete_company, name='delete_company'),

    # Dokuman isim ekleme
    path('firma/dokumanisim-ekle/', CompanyView.add_companyfilename, name='add_companyfilename'),
    path('firma/dokumanisim-listesi/', CompanyView.view_companyfilename, name='view_companyfilename'),

    path('firma/dokumanisim-guncelleme/<uuid:uuid>/', CompanyView.change_companyfilename,
         name='change_companyfilename'),
    path('firma/dokumanisim-sil/<uuid:uuid>/', CompanyView.delete_companyfilename,
         name='delete_companyfilename'),

    path('firma/dokumanisim-guncelleme/<uuid:uuid>/', CompanyView.change_companyfilename,
         name='change_companyfilename'),

    # Grup
    path('grup/grup-ekle/', GroupView.add_group, name='add_group'),
    path('grup/grup-listesi/', GroupView.return_list_group, name='view_group'),
    path('grup/grup-guncelleme/<int:pk>/', GroupView.return_update_group, name='change_group'),
    # grup izinleri
    path('grup/grup-izin-ekle/<int:pk>', GroupView.change_groupPermission, name='change_groupPermission'),
    # Ayarlar
    path('ayar/ayar-listesi/', SettingsViews.view_settinsList, name='view_settings'),
    path('ayar/ayar-guncelleme/<int:pk>/', SettingsViews.change_serttings, name='change_settings'),

    # Bağlantı Bölgesi
    path('baglanti/birim-ekle/', ConnectionRegionViews.return_connectionRegionUnit, name='view_units'),
    path('baglanti/birim-sil/', ConnectionRegionViews.delete_unit, name='delete_unit'),
    path('baglanti/birim-guncelle/<uuid:uuid>/', ConnectionRegionViews.update_unit, name='update_unit'),

    path('yeka/yeka-yarisma-listesi/<uuid:uuid>', YekaCompetitionViews.view_competition, name='view_competition'),
    path('yarisma/yarisma-ekle/<uuid:region>', YekaCompetitionViews.add_competition, name='add_competition'),

    path('yarisma/yarisma-sil/', YekaCompetitionViews.delete_competition, name='delete_competition'),
    path('yarisma/yarisma-guncelle/<uuid:region>/<uuid:competition>', YekaCompetitionViews.update_competition,
         name='change_competition'),
    path('yarisma/yarisma-is-bloklari-list/<uuid:uuid>/', YekaCompetitionViews.view_competition_yekabusinessBlog,
         name='view_competitionbusinessblog'),
    path('yarisma/yarisma-IsBlogu-ekle/<uuid:uuid>/', YekaCompetitionViews.add_yekacompetitionbusiness,
         name='add_yekacompetitionbusiness'),
    path('yarisma/yarisma-IsBlogu-guncelle/<uuid:uuid>/<uuid:competition>/',
         YekaCompetitionViews.change_yekacompetitionbusiness,
         name='change_yekacompetitionbusiness'),
    path('yarisma/yarisma-is-bloklari-ekle/<uuid:competition>/<uuid:yekabusiness>/<uuid:business>/',
         YekaCompetitionViews.change_yekacompetitionbusinessBlog, name='change_yekacompetitionbusinessBlog'),
    path('yarisma/yarisma-personeller/<uuid:uuid>', YekaCompetitionViews.yeka_person_list,
         name='view_yekacompetition_personel'),

    # alt yeka
    path('yarisma/alt-yeka-ekle/<uuid:uuid>', YekaCompetitionViews.add_sumcompetition, name='add_sumcompetition'),
    path('yarisma/alt-yeka-listesi/<uuid:uuid>', YekaCompetitionViews.return_sub_competition,
         name='view_sub_competition'),

    path('yarisma/alt-yeka-guncelle/<uuid:uuid>', YekaCompetitionViews.change_sumcompetition,
         name='change_sumcompetition'),

    path('baglanti/bolgesi-ekle/<uuid:uuid>', ConnectionRegionViews.add_connectionRegion, name='add_region'),
    path('baglanti/bolge-listesi/<uuid:uuid>', ConnectionRegionViews.return_connectionRegion, name='view_region'),

    path('baglanti/bölge-sil/', ConnectionRegionViews.delete_region, name='delete_region'),
    path('baglanti/bolge-guncelle/<uuid:uuid>/<uuid:yeka>', ConnectionRegionViews.update_region, name='update_region'),

    # Yeka

    path('yeka/yeka-ekle/', YekaViews.add_yeka, name='add_yeka'),

    path('yeka/yeka-listesi/', YekaViews.return_yeka, name='view_yeka'),
    path('yeka/api-yeka-listesi/', APIViews.GetYeka.as_view(), name='view_yeka-api'),

    path('yeka/yeka-sil/', YekaViews.delete_yeka, name='delete_yeka'),
    path('yeka/yeka-guncelle/<uuid:uuid>', YekaViews.update_yeka, name='change_yeka'),

    path('yeka/yeka-is-bloklari-semasi/<uuid:uuid>/', YekaViews.view_yekabusiness_gant, name='view_yekabusiness_gant'),
    path('yeka/yeka-is-bloklari-gant/<uuid:uuid>/', YekaViews.view_yekabusiness_gant, name='view_yekabusiness_gant2'),
    path('yeka/yeka-is-bloklari-incele-gant-detay/<uuid:yeka>/<uuid:yekabusiness>/',
         YekaViews.view_yekabusinessblog_gant, name='view_yekabusinessblog_gant'),

    # yekabusinessBlog
    path('yeka/yeka-is-bloklari-list/<uuid:uuid>/', YekaViews.view_yekabusinessBlog, name='view_yekabusinessBlog'),
    path('yeka/yeka-is-bloklari-ekle/<uuid:yeka>/<uuid:yekabusiness>/<uuid:business>/',
         YekaViews.change_yekabusinessBlog, name='change_yekabusinessBlog'),
    path('yeka/yeka-is-bloklari-firma-ekle/<uuid:yeka>/<uuid:yekabusinessblog>/',
         YekaViews.add_yekabusinessblog_company, name='add_yekabusinessblog_company'),

    path('yeka/alt-yeka-ekle/<uuid:uuid>', YekaViews.alt_yeka_ekle, name='add_sub_yeka'),
    path('yeka/alt-yekalar/<uuid:uuid>', YekaViews.return_sub_yeka, name='view_sub_yeka'),
    path('yeka/alt-yeka-guncelle/<uuid:uuid>', YekaViews.update_sub_yeka, name='change_sub_yeka'),

    path('yeka/yeka-personeller/<uuid:uuid>', YekaViews.yeka_person_list, name='view_yeka_personel'),

    path('yeka/yeka-firmalar/<uuid:uuid>', YekaViews.yeka_company_list, name='view_yeka_company'),
    path('yeka/yeka-firma-ata/', YekaViews.yeka_company_assignment, name='yeka_company_assignment'),
    path('yeka/remove-yeka-company/', YekaViews.yeka_company_remove, name='company_remove_yeka'),

    # yekabusiness
    path('yekaIsBlogu/yeka-IsBlogu-ekle/<uuid:uuid>/', BusinessBlogViews.add_yekabusiness, name='add_yekabusiness'),
    path('yekaIsBlogu/yeka-IsBlogu-guncelle/<uuid:uuid>/<uuid:yeka>/', BusinessBlogViews.change_yekabusiness,
         name='change_yekabusiness'),
    path('yekaIsBlogu/yekaIsBlogu-sil/', BusinessBlogViews.delete_yekabusiness, name='delete_yekabusiness'),
    # alt yeka
    path('yeka/alt-yeka-ekle/<uuid:uuid>', YekaViews.alt_yeka_ekle, name='add_sub_yeka'),
    # business
    path('isBlogu/isBlogu-listesi/', BusinessBlogViews.view_businessBlog, name='view_businessBlog'),
    path('isBlogu/isBlogu-ekle/', BusinessBlogViews.add_businessBlog, name='add_businessBlog'),
    path('isBlogu/isBlogu-guncelleme/<uuid:uuid>/', BusinessBlogViews.change_businessBlog, name='change_businessBlog'),
    path('isBlogu/isBlogu-sil/', BusinessBlogViews.delete_businessBlog, name='delete_businessBlog'),
    path('isBlogu/parametre-ekle/<uuid:uuid>', BusinessBlogViews.add_businessBlogParametre,
         name='add_businessBlogParametre'),
    path('isBlogu/parametre-guncelleme/<uuid:uuid>/<uuid:uuidparametre>',
         BusinessBlogViews.change_businessBlogParametre,
         name='change_businessBlogParametre'),
    path('isBlogu/parametre-sil/', BusinessBlogViews.delete_businessBlogParametre, name='delete_businessBlogParametre'),

    # Ek zaman
    path('yeka/ek-sure-listesi/', ExtraTimeViews.return_list_extra_time, name='view_extratime'),
    path('yeka/ek-sure-ekle/<uuid:business>/<uuid:businessblog>/', ExtraTimeViews.return_add_extra_time,
         name='add_extratime'),
    path('yeka/ek-sure-guncelle/<uuid:uuid>/', ExtraTimeViews.return_update_extra_time, name='change_extratime'),
    path('yeka/ek-sure-sil/', ExtraTimeViews.delete_extra_time, name='delete_extratime'),

    # Ekstra zaman file
    path('yeka/ek-sure-dosya-ekle/<uuid:uuid>/', ExtraTimeViews.add_extratimefile, name='add_extratimefile'),
    path('yeka/ek-sure-dosya-guncelle/<uuid:uuid>/<uuid:time>', ExtraTimeViews.change_extratimefile,
         name='change_extratimefile'),
    path('yeka/ek-sure-sil/', ExtraTimeViews.delete_extratimefile, name='delete_extratimefile'),

    path('ilce/ilce-getir/', CityViews.get_districts, name='ilce-getir'),
    path('firma/firma-kullanicilari/<uuid:uuid>/', CompanyView.return_user_company, name='view_company_user'),
    path('firma/firma-kullanicisi-ekle/', CompanyView.add_company_user, name='add_company_user'),
    path('firma/firma-kullanici-listesi/', CompanyView.company_users, name='company_users'),

    path('firma/firma-kullanicisi-gorevlendir/<uuid:uuid>/', CompanyView.assigment_company_user, name='assigment_company_user'),

]
