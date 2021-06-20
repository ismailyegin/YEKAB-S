from django.conf.urls import url

from ekabis.Views import DashboardViews,ArsivView,ClaimView,LogViews,AdminViews,HelpViews

app_name = 'ekabis'
urlpatterns = [

    # Dashboard
    url(r'anasayfa/admin/$', DashboardViews.return_admin_dashboard, name='admin'),
    url(r'anasayfa/sehir-sporcu-sayisi/$', DashboardViews.City_athlete_cout, name='sehir-sporcu-sayisi'),
    url(r'anasayfa/sporcu/$', DashboardViews.return_athlete_dashboard, name='sporcu'),
    url(r'anasayfa/hakem/$', DashboardViews.return_referee_dashboard, name='hakem'),
    url(r'anasayfa/antrenor/$', DashboardViews.return_coach_dashboard, name='antrenor'),
    url(r'anasayfa/federasyon/$', DashboardViews.return_directory_dashboard, name='federasyon'),
    url(r'anasayfa/kulup-uyesi/$', DashboardViews.return_club_user_dashboard, name='kulup-uyesi'),

    #   log kayıtlari

    url(r'log/log-kayitlari/$', LogViews.return_log,
        name='logs'),

    url(r'message/messages/$', DashboardViews.return_message,
        name='message'),

    url(r'rol/guncelle/(?P<pk>\d+)$', DashboardViews.activeGroup,
        name='aktive-update'),

    url(r'rol/degisitir/(?P<pk>\d+)$', AdminViews.activeGroup,
        name='sporcu-aktive-group'),



#     arsiv modulü
    url(r'arsiv/arsiv-gorsel/',ArsivView.return_arsiv, name='arsiv-listesi'),
    url(r'arsiv/arsiv-konumEkle/',ArsivView.arsiv_location_add, name='arsiv-konumEkle'),
    url(r'arsiv/arsiv-konumGuncelle/(?P<pk>\d+)$',ArsivView.arsiv_location_update,name='arsiv-konumUpdate'),
    url(r'arsiv/arsiv-BirimEkle/', ArsivView.arsiv_birim_add, name='arsiv-birimEkle'),
    url(r'arsiv/arsiv-BirimGuncelle/(?P<pk>\d+)$',ArsivView.arsiv_birim_update,name='arsiv-birimUpdate'),
    url(r'arsiv/arsiv-Birim/sil/(?P<pk>\d+)$', ArsivView.categoryItemDelete,name='Birim-delete'),
    url(r'arsiv/arsiv-Birim/ParametreEkle/(?P<pk>\d+)$', ArsivView.arsiv_birimParametre, name='Birim-parametreAdd'),
    url(r'arsiv/arsiv-Birim/ParametreGuncelle/(?P<pk>\d+)$', ArsivView.arsiv_birimParametreUpdate, name='Birim-parametreGuncelle'),
    url(r'arsiv/arsiv-Birim/ParametreSil/(?P<pk>\d+)$', ArsivView.parametredelete, name='Birim-parametre-delete'),
    url(r'arsiv/arsiv-Birim/BirimListesi/$', ArsivView.arsiv_birimListesi,name='Birim-listesi'),
    url(r'arsiv/arsiv-Birim/BirimArama/$', ArsivView.birimsearch, name='birim-arama'),
    url(r'arsiv/arsiv-Birim/BirimListesi/parametre/$', ArsivView.parametre, name='parametre-bilgi'),

    #     destek ve talep

    url(r'destek-talep-listesi', ClaimView.return_claim, name='destek-talep-listesi'),
    url(r'destek/Destekekle', ClaimView.claim_add, name='destek-talep-ekle'),
    url(r'destek/sil/(?P<pk>\d+)$', ClaimView.claim_delete, name='destek-delete'),
    url(r'destek/guncelle/(?P<pk>\d+)$', ClaimView.claim_update, name='destek-guncelle'),

    #     Yardım ve destek

    url(r'yardim$', HelpViews.help, name='help'),
]