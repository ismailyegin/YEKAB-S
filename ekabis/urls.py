from django.urls import path
from ekabis.Views import DashboardViews, ClaimView, LogViews, AdminViews, HelpViews, DirectoryViews, UserViews, \
    CompanyView, EmployeeViews, GroupView, SettingsViews, ConnectionRegionViews, YekaViews, BusinessBlogViews

app_name = 'ekabis'
urlpatterns = [
    path('maintenance-page/', AdminViews.viewRepairPage, name='view_repair_page'),
    # Dashboard
    path('anasayfa/admin/', DashboardViews.return_admin_dashboard, name='view_admin'),
    path('anasayfa/federasyon/', DashboardViews.return_directory_dashboard, name='view_federasyon'),
    path('anasayfa/personel/', DashboardViews.return_personel_dashboard, name='view_personel'),

    # profil güncelle
    path('admin/admin-profil-guncelle/', AdminViews.updateProfile,
         name='admin-profil-guncelle'),

    path('yonetim/yonetim-kurul-profil-guncelle/', DirectoryViews.updateDirectoryProfile,
         name='yonetim-kurul-profil-guncelle'),

    path('personel/personel-profil-guncelle/', EmployeeViews.updateRefereeProfile, name='personel-profil-güncelle'),

    # Yönetim
    path('kurul-uyeleri/', DirectoryViews.return_directory_members, name='view_directoryMember'),
    path('kurul-uyesi-ekle/', DirectoryViews.add_directory_member, name='add_directorymember'),
    path('kurul-uyesi-duzenle/<uuid:uuid>/', DirectoryViews.update_directory_member,
         name='change_directorymember'),
    path('kurul-uyeleri/sil/', DirectoryViews.delete_directory_member, name='delete_directorymember'),

    # yönetim rol
    path('kurul-uye-rolleri/', DirectoryViews.return_member_roles, name='view_directorymemberrole'),
    path('kurul-uye-rolleri/sil/', DirectoryViews.delete_member_role,
         name='delete_directorymemberrole'),
    path('kurul-uye-rol-duzenle/<uuid:uuid>/', DirectoryViews.update_member_role,
         name='change_directorymemberrole'),
    # yönetim kurul

    path('kurullar/', DirectoryViews.return_commissions, name='view_directorycommission'),
    path('kurullar/sil/', DirectoryViews.delete_commission, name='delete_directorycommission'),
    path('kurul-duzenle/<uuid:pk>/', DirectoryViews.update_commission, name='change_directorycommission'),

    # Kullanıcılar
    path('kullanici/kullanicilar/', UserViews.return_users, name='view_user'),
    path('kullanici/kullanici-duzenle/<int:pk>/', UserViews.update_user, name='change_user'),
    path('kullanici/kullanicilar/aktifet<int:pk>/', UserViews.active_user, name='view_status'),
    path('kullanici/kullanici-mail-gonder/<int:pk>/', UserViews.send_information, name='view_email'),
    path('kullanici/kullanici-group-guncelle/<int:pk>/', UserViews.change_group_function, name='change_user_group'),

    # Personeller
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

    path('destek-talep-listesi/', ClaimView.return_claim, name='view_claim'),
    path('destek/Destek-Ekle', ClaimView.claim_add, name='add_claim'),
    path('destek/destek-sil/', ClaimView.delete_claim, name='delete_claim'),
    path('destek/destek-guncelle/<uuid:uuid>/', ClaimView.claim_update, name='change_claim'),

    #     Yardım
    path('yardim', HelpViews.help, name='view_help'),

    # firma
    path('firma/firma-ekle/', CompanyView.return_add_Company, name='add_company'),
    path('firma/firma-listesi/', CompanyView.return_list_Company, name='view_company'),
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
    path('baglanti/bolge-ekle/', ConnectionRegionViews.return_connectionRegion, name='view_region'),
    path('baglanti/bölge-sil/', ConnectionRegionViews.delete_region, name='delete_region'),
    path('baglanti/bolge-guncelle/<uuid:uuid>/', ConnectionRegionViews.update_region, name='update_region'),
    path('baglanti/kapasite-ekle/<uuid:uuid>', ConnectionRegionViews.return_connectionCapacity, name='view_capacity'),
    path('baglanti/kapasite-guncelle/<uuid:uuid>', ConnectionRegionViews.update_capacity,
         name='update-region-capacity'),
    path('baglanti/kapasite-sil/', ConnectionRegionViews.delete_capacity, name='delete_capacity'),
    # Yeka
    path('yeka/yeka-ekle/', YekaViews.return_yeka, name='view_yeka'),
    path('yeka/yeka-sil/', YekaViews.delete_yeka, name='delete_yeka'),
    path('yeka/yeka-guncelle/<uuid:uuid>', YekaViews.update_yeka, name='change_yeka'),
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


    # yekabusiness
    path('yekaIsBlogu/yekaIsBlogu-ekle/', BusinessBlogViews.add_yekabusiness, name='add_yekabusiness'),
    path('yekaIsBlogu/yekaIsBlogu-listesi/', BusinessBlogViews.view_yekabusiness, name='view_yekabusiness'),

]
