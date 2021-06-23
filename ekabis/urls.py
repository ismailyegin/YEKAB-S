from django.conf.urls import url

from ekabis.Views import DashboardViews, ClaimView, LogViews, AdminViews, HelpViews,DirectoryViews,UserViews,\
    CompanyView,EmployeeViews

app_name = 'ekabis'
urlpatterns = [

    # Dashboard
    url(r'anasayfa/admin/$', DashboardViews.return_admin_dashboard, name='admin'),
    url(r'anasayfa/federasyon/$', DashboardViews.return_directory_dashboard, name='federasyon'),
    url(r'anasayfa/personel/$', DashboardViews.return_personel_dashboard, name='personel'),

    #
    # profile update yönetim
    url(r'yonetim/yonetim-kurul-profil-guncelle/$', DirectoryViews.updateDirectoryProfile,
        name='yonetim-kurul-profil-guncelle'),
    # Admin
    url(r'admin/admin-profil-guncelle/$', AdminViews.updateProfile,
        name='admin-profil-guncelle'),

    # Yönetim Kurulu
    url(r'yonetim/kurul-uyeleri/$', DirectoryViews.return_directory_members, name='kurul-uyeleri'),
    url(r'yonetim/kurul-uyesi-ekle/$', DirectoryViews.add_directory_member, name='kurul-uyesi-ekle'),
    url(r'yonetim/kurul-uyesi-duzenle/(?P<pk>\d+)$', DirectoryViews.update_directory_member,
        name='kurul-uyesi-duzenle'),
    url(r'yonetim/kurul-uyeleri/sil/(?P<pk>\d+)$', DirectoryViews.delete_directory_member,
        name='kurul-uyesi-sil'),
    url(r'yonetim/kurul-uye-rolleri/$', DirectoryViews.return_member_roles, name='kurul-uye-rolleri'),
    url(r'yonetim/kurul-uye-rolleri/sil/(?P<pk>\d+)$', DirectoryViews.delete_member_role,
        name='kurul_uye_rol_sil'),
    url(r'yonetim/kurul-uye-rol-duzenle/(?P<pk>\d+)$', DirectoryViews.update_member_role,
        name='kurul-uye-rol-duzenle'),
    url(r'yonetim/kurullar/$', DirectoryViews.return_commissions, name='kurullar'),
    url(r'yonetim/kurullar/sil/(?P<pk>\d+)$', DirectoryViews.delete_commission,
        name='kurul_sil'),
    url(r'yonetim/kurul-duzenle/(?P<pk>\d+)$', DirectoryViews.update_commission,
        name='kurul-duzenle'),
    url(r'yonetim/yonetim-kurul-profil-guncelle/$', DirectoryViews.updateDirectoryProfile,
        name='yonetim-kurul-profil-guncelle'),

    # Kullanıcılar
    url(r'kullanici/kullanicilar/$', UserViews.return_users, name='kullanicilar'),
    url(r'kullanici/kullanicilar/toplu$', UserViews.UserAllMail, name='kullanicilar-toplu-mesaj'),
    url(r'kullanici/kullanici-duzenle/(?P<pk>\d+)$', UserViews.update_user, name='kullanici-duzenle'),
    url(r'kullanici/kullanicilar/aktifet/(?P<pk>\d+)$', UserViews.active_user,
        name='kullanici-aktifet'),
    url(r'kullanici/kullanicilar/kullanici-bilgi-gonder/(?P<pk>\d+)$', UserViews.send_information,
        name='kullanici-bilgi-gonder'),

    #personeller
    url(r'personel/personeller/$', EmployeeViews.return_employees, name='personeller'),
    url(r'personel/personeller/hepsi/$', EmployeeViews.return_employees_all, name='personeller-all'),
    url(r'personel/personel-ekle/$', EmployeeViews.add_employee, name='personel-ekle'),
    url(r'personel/personel-duzenle/(?P<pk>\d+)$', EmployeeViews.edit_employee, name='personel-duzenle'),
    url(r'personel/unvanListesi/$', EmployeeViews.return_workdefinitionslist, name='unvanlistesi'),
    url(r'personel/istanimi/sil/(?P<pk>\d+)$', EmployeeViews.delete_workdefinition,
        name='istanimi-sil'),
    url(r'personel/isTanimi-duzenle/(?P<pk>\d+)$', EmployeeViews.edit_workdefinition,
        name='istanimi-duzenle'),
    url(r'personel/Unvan-duzenle/(?P<pk>\d+)$', EmployeeViews.edit_workdefinitionUnvan,
        name='unvan-duzenle'),
    url(r'personel/personel-profil-guncelle/$', EmployeeViews.updateRefereeProfile,
        name='personel-profil-guncelle'),
    url(r'personel/Unvansil/(?P<pk>\d+)$', EmployeeViews.delete_employeetitle,
        name='unvan-sil'),





    #   log kayıtlari
    url(r'log/log-kayitlari/$', LogViews.return_log,
        name='logs'),

    url(r'rol/guncelle/(?P<pk>\d+)$', DashboardViews.activeGroup,
        name='aktive-update'),

    url(r'rol/degisitir/(?P<pk>\d+)$', AdminViews.activeGroup,
        name='sporcu-aktive-group'),

    #     destek ve talep

    url(r'destek-talep-listesi', ClaimView.return_claim, name='destek-talep-listesi'),
    url(r'destek/Destekekle', ClaimView.claim_add, name='destek-talep-ekle'),
    url(r'destek/sil/(?P<pk>\d+)$', ClaimView.claim_delete, name='destek-delete'),
    url(r'destek/guncelle/(?P<pk>\d+)$', ClaimView.claim_update, name='destek-guncelle'),

    #     Yardım ve destek

    url(r'yardim$', HelpViews.help, name='help'),

    #     company
    url(r'company/company-add/$', CompanyView.return_add_Company, name='company-add'),
    url(r'company/company-list/$', CompanyView.return_list_Company, name='company-list'),
    url(r'company/company-update/(?P<pk>\d+)$', CompanyView.return_update_Company, name='company-update'),

    url(r'destek-talep-listesi', ClaimView.return_claim, name='destek-talep-listesi'),
    url(r'destek/Destekekle', ClaimView.claim_add, name='destek-talep-ekle'),
    url(r'destek/sil/(?P<pk>\d+)$', ClaimView.claim_delete, name='destek-delete'),
    url(r'destek/guncelle/(?P<pk>\d+)$', ClaimView.claim_update, name='destek-guncelle'),
]
