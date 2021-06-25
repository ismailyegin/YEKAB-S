from django.conf.urls import url
from django.urls import path

from ekabis.Views import DashboardViews, ClaimView, LogViews, AdminViews, HelpViews,DirectoryViews,UserViews,\
    CompanyView,EmployeeViews

app_name = 'ekabis'
urlpatterns = [

    # Dashboard
    path('anasayfa/admin/', DashboardViews.return_admin_dashboard, name='admin'),
    path('anasayfa/federasyon/', DashboardViews.return_directory_dashboard, name='federasyon'),
    path('anasayfa/personel/', DashboardViews.return_personel_dashboard, name='personel'),

    #
    # profile update yönetim
    path('yonetim/yonetim-kurul-profil-guncelle/', DirectoryViews.updateDirectoryProfile,
        name='yonetim-kurul-profil-guncelle'),
    # Admin
    path('admin/admin-profil-guncelle/', AdminViews.updateProfile,
        name='admin-profil-guncelle'),

    # Yönetim Kurulu
    path('yonetim/kurul-uyeleri/', DirectoryViews.return_directory_members, name='kurul-uyeleri'),
    path('yonetim/kurul-uyesi-ekle/', DirectoryViews.add_directory_member, name='kurul-uyesi-ekle'),
    path('yonetim/kurul-uyesi-duzenle/<int:pk>/', DirectoryViews.update_directory_member,
        name='kurul-uyesi-duzenle'),
    path('yonetim/kurul-uyeleri/sil/<int:pk>/', DirectoryViews.delete_directory_member,
        name='kurul-uyesi-sil'),
    path('yonetim/kurul-uye-rolleri/', DirectoryViews.return_member_roles, name='kurul-uye-rolleri'),
    path('yonetim/kurul-uye-rolleri/sil/<int:pk>/', DirectoryViews.delete_member_role,
        name='kurul_uye_rol_sil'),
    path('yonetim/kurul-uye-rol-duzenle/<int:pk>/', DirectoryViews.update_member_role,
        name='kurul-uye-rol-duzenle'),
    path('yonetim/kurullar/', DirectoryViews.return_commissions, name='kurullar'),
    path('yonetim/kurullar/sil/<int:pk>/', DirectoryViews.delete_commission,
        name='kurul_sil'),
    path('yonetim/kurul-duzenle/<int:pk>/', DirectoryViews.update_commission,
        name='kurul-duzenle'),
    path('yonetim/yonetim-kurul-profil-guncelle/', DirectoryViews.updateDirectoryProfile,
        name='yonetim-kurul-profil-guncelle'),

    # Kullanıcılar
    path('kullanici/kullanicilar/', UserViews.return_users, name='kullanicilar'),
    path('kullanici/kullanicilar/toplu', UserViews.UserAllMail, name='kullanicilar-toplu-mesaj'),
    path('kullanici/kullanici-duzenle/<int:pk>/', UserViews.update_user, name='kullanici-duzenle'),
    path('kullanici/kullanicilar/aktifet/<int:pk>/', UserViews.active_user,
        name='kullanici-aktifet'),
    path('kullanici/kullanicilar/kullanici-bilgi-gonder/<int:pk>/', UserViews.send_information,
        name='kullanici-bilgi-gonder'),

    #personeller
    path('personel/personeller/', EmployeeViews.return_employees, name='personeller'),
    path('personel/personel-ekle/', EmployeeViews.add_employee, name='personel-ekle'),
    path('personel/personel-duzenle/<int:pk>/', EmployeeViews.edit_employee, name='personel-duzenle'),


    path('personel/unvanListesi/', EmployeeViews.return_workdefinitionslist, name='unvanlistesi'),
    path('personel/Unvan-duzenle/<int:pk>/', EmployeeViews.edit_workdefinitionUnvan,name='unvan-duzenle'),
    path('personel/Unvansil/<int:pk>/', EmployeeViews.delete_employeetitle, name='unvan-sil'),

    path('personel/personel-profil-guncelle/', EmployeeViews.updateRefereeProfile,name='personel-profil-guncelle'),

    #   log kayıtlari
    path('log/log-kayitlari/', LogViews.return_log,
        name='logs'),

    path('rol/guncelle/<int:pk>/', DashboardViews.activeGroup,
        name='aktive-update'),

    path('rol/degisitir/<int:pk>/', AdminViews.activeGroup,
        name='sporcu-aktive-group'),

    #     destek ve talep

    path('destek-talep-listesi/', ClaimView.return_claim, name='destek-talep-listesi'),
    path('destek/Destekekle', ClaimView.claim_add, name='destek-talep-ekle'),
    path('destek/sil/<int:pk>/', ClaimView.claim_delete, name='destek-delete'),
    path('destek/guncelle/<int:pk>/', ClaimView.claim_update, name='destek-guncelle'),

    #     Yardım ve destek




    path('yardim', HelpViews.help, name='help'),

    #     company
    path('company/company-add/', CompanyView.return_add_Company, name='company-add'),
    path('company/company-list/', CompanyView.return_list_Company, name='company-list'),
    path('company/company-update/<int:pk>/', CompanyView.return_update_Company, name='company-update'),

    path('destek-talep-listesi', ClaimView.return_claim, name='destek-talep-listesi'),
    path('destek/Destekekle', ClaimView.claim_add, name='destek-talep-ekle'),
    path('destek/sil/<int:pk>/', ClaimView.claim_delete, name='destek-delete'),
    path('destek/guncelle/<int:pk>/', ClaimView.claim_update, name='destek-guncelle'),
]
