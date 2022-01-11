from django.conf.urls import url
from django.urls import path, include

from ekabis.Views import DashboardViews, ClaimView, LogViews, AdminViews, HelpViews, DirectoryViews, UserViews, \
    CompanyView, EmployeeViews, GroupView, SettingsViews, ConnectionRegionViews, YekaViews, BusinessBlogViews, \
    YekaBussinessBlogStaticView, HelpMenuViews, CityViews, ExtraTimeViews, APIViews, AcceptViews, YekaCompetitionViews, \
    VacationDayViews, ExtraTimeViews, CityViews, VacationDayViews, YekaCompetitionViews, HelpMenuViews, \
    YekaBussinessBlogStaticView, FactoryViews, PermissionView, AssociateDegreeViews, ReportViews, NotificationViews, \
    ProduceAmountViews, EskalasyonViews
from ekabis.services import general_methods, NotificationServices, DataService
from ekabis.services.general_methods import add_block

app_name = 'ekabis'

urlpatterns = [
    path('anasayfa/maintenance-page/', AdminViews.viewRepairPage, name='view_repair_page'),
    # Dashboard
    path('anasayfa/admin/', DashboardViews.return_admin_dashboard, name='view_admin'),
    path('anasayfa/federasyon/', DashboardViews.return_directory_dashboard, name='view_federasyon'),
    path('anasayfa/personel/', DashboardViews.return_personel_dashboard, name='view_personel'),
    path('anasayfa/yonetici/', DashboardViews.return_yonetici_dashboard, name='view_yonetici'),

    # Takvim notları
    path('anasayfa/takvim-not-ekle/', DashboardViews.add_calendarName, name='add_calendarName'),
    path('yeka/tatil-gunleri/', VacationDayViews.return_vacation_day, name='vacation_days'),
    path('yeka/tatil-gunu-ekle/', VacationDayViews.add_vacation_day, name='add_vacation_day'),
    path('yeka/tatil-gunu-sil/', VacationDayViews.delete_vacation_date, name='delete_vacation_day'),
    path('yeka/tatil-gunu-guncelle/<uuid:uuid>', VacationDayViews.update_vacation_date, name='update_vacation_day'),

    # Anasayfa Takvim notlar kaydet
    path('anasayfa/takvim-not-ekle/', DashboardViews.add_calendar, name='add_calendarfdk'),

    # profil güncelle
    # path('admin/admin-profil-guncelle/', AdminViews.updateProfile,
    #      name='admin-profil-guncelle'),
    #
    # path('yonetim/yonetim-kurul-profil-guncelle/', DirectoryViews.updateDirectoryProfile,
    #      name='yonetim-kurul-profil-guncelle'),

    # path('personel/personel-profil-guncelle/', EmployeeViews.updateRefereeProfile, name='personel-profil-guncelle'),

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
    path('log/log-kayitlari/', LogViews.view_log, name='view_logs'),

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
    path('firma/firma-listesi/', CompanyView.return_list_company, name='view_company'),
    path('firma/konsorsiyum-firma-ekle/', CompanyView.add_consortium, name='add_consortium'),
    path('firma/konsorsiyum/', CompanyView.view_consortium, name='view_consortium'),
    path('firma/konsorsiyum-guncelle/<uuid:uuid>/', CompanyView.change_consortium, name='change_consortium'),

    path('firma/api-firma-listesi/', APIViews.GetCompany.as_view(), name='view_company-api'),
    path('firma/firma-guncelle/<uuid:uuid>/', CompanyView.change_company, name='change_company'),
    path('firma/firma-sil/', CompanyView.delete_company, name='delete_company'),

    # Dokuman isim ekleme
    path('firma/dokumanisim-ekle/', CompanyView.add_company_file_name, name='add_companyfilename'),
    path('firma/dokumanisim-listesi/', CompanyView.view_company_file_name, name='view_companyfilename'),

    path('firma/dokumanisim-guncelleme/<uuid:uuid>/', CompanyView.change_company_file_name,
         name='change_companyfilename'),
    path('firma/dokumanisim-sil/', CompanyView.delete_company_file_name,
         name='delete_companyfilename'),

    # Grup
    path('grup/grup-ekle/', GroupView.add_group, name='add_group'),
    path('grup/grup-listesi/', GroupView.return_list_group, name='view_group'),
    path('grup/grup-guncelleme/<int:pk>/', GroupView.return_update_group, name='change_group'),
    # grup izinleri
    path('grup/grup-izin-ekle/<int:pk>', GroupView.change_groupPermission, name='change_groupPermission'),
    # Ayarlar

    path('ayar/sistem-ayar-listesi/', SettingsViews.view_settinsList, name='view_settings'),
    path('ayar/sistem-ayar-guncelleme/<int:pk>/', SettingsViews.change_serttings, name='change_settings'),

    # Birim Alanı
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
    path('yarisma/alt-yeka-ekle/<uuid:uuid>/<uuid:proposal_uuid>', YekaCompetitionViews.add_sumcompetition,
         name='add_sumcompetition'),
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
    path('yeka/yeka-yarismasi-is-bloklari-semasi/<uuid:uuid>/', YekaViews.view_yekacompetition_business_gant,
         name='view_yekacompeittion_business_gant'),
    path('yeka/yeka-is-bloklari-gant/<uuid:uuid>/', YekaViews.view_yekabusiness_gant, name='view_yekabusiness_gant2'),
    path('yeka/yeka-is-bloklari-incele-gant-detay/<uuid:yeka>/<uuid:yekabusiness>/',
         YekaViews.view_yekabusinessblog_gant, name='view_yekabusinessblog_gant'),

    # yekabusinessBlogyeka-lis
    path('yeka/yeka-is-bloklari-list/<uuid:uuid>/', YekaViews.view_yekabusinessBlog, name='view_yekabusinessBlog'),
    path('yeka/yeka-is-bloklari-ekle/<uuid:yeka>/<uuid:yekabusiness>/<uuid:business>/',
         YekaViews.change_yekabusinessBlog, name='change_yekabusinessBlog'),
    path('yeka/yeka-is-bloklari-firma-ekle/<uuid:business>/<uuid:yekabusinessblog>/',
         YekaViews.add_yekabusinessblog_company, name='add_yekabusinessblog_company'),

    path('yeka/alt-yeka-ekle/<uuid:uuid>', YekaViews.alt_yeka_ekle, name='add_sub_yeka'),
    path('yeka/alt-yekalar/<uuid:uuid>', YekaViews.return_sub_yeka, name='view_sub_yeka'),
    path('yeka/alt-yeka-guncelle/<uuid:uuid>', YekaViews.update_sub_yeka, name='change_sub_yeka'),

    path('yeka/yeka-personeller/<uuid:uuid>', YekaViews.yeka_person_list, name='view_yeka_personel'),

    # Yeka firma atama olmayacak başvurular olacak
    # path('yeka/yeka-firmalar/<uuid:uuid>', YekaViews.yeka_company_list, name='view_yeka_company'),
    # path('yeka/yeka-firma-ata/', YekaViews.yeka_company_assignment, name='yeka_company_assignment'),
    # path('yeka/remove-yeka-company/', YekaViews.yeka_company_remove, name='company_remove_yeka'),

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
    path('firma/firma-kullanicisi-gorevlendir/<uuid:uuid>/', CompanyView.assigment_company_user,
         name='assigment_company_user'),
    # Yardım Menusu
    path('yardim/yardim-metni-ekle/', HelpMenuViews.help_text_add, name='add_help_text'),
    path('yardim/yardim-metin-listesi/', HelpMenuViews.return_help_text, name='view_help_text'),
    path('yardim/yardim-metni-duzenle/<uuid:uuid>', HelpMenuViews.update_help_menu, name='change_help_text'),
    # Resmi Gazete
    path('yeka/resim-gazete-listesi/', YekaBussinessBlogStaticView.view_newspaper, name='view_newspaper'),
    path('yeka/resim-gazete-ekle/<uuid:business>/<uuid:businessblog>/', YekaBussinessBlogStaticView.add_newspaper,
         name='add_newspaper'),
    path('yeka/resim-gazete-guncelle/<uuid:uuid>/', YekaBussinessBlogStaticView.change_newspaper,
         name='change_newspaper'),
    path('yeka/resim-gazete-sil/', YekaBussinessBlogStaticView.delete_newspaper, name='delete_newspaper'),

    # Basvuru Dosya İsimleri
    path('yeka/yeka-basvuru-dosya-isim-listesi/', YekaBussinessBlogStaticView.view_yekaapplicationfilename,
         name='view_yekaapplicationfilename'),
    path('yeka/yeka-basvuru-dosya-isim-ekle/', YekaBussinessBlogStaticView.add_yekaapplicationfilename,
         name='add_yekaapplicationfilename'),
    path('yeka/yeka-basvuru-dosya-isim-guncelle/<uuid:uuid>/',
         YekaBussinessBlogStaticView.change_yekaapplicationfilename, name='change_yekaapplicationfilename'),
    path('yeka/yeka-basvuru-dosya-isim-sil/', YekaBussinessBlogStaticView.delete_yekaapplicationfilename,
         name='delete_yekaapplicationfilename'),

    # basvuru ayarları
    path('yeka/basvuru-ayarlari-ekle/<uuid:business>/<uuid:businessblog>/',
         YekaBussinessBlogStaticView.add_yekaapplication, name='add_yekaapplication'),
    path('yeka/basvuru-ayarlari-guncelle/<uuid:uuid>', YekaBussinessBlogStaticView.change_yekaapplication,
         name='change_yekaapplication'),

    # basvurular
    path('yeka/yeka-basvuru-listesi/<uuid:business>/<uuid:businessblog>', YekaBussinessBlogStaticView.view_application,
         name='view_application'),
    # basvuru dosya ekleme
    path('yeka/yeka-basvuru-dosya-ekle/<uuid:business>/<uuid:businessblog>/<uuid:applicationfile>',
         YekaBussinessBlogStaticView.view_applicationfile,
         name='view_applicationfile'),

    path('log/api-log-listesi/', APIViews.GetLog.as_view(), name='view_log_api'),

    # KABULLER
    path('yeka/kabul-listesi/<uuid:business>/<uuid:businessblog>/', AcceptViews.view_yeka_accept,
         name='view_yeka_accept'),
    path('yeka/kabul-ekle/<uuid:uuid>/', AcceptViews.add_yeka_accept,
         name='add_yeka_accept'),
    path('yeka/kabul-guncelle/<uuid:uuid>/<uuid:accept_uuid>/', AcceptViews.change_accept,
         name='change_yeka_accept'),
    path('yeka/kabul-sil/', AcceptViews.delete_accept, name='delete_accept'),

    # yarisma
    path('yeka/yeka-yarisma/<uuid:business>/<uuid:businessblog>', YekaBussinessBlogStaticView.change_competition,
         name='change_competition_block_'),

    path('yeka/yeka-yarisma-firma-ekle/<uuid:competition>',

         YekaBussinessBlogStaticView.add_competition_company,
         name='add_competition_company'),
    path('yeka/yeka-yarisma-firma-guncelle/<uuid:competition>/<uuid:uuid>',
         YekaBussinessBlogStaticView.change_competition_company,
         name='change_competition_company'),
    path('yeka/yeka-yarisma-firma-sil/',
         YekaBussinessBlogStaticView.delete_competition_company,
         name='delete_competition_company'),

    # sözleşme

    path('yeka/yeka-yarisma-sozlesme/<uuid:business>/<uuid:businessblog>',
         YekaBussinessBlogStaticView.change_yekacontract,
         name='change_yekacontract'),

    # aday yeka (Yekanın konumu icin öneriler)

    path('yeka/aday-yeka/<uuid:business>/<uuid:businessblog>',
         YekaBussinessBlogStaticView.change_yekaproposal,
         name='change_yekaproposal'),

    path('yeka/aday-yeka-ekle/<uuid:uuid>',
         YekaBussinessBlogStaticView.add_proposal,
         name='add_proposal'),

    path('yeka/aday-yeka-guncelle/<uuid:uuid>/<uuid:proposal>',
         YekaBussinessBlogStaticView.change_proposal,
         name='change_proposal'),

    path('yeka/aday-sil/',
         YekaBussinessBlogStaticView.delete_proposal,
         name='delete_proposal'),
    # kurum önerileri

    path('yeka/aday-yeka-kurum-gorusleri/<uuid:business>/<uuid:businessblog>',
         YekaBussinessBlogStaticView.change_proposal_active,
         name='change_proposal_active'),

    path('yeka/aday-yeka-kurum-listesi/<uuid:business>/<uuid:businessblog>',
         YekaBussinessBlogStaticView.view_institution,
         name='view_institution'),

    path('yeka/aday-yeka-kurum-guncelle/<uuid:business>/<uuid:businessblog>/<uuid:uuid>',
         YekaBussinessBlogStaticView.change_institution,
         name='change_institution'),

    path('yeka/aday-yeka-kurum-sil/',
         YekaBussinessBlogStaticView.delete_institution,
         name='delete_institution'),

    # Fabrika
    path('fabrika/fabrika-dokuman-ismi-ekle/', FactoryViews.add_factory_file_name, name='add_factory_file_name'),
    path('fabrika/fabrika-dokuman-isim-listesi/', FactoryViews.view_factory_file_name, name='views_factory_file_name'),
    path('fabrika/fabrika-dokuman-isim-guncelle/<uuid:uuid>/', FactoryViews.change_factory_file_name,
         name='change_factory_file_name'),
    path('fabrika/fabrika-dokuman-isim-sil/', FactoryViews.delete_factory_file_name, name='delete_factory_file_name'),
    path('yeka/fabrika-listesi/<uuid:business>/<uuid:businessblog>/', FactoryViews.view_yeka_factory,
         name='view_yeka_factory'),
    path('yeka/fabrika-ekle/<uuid:uuid>/', FactoryViews.add_yeka_factory, name='add_factory'),
    path('yeka/fabrika-guncelle/<uuid:uuid>/', FactoryViews.update_yeka_factory, name='update_factory'),
    path('yeka/fabrika-dokuman-ekle/<uuid:uuid>/', FactoryViews.add_factory_file, name='add_factory_file'),
    path('yeka/fabrika-dokuman-guncelle/<uuid:uuid>/<uuid:factory_uuid>/', FactoryViews.update_factory_file,
         name='change_factory_file'),
    path('fabrika/fabrika-sil/', FactoryViews.delete_factory, name='delete_factory'),
    path('fabrika/dokuman-sil/', FactoryViews.delete_factory_file, name='delete_factory_file'),

    # Koordinat
    path('aday-yeka/koordinat-ekle/<uuid:uuid>/<uuid:yeka_proposal_uuid>/', YekaBussinessBlogStaticView.add_coordinate,
         name='add_coordinate'),
    path('aday-yeka/koordinat-guncelle/<uuid:uuid>/<uuid:yeka_proposal_uuid>/',
         YekaBussinessBlogStaticView.change_coordinate,
         name='change_coordinate'),
    path('aday-yeka/koordinat-sil/', YekaBussinessBlogStaticView.delete_coordinate, name='delete_coordinate'),

    # Mahalle
    path('yeka/mahalle-getir/', CityViews.get_neighborhood, name='get_neighborhood'),

    # Konum
    path('aday-yeka/konum-ekle/<uuid:uuid>/<uuid:yeka_proposal_uuid>/', YekaBussinessBlogStaticView.add_location,
         name='add_location'),
    path('aday-yeka/konum-guncelle/<uuid:uuid>/<uuid:yeka_proposal_uuid>/', YekaBussinessBlogStaticView.change_location,
         name='change_location'),
    path('aday-yeka/konum-sil/', YekaBussinessBlogStaticView.delete_location, name='delete_location'),

    # aday yeka kurum önerileri
    path('yeka/aday-yeka-kurum-oneri-listesi/<uuid:yekaproposal>/<uuid:uuid>',
         YekaBussinessBlogStaticView.view_proposal_institution,
         name='view_proposal_institution'),

    path('yeka/aday-yeka-kurum-oneri-guncelle/<uuid:yekaproposal>/<uuid:proposal>/<uuid:uuid>',
         YekaBussinessBlogStaticView.change_proposal_institution,
         name='change_proposal_institution'),
    path('yeka/aday-yeka-kurum-oneri-sil',
         YekaBussinessBlogStaticView.delete_proposal_institution,
         name='delete_proposal_institution'),
    # firma kullanıcısı
    path('yeka/yeka-firma-kullanici-listesi/<uuid:business>/<uuid:businessblog>',
         YekaBussinessBlogStaticView.view_yeka_user,
         name='view_yeka_user'),
    path('yeka/yeka-firma-kullanici-ekle/<uuid:yekacompany>',
         YekaBussinessBlogStaticView.add_yeka_user,
         name='add_yeka_user'),
    path('yeka/yeka-firma-kullanici-guncelle/<uuid:yekacompany>/<uuid:companyuser>',
         YekaBussinessBlogStaticView.change_yeka_user,
         name='change_yeka_user'),
    path('yeka/yeka-firma-kullanici-sil',
         YekaBussinessBlogStaticView.delete_yeka_user,
         name='delete_yeka_user'),

    path('yeka/izin-listesi/', PermissionView.view_permission, name='view_permission'),
    path('yeka/izin-guncelle/<uuid:uuid>', PermissionView.change_permission, name='change_permission'),

    path('yeka/ufe-tufe/', YekaViews.view_ufe, name='view_ufe'),
    path('yeka/kur/', YekaViews.view_kur, name='view_kur'),

    # Onlisans-Süreci
    path('onlisans/onlisans-dokuman-ismi-ekle/', AssociateDegreeViews.add_associate_file_name,
         name='add_associate_file_name'),
    path('onlisans/onlisans-dokuman-isim-listesi/', AssociateDegreeViews.view_associate_file_name,
         name='view_associate_file_name'),
    path('onlisans/onlisans-dokuman-isim-guncelle/<uuid:uuid>/', AssociateDegreeViews.change_factory_file_name,
         name='change_associate_file_name'),
    path('onlisans/onlisans-dokuman-isim-sil/', AssociateDegreeViews.delete_associate_file_name,
         name='delete_associate_file_name'),
    path('onlisans/onlisans-belge-listesi/<uuid:business>/<uuid:businessblog>/',
         AssociateDegreeViews.view_yeka_associate_degree,
         name='view_yeka_associate_degree_file'),
    path('onlisans/onlisans-belge-ekle/<uuid:uuid>/', AssociateDegreeViews.add_associate_file,
         name='add_yeka_associate_degree_file'),
    path('onlisans/onlisans-belge-guncelle/<uuid:uuid>/<uuid:yeka_associate>/',
         AssociateDegreeViews.change_associate_file,
         name='change_associate_file'),
    path('onlisans/dokuman-sil/', AssociateDegreeViews.delete_associate_file, name='delete_associate_file'),

    path('yeka/firma-basvuru-guncelle/<uuid:uuid>/<uuid:business>/<uuid:yekabusinessblog>/',
         YekaViews.change_yekabusinessblog_company,
         name='change_yekabusinessblog_company'),

    path('test/test', YekaViews.test_yeka, name='test'),

    # yeka ve yarışmada kolay ulaşım sayfası
    path('yeka/yeka-detay/<uuid:uuid>/', YekaViews.view_yeka_detail,
         name='view_yeka_detail'),

    path('yeka/yarisma-listesi/', APIViews.GetYekaCompetition.as_view(), name='view_competition_api'),
    path('yeka/yeka-test/<uuid:uuid>/', YekaViews.test, name='test'),

    path('yeka/yeka-yarisma-detay/<uuid:uuid>/', YekaCompetitionViews.view_yeka_competition_detail,
         name='view_yeka_competition_detail'),
    path('yeka/alt-yeka-detay/<uuid:uuid>/', YekaCompetitionViews.view_sub_yeka_competition_detail,
         name='view_sub_yeka_competition_detail'),
    # #RAPORLAMA
    path('yeka/yeka-rapor/', YekaViews.select_report,
         name='select_report'),
    # path('yeka/rapor-il-yarisma-listesi/<uuid:uuid>/', ReportViews.view_city_competition,
    #      name='view_city_competition'),
    #
    # path('yeka/api-yeka-yarisma-listesi/', ReportViews.GetYekaCompetition.as_view(), name='get_yeka_competition'),

    # dependense finish date -start date

    path('yeka/yeka-bagimlilik/', YekaViews.view_dependence, name='view_dependence'),

    #     şehirleri renklendirme

    path('yeka/blockAdd/', add_block, name='add_block'),

    path('yeka/yeka-baglantı-bolgesi-renkleri/', DashboardViews.api_connection_region_cities,
         name='api_connection_region_cities'),
    path('yeka/yeka-baglantı-bolgesi-yarismalari/', DashboardViews.api_connection_region_competitions,
         name='api_connection_region_competitions'),
    path('yeka/yarisma-kabul-toplam/', DashboardViews.api_yeka_accept,
         name='api_yeka_accept'),

    path('yeka/yeka-rapor-listesi/', ReportViews.view_report, name='view_report'),

    path('yeka/basvuru-firma-ekle/', YekaBussinessBlogStaticView.add_competition_company_select,
         name='add_competition_company_select'),

    path('yeka/api-basvuru/', YekaBussinessBlogStaticView.add_competition_company_select_api,
         name='add_competition_company_select_api'),

    path('bildirim/bildirim-getir/', NotificationViews.get_notification, name='bildirim-getir'),
    path('bildirim/bildirimler/', NotificationViews.view_notification, name='bildirimler'),
    path('bildirim/bildirim-okundu/<int:id>', NotificationViews.is_read, name='bildirim-okundu-yap'),
    path('bildirim/okundu-isaretle/', NotificationViews.make_is_read, name='bildirim-okundu-isaretle'),

    # Alım Garantisi
    path('yeka/yarisma-uretim-miktari-ekle/<uuid:yeka_business_uuid>/<uuid:yeka_business_block_uuid>/',
         ProduceAmountViews.add_produce_amount,
         name='add_produce_amount'),
    path('yeka/yarisma-uretim-miktari-guncelle/<uuid:uuid>/<uuid:yeka_business_uuid>/',
         ProduceAmountViews.change_produce_amount,
         name='change_produce_amount'),
    path('yeka/yarisma-uretim-miktarlari/<uuid:yeka_business_uuid>/<uuid:yeka_business_block_uuid>/',
         ProduceAmountViews.view_business_block_produce_amount,
         name='view_produce_amount'),

    path('yeka/uretim-miktari-sil/', ProduceAmountViews.delete_produce_amount, name='delete_produce_amount'),

    path('yeka/alt-yekaya-aday-yeka-belirle/<uuid:yeka_business>/<uuid:yeka_business_block>/',
         YekaBussinessBlogStaticView.proposal_add_sub_yeka,
         name='proposal_add_sub_yeka'),

    path('yeka/kaynak-turu-yeka/<str:type>', YekaViews.view_yeka_by_type, name='view_yeka_by_type'),

    path('yeka/yeka-baglanti-bolge-getir/', YekaViews.get_region, name='get_region'),
    path('yeka/yeka-yarisma-getir/', YekaViews.get_yeka_competition, name='get_yeka_competition'),
    path('yeka/yeka-firma-basvuru/', YekaViews.company_application, name='company_aplication'),
    path('yeka/yeka-firma-basvuru-yap/', YekaViews.make_application, name='yeka_make_aplication_company'),
    path('yeka/basvuru-listesi/', APIViews.GetApplicationCompany.as_view(), name='view_application_company'),

    path('yeka/yarisma-basvurusu-getir/', YekaViews.get_yeka_company, name='get_yeka_company'),
    path('yeka/yarisma-dosya-kaydet/', YekaViews.save_company_app_file, name='save_company_app_file'),
    path('yeka/yeka-basvuru-dosya-sil/', YekaViews.delete_yeka_company_file, name='delete_yeka_company_file'),
    path('yeka/yeka-eskalasyon/<uuid:uuid>', EskalasyonViews.EskalasyonCalculation, name='eskalasyon_hesapla'),
    path('yeka/yeka-tufe-second-month/<str:date>/', EskalasyonViews.month_value_tufe_ufe,
         name='second_month_value_tufe'),
    path('yeka/yeka-eskalasyon-hesapla/', EskalasyonViews.yeka_competition_eskalasyon,
         name='yeka_competition_eskalasyon'),
    path('yeka/yeka-yarisma-rapor/', YekaViews.yeka_report, name='yeka_report'),
    path('yeka/yeka-yarisma-firma-getir/', YekaViews.get_yeka_competition_company, name='get_yeka_competition_company'),
    path('yeka/yeka-yarisma-aday-yeka-getir/', YekaViews.get_yeka_competition_proposal,
         name='get_yeka_competition_proposal'),
    path('yeka/yeka-yarisma-guncel-fiyat/', YekaViews.get_yeka_competition_eskalasyon,
         name='get_yeka_competition_eskalasyon'),

    path('yeka/butun-yekalar/', DashboardViews.api_yeka_by_type,
         name='api_yeka_by_type'),
    path('yeka/initial_data/', general_methods.initial_data, name='add_setting_data'),

    path('yeka/initial_data_success/', DashboardViews.success_initial_data, name='initial_data_success_page'),
    path('yeka/initial_data_error/', DashboardViews.error_initial_data, name='initial_data_error_page'),
    path('yeka/search_person/', EmployeeViews.search_person, name='search_person'),
    # path('yeka/il/', CityViews.add_city, name='city_add'),
    # path('yeka/ilce/', CityViews.add_district, name='´district_add'),
    # path('yeka/mahalle/', CityViews.add_neighborhood, name='neighborhood_add'),
    # path('yeka/is-bloklari/', BusinessBlogViews.data_business_blog, name='business_block_add'),
    # path('yeka/is-blok-parametre/', BusinessBlogViews.data_parameter, name='data_business_block_parameter'),
    # path('yeka/is-blok-parametre-id/', BusinessBlogViews.data_parameter_block_id, name='data_block_parameter_id'),
    path('yeka/tum-bildirim-okundu-yap/', NotificationViews.read_notification_all, name='read_notification_all'),
    path('yeka/yarisma-teminat-listesi/<uuid:yeka_business>/<uuid:yeka_business_block>',
         YekaBussinessBlogStaticView.guaranteeListYekaCompetition, name='guaranteeListYekaCompetition'),
    path('yeka/teminat-ekle/<uuid:uuid>', YekaBussinessBlogStaticView.add_guarantee, name='add_guarantee'),
    path('yeka/teminat-guncelle/<uuid:uuid>/<uuid:guarantee>', YekaBussinessBlogStaticView.change_guarantee,
         name='change_guarantee'),
    path('yeka/yeka-teminat-sil/', YekaBussinessBlogStaticView.delete_guarantee, name='delete_guarantee'),
    path('yeka/yeka-kurum-gorusleri-rapor', ReportViews.proposal_yeka_report, name='proposal_yeka_report'),
    path('yeka/is-blok-sure', YekaViews.yeka_business_time, name='yeka_business_time'),
    path('yeka/yeka-yarismalari-getir/', YekaViews.getYekaCompetitions, name='yeka-yarismalari-getir'),

    # Bütçe
    path('yeka/yarisma-butce-listesi/<uuid:yeka_business>/<uuid:yeka_business_block>',
         YekaBussinessBlogStaticView.budgetYekaCompetition, name='budget-yeka-competition-list'),
    path('yeka/butce-ekle/<uuid:uuid>', YekaBussinessBlogStaticView.add_budget, name='add_budget'),
    path('yeka/yarisma-istihdam-listesi/<uuid:yeka_business>/<uuid:yeka_business_block>',
         YekaBussinessBlogStaticView.employmentYekaCompetition, name='employment-yeka-competition-list'),
    path('yeka/istihdam-ekle/<uuid:uuid>', YekaBussinessBlogStaticView.add_employment, name='add_employment'),
    path('yeka/yeka-butce-sil/', YekaBussinessBlogStaticView.delete_budget, name='delete_budget'),
    path('yeka/yeka-istihdam-sil/', YekaBussinessBlogStaticView.delete_employment, name='delete_employment'),
    path('yeka/butce-guncelle/<uuid:uuid>/<uuid:budget_uuid>', YekaBussinessBlogStaticView.change_budget,
         name='change_budget'),

    path('yeka/yarisma-personel-ata', YekaViews.competition_personal_assigment, name='competition_personal_assigment'),

]
