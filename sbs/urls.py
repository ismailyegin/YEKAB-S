from django.conf.urls import url

from sbs.Views import DashboardViews, AthleteViews, RefereeViews, ClubViews, CoachViews, DirectoryViews, UserViews, \
    CompetitionViews, AdminViews, HelpViews, PageViews, PreRegistration, ActivityView, ReferenceView, QuestionViews, \
    LogViews, ProductView, Aktarma, ClaimView, PenalView,ArsivView,EmployeView

app_name = 'sbs'

urlpatterns = [

    # Dashboard
    url(r'anasayfa/admin/$', DashboardViews.return_admin_dashboard, name='admin'),
    url(r'anasayfa/sehir-sporcu-sayisi/$', DashboardViews.City_athlete_cout, name='sehir-sporcu-sayisi'),
    url(r'anasayfa/sporcu/$', DashboardViews.return_athlete_dashboard, name='sporcu'),
    url(r'anasayfa/hakem/$', DashboardViews.return_referee_dashboard, name='hakem'),
    url(r'anasayfa/antrenor/$', DashboardViews.return_coach_dashboard, name='antrenor'),
    url(r'anasayfa/federasyon/$', DashboardViews.return_directory_dashboard, name='federasyon'),
    url(r'anasayfa/kulup-uyesi/$', DashboardViews.return_club_user_dashboard, name='kulup-uyesi'),

    # Sporcular
    url(r'sporcu/sporcu-ekle/$', AthleteViews.return_add_athlete, name='sporcu-ekle'),
    url(r'sporcu/sporcu-birlestir/(?P<pk>\d+)$', AthleteViews.sporcu_sec, name='sporcu-birlestir'),
    url(r'sporcu/sporcu-birlestironay/$', AthleteViews.sporcu_birlestir, name='sporcu-birlestir-onay'),
    url(r'sporcu/sporcu-ekle-antrenor/$', AthleteViews.return_add_athlete_antrenor, name='sporcu-ekle-antrenor'),
    url(r'sporcu/sporcular/$', AthleteViews.return_athletes, name='sporcular'),
    url(r'sporcu/sporcular/antrenor/$', AthleteViews.return_athletes_antrenor, name='sporcular-antrenor'),

    # pagenation deneme
    url(r'page/$', PageViews.deneme, name='deneme'),
    url(r'sporcularajax/$', PageViews.return_athletesdeneme, name='sporculardeneme'),

    url(r'sporcu/sporcuKusakEkle/(?P<pk>\d+)$', AthleteViews.sporcu_kusak_ekle, name='sporcu-kusak-ekle'),
    url(r'sporcu/sporcuKusakDuzenle/(?P<belt_pk>\d+)/(?P<athlete_pk>\d+)$', AthleteViews.sporcu_kusak_duzenle,
        name='sporcu-kusak-duzenle'),
    url(r'sporcu/sporcuLisansEkle/(?P<pk>\d+)$', AthleteViews.sporcu_lisans_ekle, name='sporcu-lisans-ekle'),

    url(r'sporcu/sporcuBelgeEkle/(?P<pk>\d+)$', AthleteViews.sporcu_belge_ekle, name='sporcu-belge-ekle'),
    url(r'sporcu/sporcuCezaEkle/(?P<pk>\d+)$', AthleteViews.sporcu_ceza_ekle, name='sporcu-ceza-ekle'),

    url(r'sporcu/sporcuLisansEkle/antrenor/(?P<pk>\d+)$', AthleteViews.sporcu_lisans_ekle_antrenor,
        name='sporcu-lisans-ekle-antrenor'),
    url(r'sporcu/sporcuLisansDuzenle/(?P<license_pk>\d+)/(?P<athlete_pk>\d+)$', AthleteViews.sporcu_lisans_duzenle,
        name='sporcu-lisans-duzenle'),
    url(r'sporcu/sporcuLisansDuzenle/antrenor/(?P<license_pk>\d+)/(?P<athlete_pk>\d+)$',
        AthleteViews.sporcu_lisans_duzenle_antrenor,
        name='sporcu-lisans-duzenle-antrenor'),
    url(r'sporcu/sporcuLisansDuzenleMobil/(?P<count>\d+)$', AthleteViews.sporcu_lisans_duzenle_mobil,
        name='sporcu-lisans-duzenle-mobil'),
    # ilk degeri verebilmek icin yönlendirme amaci ile kullanildi.
    url(r'sporcu/sporcuLisansDuzenleMobil/$', AthleteViews.sporcu_lisans_duzenle_mobil_ilet,
        name='sporcu-lisans-duzenle-mobil-ilet'),

    url(r'sporcu/sporcuLisansDuzenle/onayla/(?P<license_pk>\d+)/(?P<athlete_pk>\d+)$',
        AthleteViews.sporcu_lisans_onayla, name='sporcu-lisans-onayla'),

    url(r'sporcu/sporcuLisansDuzenle/reddet/(?P<license_pk>\d+)/(?P<athlete_pk>\d+)$',
        AthleteViews.sporcu_lisans_reddet, name='sporcu-lisans-reddet'),
    url(r'sporcu/sporcuLisansDuzenle/lisanssil/(?P<pk>\d+)/(?P<athlete_pk>\d+)$', AthleteViews.sporcu_lisans_sil,
        name='sporcu-lisans-sil'),
    url(r'sporcu/sporcuLisansListesi/onayla/(?P<license_pk>\d+)$',
        AthleteViews.sporcu_lisans_listesi_onayla, name='sporcu-lisans-listesi-onayla'),
    url(r'sporcu/sporcuLisansListesi/onaylaMobil/(?P<license_pk>\d+)/(?P<count>\d+)$',
        AthleteViews.sporcu_lisans_listesi_onayla_mobil, name='sporcu-lisans-listesi-onayla-mobil'),
    # lisans listesinin hepsini onaylama
    url(r'sporcu/sporcuLisansListesi/hepsinionayla/$', AthleteViews.sporcu_lisans_listesi_hepsionay,
        name='sporcu-lisans-hepsini-onayla'),
    # lisanslarin hepsini reddetme
    url(r'sporcu/sporcuLisansListesi/hepsiniReddet/$', AthleteViews.sporcu_lisans_listesi_hepsireddet,
        name='sporcu-lisans-hepsini-reddet'),

    # hepsini beklemeye al
    url(r'sporcu/sporcuLisansListesi/hepsinibekle/$', AthleteViews.sporcu_bekle,
        name='sporcu-lisans-hepsini-bekle'),

    url(r'sporcu/sporcuLisansListesi/reddet/(?P<license_pk>\d+)$',
        AthleteViews.sporcu_lisans_listesi_reddet, name='sporcu-lisans-listesi-reddet'),
    url(r'sporcu/sporcuLisansListesiMobil/reddet/(?P<license_pk>\d+)/(?P<count>\d+)$',
        AthleteViews.sporcu_lisans_listesi_reddet_mobil, name='sporcu-lisans-listesi-reddet-mobil'),
    url(r'sporcu/kusak/$', AthleteViews.return_belt, name='kusak'),
    url(r'sporcu/kusak/sil/(?P<pk>\d+)$', AthleteViews.categoryItemDelete,
        name='categoryItem-delete'),
    url(r'sporcu/kusakDuzenle/(?P<pk>\d+)$', AthleteViews.categoryItemUpdate,
        name='categoryItem-duzenle'),
    url(r'sporcu/sporcuKusakDuzenle/onayla/(?P<belt_pk>\d+)/(?P<athlete_pk>\d+)$',
        AthleteViews.sporcu_kusak_onayla, name='sporcu-kusak-onayla'),
    url(r'sporcu/sporcuKusakReddet/(?P<belt_pk>\d+)/(?P<athlete_pk>\d+)$',
        AthleteViews.sporcu_kusak_reddet, name='sporcu-kusak-reddet'),
    url(r'sporcu/sporcuKusakDuzenle/kusaksil/(?P<pk>\d+)/(?P<athlete_pk>\d+)$', AthleteViews.sporcu_kusak_sil,
        name='sporcu-kusak-sil'),

    # kuşaklarin hepsini beklemeye al
    url(r'sporcu/sporcuKusakbekle',
        AthleteViews.sporcu_kusak_bekle, name='sporcu-kusak-bekle'),
    # kuşak listesinin hepsini onayla
    url(r'sporcu/sporcuKusakListesi/hepsinionayla/$',
        AthleteViews.sporcu_kusak_listesi_hepsinionayla, name='sporcu-kusak-listesi-hepsinionayla'),

    # kuşak hepsini reddet
    url(r'sporcu/sporcuKusakDuzenle/reddet/$',
        AthleteViews.sporcu_kusak_hepsinireddet, name='sporcu-kusak-hepsinireddet'),

    # kusak listesi onay
    url(r'sporcu/sporcuKusakListesi/onayla/(?P<belt_pk>\d+)$',
        AthleteViews.sporcu_kusak_listesi_onayla, name='sporcu-kusak-listesi-onayla'),
    # kuşak listesi reddet
    url(r'sporcu/sporcuKusakListesi/reddet/(?P<belt_pk>\d+)$',
        AthleteViews.sporcu_kusak_listesi_reddet, name='sporcu-kusak-listesi-reddet'),

    url(r'sporcu/sporcuDuzenle/(?P<pk>\d+)$', AthleteViews.updateathletes, name='update-athletes'),
    url(r'sporcu/sporcu-kusak-listesi/$', AthleteViews.sporcu_kusak_listesi, name='kusak-listesi'),
    url(r'sporcu/sporcu-lisans-listesi/$', AthleteViews.sporcu_lisans_listesi, name='lisans-listesi'),
    url(r'sporcu/sporcu-profil-guncelle/$', AthleteViews.updateAthleteProfile,
        name='sporcu-profil-guncelle'),

    url(r'sporcu/sporcuBelgeKaldir/(?P<athlete_pk>\d+)/(?P<document_pk>\d+)$', AthleteViews.athlete_document_delete,
        name='sporcu-belge-kaldir'),
    url(r'sporcu/sporcuCezaKaldir/(?P<athlete_pk>\d+)/(?P<document_pk>\d+)$', AthleteViews.athlete_penal_delete,
        name='sporcu-ceza-kaldir'),

    # Hakemler
    url(r'hakem/hakem-ekle/$', RefereeViews.return_add_referee, name='hakem-ekle'),
    url(r'hakem/hakemler/$', RefereeViews.return_referees, name='hakemler'),
    url(r'hakem/seviye/$', RefereeViews.return_level, name='seviye'),
    url(r'hakem/seviye/sil/(?P<pk>\d+)$', RefereeViews.categoryItemDelete,
        name='categoryItem-delete-seviye'),
    url(r'hakem/seviye/(?P<pk>\d+)$', RefereeViews.categoryItemUpdate,
        name='categoryItem-duzenle-seviye'),
    url(r'hakem/hakemler/sil/(?P<pk>\d+)$', RefereeViews.deleteReferee,
        name='referee-delete'),
    url(r'hakem/hakemler/reddet/basvuru/(?P<pk>\d+)$', RefereeViews.refencedeleteReferee,
        name='referee-reddet-basvuru'),
    url(r'hakem/hakemler/onayla/basvuru/(?P<pk>\d+)$', RefereeViews.refenceapprovalReferee,
        name='referee-onayla-basvuru'),
    url(r'hakem/hakemDuzenle/(?P<pk>\d+)$', RefereeViews.updateReferee,
        name='hakem-duzenle'),
    url(r'hakem/hakemDuzenle-basvuru/(?P<pk>\d+)$', RefereeViews.referenceUpdateReferee,
        name='hakem-duzenle-basvuru'),
    url(r'hakem/hakem-profil-guncelle/$', RefereeViews.updateRefereeProfile,
        name='hakem-profil-guncelle'),
    # /kademe
    url(r'hakem/Hakem-kademe-ekle/(?P<pk>\d+)$', RefereeViews.hakem_kademe_ekle, name='hakem-kademe-ekle'),
    url(r'hakem/Kademe-Duzenle/onayla/(?P<grade_pk>\d+)/(?P<referee_pk>\d+)$', RefereeViews.kademe_onay,
        name='kademe-onayla-hakem'),
    url(r'hakem/Kademe-Duzenle/reddet/(?P<grade_pk>\d+)/(?P<referee_pk>\d+)$', RefereeViews.kademe_reddet,
        name='kademe-reddet-hakem'),
    url(r'hakem/Kademe-Duzenle/guncelle/(?P<grade_pk>\d+)/(?P<referee_pk>\d+)$', RefereeViews.kademe_update,
        name='kademe-guncelle-hakem'),
    url(r'hakem/Kademe-Duzenle/sil/(?P<grade_pk>\d+)/(?P<referee_pk>\d+)$', RefereeViews.kademe_delete,
        name='Kademe-sil-hakem'),
    # /vize
    url(r'hakem/hakem-vize-ekle/(?P<pk>\d+)$', RefereeViews.visa_ekle, name='hakem-vize-ekle'),
    url(r'hakem/Vize-Duzenle/onayla/(?P<grade_pk>\d+)/(?P<referee_pk>\d+)$', RefereeViews.visa_onay,
        name='hakem-vize-onayla'),
    url(r'hakem/Vize-Duzenle/reddet/(?P<grade_pk>\d+)/(?P<referee_pk>\d+)$', RefereeViews.visa_reddet,
        name='hakem-vize-reddet'),
    url(r'hakem/Vize-Duzenle/guncelle/(?P<grade_pk>\d+)/(?P<referee_pk>\d+)$', RefereeViews.vize_update,
        name='hakem-vize-guncelle'),
    url(r'hakem/Vize-Duzenle/sil/(?P<grade_pk>\d+)/(?P<referee_pk>\d+)$', RefereeViews.vize_delete,
        name='hakem-vize-sil'),
    url(r'hakem/hakemBelgeEkle/(?P<pk>\d+)$', RefereeViews.hakem_belge_ekle, name='hakem-belge-ekle'),
    url(r'hakem/hakemBelgeKaldir/(?P<athlete_pk>\d+)/(?P<document_pk>\d+)$', RefereeViews.judje_document_delete,
        name='hakem-belge-kaldir'),
    url(r'hakem/hakemCezaEkle/(?P<pk>\d+)$', RefereeViews.judge_ceza_ekle, name='hakem-ceza-ekle'),

    # Kulüpler
    url(r'kulup/basvuru-listesi/$', PreRegistration.return_preRegistration, name='basvuru-listesi'),
    url(r'kulup/basvuru/onayla/(?P<pk>\d+)$', PreRegistration.approve_preRegistration, name='basvuru-onayla'),
    url(r'kulup/basvuru/reddet/(?P<pk>\d+)$', PreRegistration.rejected_preRegistration, name='basvuru-reddet'),
    url(r'klup/basvuru-incele/(?P<pk>\d+)$', PreRegistration.update_preRegistration, name='update-basvuru'),

    url(r'kulup/kulup-ekle/$', ClubViews.return_add_club, name='kulup-ekle'),
    url(r'kulup/kulupler/$', ClubViews.return_clubs, name='kulupler'),
    url(r'kulup/kulup-uyesi-ekle/$', ClubViews.return_add_club_person, name='kulup-uyesi-ekle'),
    url(r'kulup/kulup-uyesi-guncelle/(?P<pk>\d+)$', ClubViews.updateClubPersons, name='kulup-uyesi-guncelle'),
    url(r'kulup/kulup-uyeleri/$', ClubViews.return_club_person, name='kulup-uyeleri'),

    url(r'kulup/kulup-raporu/$', ClubViews.return_rapor_club, name='kulup-rapor'),
    url(r'kulup/kulup-raporu/ajax$', ClubViews.return_clup, name='kulup-rapor-ajax'),

    url(r'kulup/kulup-antrenor/$', ClubViews.return_club_coach, name='kulup-antrenor'),

    url(r'kulup/kulup-uye-rolu/$', ClubViews.return_club_role, name='kulup-uye-rolu'),
    url(r'kulup/kulup-uye-rolu/sil/(?P<pk>\d+)$', ClubViews.deleteClubRole,
        name='ClubRole-delete'),
    url(r'kulup/kulup-uyeleri/sil/(?P<pk>\d+)$', ClubViews.deleteClubUser,
        name='ClubUser-delete'),

    url(r'kulup/kulup-uyeleri/cikar/(?P<pk>\d+)/(?P<club_pk>\d+)/$', ClubViews.deleteClubUserFromClub,
        name='ClubUser-cikar'),
    url(r'kulup/kulup-antrenorleri/cikar/(?P<pk>\d+)/(?P<club_pk>\d+)/$', ClubViews.deleteCoachFromClub,
        name='ClubCoach-cikar'),

    url(r'kulup/kulupRolDuzenle/(?P<pk>\d+)$', ClubViews.updateClubRole,
        name='updateClubRole'),
    url(r'kulup/kulupler/sil/(?P<pk>\d+)$', ClubViews.clubDelete,
        name='delete-club'),
    url(r'kulup/kulupDuzenle/(?P<pk>\d+)$', ClubViews.clubUpdate,
        name='update-club'),
    url(r'kulup/kusak-sinavlari/$', ClubViews.return_belt_exams, name='kusak-sinavlari'),
    url(r'kulup/kusak-sinavi-sporcu-sec/(?P<pk>\d+)$', ClubViews.choose_athlete, name='kusak-sinavi-sporcu-sec'),
    #

    url(r'kulup/kusak-sinavi-ekle/$', ClubViews.add_belt_exam, name='kusak-sinavi-ekle'),
    url(r'kulup/kusak-sinavi-antroner-sec/(?P<pk>\d+)$', ClubViews.choose_coach, name='kusak-sinavi-antroner-sec'),

    url(r'kulup/kusak-sinavi-antroner-sil/(?P<pk>\d+)/(?P<exam_pk>\d+)$', ClubViews.choose_coach_remove,
        name='kulup-sinavi-antroner-sil'),
    url(r'kulup/kusak-sinavi-sporcu-sil/(?P<pk>\d+)/(?P<exam_pk>\d+)$', ClubViews.choose_athlete_remove,
        name='kulup-sinavi-sporcu-sil'),

    url(r'kulup/kusak-sinavi-ekle/(?P<athlete1>\S+?)$', ClubViews.add_belt_exam, name='kusak-sinavi-ekle'),
    url(r'kulup/kusak-sinavi-duzenle/(?P<pk>\d+)$', ClubViews.update_belt_exam, name='kusak-sinavi-duzenle'),
    url(r'kulup/kusak-sinavlari/sil/(?P<pk>\d+)$', ClubViews.delete_belt_exam, name='kusak-sinavi-sil'),
    url(r'kulup/kusak-sinavlari/incele/(?P<pk>\d+)$', ClubViews.detail_belt_exam, name='kusak-sinavi-incele'),
    url(r'kulup/kusak-sinavlari/onayla/(?P<pk>\d+)$', ClubViews.approve_belt_exam, name='kusak-sinavi-onayla'),
    url(r'kulup/kusak-sinavlari/reddet/(?P<pk>\d+)$', ClubViews.denied_belt_exam, name='kusak-sinavi-reddet'),

    url(r'kulup/kulup-uyesi-profil-guncelle/$', ClubViews.updateClubPersonsProfile,
        name='kulup-uyesi-profil-guncelle'),

    url(r'kulup/kulup-uyesi-sec/(?P<pk>\d+)$', ClubViews.choose_sport_club_user,
        name='choose-sport-club-user'),
    url(r'kulup/klupuyesi-listesi-sec/(?P<pk>\d+)$', ClubViews.choose_sport_club_user,
        name='choose-sport-club-user'),

    # Antrenörler
    url(r'antrenor/antrenor-ekle/$', CoachViews.return_add_coach, name='antrenor-ekle'),
    url(r'antrenor/antrenorler/$', CoachViews.return_coachs, name='antrenorler'),
    url(r'antrenor/kademe/$', CoachViews.return_grade, name='kademe'),
    url(r'antrenor/kademe/sil/(?P<pk>\d+)$', CoachViews.categoryItemDelete,
        name='categoryItem-delete-kademe'),
    url(r'antrenor/kademeDuzenle/(?P<pk>\d+)$', CoachViews.categoryItemUpdate,
        name='categoryItem-duzenle-kademe'),
    url(r'antrenor/antrenorler/sil/(?P<pk>\d+)$', CoachViews.deleteCoach,
        name='delete-coach'),
    url(r'antrenor/antrenorler/reddet/basvuru/(?P<pk>\d+)$', CoachViews.referencedeniedCoach,
        name='coach-basvuru-reddet'),
    url(r'antrenor/antrenorler/onayla/basvuru/(?P<pk>\d+)$', CoachViews.referenappcoverCoach,
        name='onayla-coach-basvuru'),
    url(r'antrenor/basvuru/onayla/(?P<pk>\d+)$', CoachViews.referenceCoachStatus, name='basvuru-onayla-coach'),

    url(r'antrenor/antrenorDuzenle/(?P<pk>\d+)$', CoachViews.coachUpdate,
        name='update-coach'),
    url(r'antrenor/antrenorDuzenle-Kayit/(?P<pk>\d+)$', CoachViews.coachreferenceUpdate,
        name='update-coach-reference'),
    url(r'antrenor/antrenorSec/(?P<pk>\d+)$', ClubViews.choose_coach,
        name='choose-coach'),
    url(r'antrenor/antrenorSec/klup/(?P<pk>\d+)$', ClubViews.choose_coach_clup,
        name='choose-coach-clup'),

    url(r'antrenor/antrenor-profil-guncelle/$', CoachViews.updateCoachProfile,
        name='antrenor-profil-guncelle'),
    url(r'antrenor/antrenor-kademe-ekle/(?P<pk>\d+)$', CoachViews.antrenor_kademe_ekle, name='antrenor-kademe-ekle'),
    #     # vize ekle
    url(r'antrenor/antrenor-vize-ekle/(?P<pk>\d+)$', CoachViews.antrenor_vısa_ekle, name='antrenor-vize-ekle'),

    # Kademe onay reddet sil güncelle liste
    url(r'antrenor/vize-Liste-Reddet/(?P<grade_pk>\d+)$', CoachViews.vize_reddet_liste,
        name='vize-list-reddet'),
    url(r'antrenor/vize-Liste-Onayla/(?P<grade_pk>\d+)$', CoachViews.vize_onayla_liste,
        name='vize-list-onay'),
    url(r'antrenor/Vize-Duzenle/sil/(?P<grade_pk>\d+)/(?P<coach_pk>\d+)$', CoachViews.vize_delete,
        name='vize-sil'),
    url(r'antrenor/Vize-Reddet/(?P<grade_pk>\d+)/(?P<coach_pk>\d+)$', CoachViews.vize_reddet, name='vize-reddet'),
    url(r'antrenor/Vize-Duzenle/onayla/(?P<grade_pk>\d+)/(?P<coach_pk>\d+)$', CoachViews.visa_onay, name='vize-onayla'),
    url(r'antrenor/Kademe-Duzenle/onayla/(?P<grade_pk>\d+)/(?P<coach_pk>\d+)$', CoachViews.kademe_onay,
        name='kademe-onayla'),
    url(r'antrenor/Kademe-Reddet/(?P<grade_pk>\d+)/(?P<coach_pk>\d+)$', CoachViews.kademe_reddet, name='kademe-reddet'),
    url(r'antrenor/Kademe-Duzenle/guncelle/(?P<grade_pk>\d+)/(?P<coach_pk>\d+)$', CoachViews.kademe_update,
        name='kademe-guncelle'),
    url(r'antrenor/Vize-Duzenle/guncelle/(?P<grade_pk>\d+)/(?P<coach_pk>\d+)$', CoachViews.vize_update,
        name='vize-guncelle'),
    url(r'antrenor/Kademe-Duzenle/sil/(?P<grade_pk>\d+)/(?P<coach_pk>\d+)$', CoachViews.kademe_delete,
        name='Kademe-sil'),
    url(r'antrenor/Kademe-listesi/', CoachViews.kademe_list, name='kademe-listesi'),
    url(r'antrenor/Vize-listesi/', CoachViews.vize_list, name='vize-listesi'),
    url(r'antrenor/kademe-Liste-Onayla/(?P<grade_pk>\d+)$', CoachViews.kademe_onayla,
        name='kademe-list-onay'),
    url(r'antrenor/kademe-Liste-reddet/(?P<grade_pk>\d+)$', CoachViews.kademe_reddet_liste,
        name='kademe-list-reddet'),
    url(r'antrenor/kademe-Liste-reddet-hepsi$', CoachViews.kademe_reddet_hepsi,
        name='kademe-list-reddet-hepsi'),
    url(r'antrenor/kademe-Liste-onay-hepsi$', CoachViews.kademe_onay_hepsi,
        name='kademe-list-onay-hepsi'),
    url(r'antrenor/kademe-Liste-bekle-hepsi$', CoachViews.kademe_bekle_hepsi, name='kademe-list-bekle-hepsi'),

    # visa seminar
    # Antrenör
    url(r'antrenor/visa-Seminar$', CoachViews.return_visaSeminar, name='visa-seminar'),
    url(r'antrenor/visa-Seminar/basvuruListesi$', CoachViews.return_visaSeminar_Basvuru, name='visa-seminar-basvuru'),
    url(r'antrenor/visa-Seminar-ekle/$', CoachViews.visaSeminar_ekle, name='visa-seminar-ekle'),
    url(r'antrenor/visa-Seminar-duzenle/(?P<pk>\d+)$', CoachViews.visaSeminar_duzenle, name='seminar-duzenle'),
    url(r'antrenor/visa-Seminar-Onayla/(?P<pk>\d+)$', CoachViews.visaSeminar_onayla, name='seminar-onayla'),
    url(r'antrenor/visa-Seminar/Seminer-sil(?P<pk>\d+)$', CoachViews.visaSeminar_sil, name='seminar-sil'),
    url(r'antrenor/visa-Seminar/antroner-sec/(?P<pk>\d+)$', CoachViews.choose_coach, name='vize-semineri-antroner-sec'),
    url(r'antrenor/visa-Seminar/antroner-sil/(?P<pk>\d+)/(?P<competition>\d+)$', CoachViews.visaSeminar_Delete_Coach,
        name='visaSeminar-antrenör-sil'),

    url(r'antrenor/visa-Seminar/antroner-basvuru-onayla/(?P<pk>\d+)/(?P<competition>\d+)$',
        CoachViews.visaSeminar_Onayla_Coach_application,
        name='visaSeminar-antrenorbasvuru-onayla'),
    url(r'antrenor/visa-Seminar/antroner-basvuru-reddet/(?P<pk>\d+)/(?P<competition>\d+)$',
        CoachViews.visaSeminar_Delete_Coach_application,
        name='visaSeminar-antrenorbasvuru-reddet'),

    url(r'antrenor/antrenorCezaEkle/(?P<pk>\d+)$', CoachViews.coach_penal_add, name='antrenor-ceza-ekle'),
    url(r'antrenor/antrenorCezaKaldır/(?P<athlete_pk>\d+)/(?P<document_pk>\d+)$', CoachViews.coach_penal_delete,
        name='antrenor-ceza-kaldir'),
    url(r'antrenor/antrenorBelgeEkle/(?P<pk>\d+)$', CoachViews.antrenor_belge_ekle, name='antrenor-belge-ekle'),
    url(r'antrenor/antrenorBelgeKaldır/(?P<athlete_pk>\d+)/(?P<document_pk>\d+)$', CoachViews.coach_document_delete,
        name='antrenor-belge-kaldir'),

    # Hakem
    url(r'hakem/visa-Seminar$', RefereeViews.return_visaSeminar, name='hakem-visa-seminar'),
    url(r'hakem/visa-Seminar-ekle$', RefereeViews.visaSeminar_ekle, name='hakem-visa-seminar-ekle'),
    url(r'hakem/visa-Seminar-duzenle/(?P<pk>\d+)$', RefereeViews.visaSeminar_duzenle, name='hakem-seminar-duzenle'),
    url(r'hakem/visa-Seminar/Seminer-sil(?P<pk>\d+)$', RefereeViews.visaSeminar_sil, name='hakem-seminar-sil'),
    url(r'hakem/visa-Seminar/hakem-sec/(?P<pk>\d+)$', RefereeViews.choose_referee, name='vize-semineri-hakem-sec'),
    url(r'hakem/visa-Seminar/hakem-sil/(?P<pk>\d+)/(?P<competition>\d+)$', RefereeViews.visaSeminar_Delete_Referee,
        name='visaSeminar-hakem-sil'),
    url(r'hakem/visa-Seminar-Onayla/(?P<pk>\d+)$', RefereeViews.visaSeminar_onayla, name='hakem-seminar-onayla'),
    url(r'hakem/basvuru/onayla/(?P<pk>\d+)$', RefereeViews.referenceStatus, name='reference-refere-status'),
    url(r'hakem/basvuru/reddet/(?P<pk>\d+)$', RefereeViews.referenceStatus_reddet,
        name='reference-refere-status-reddet'),

    # Hakem
    url(r'hakem/visa-Seminar/Basvuru$', RefereeViews.return_visaSeminar_application, name='hakem-seminar-basvuru'),
    url(r'hakem/visa-Seminar/basvuruListesi$', RefereeViews.return_visaSeminar_Basvuru, name='hakem-visa-seminar-basvuru'),

    url(r'hakem/Kademe-listesi/', RefereeViews.kademe_list, name='hakem-kademe-listesi'),
    url(r'hakem/kademe-Liste-Onayla/(?P<referee_pk>\d+)$', RefereeViews.kademe_onayla,
        name='hakem-kademe-list-onay'),
    url(r'hakem/kademe-Liste-reddet/(?P<referee_pk>\d+)$', RefereeViews.kademe_reddet_liste,
        name='hakem-kademe-list-reddet'),
    url(r'hakem/vize-Liste-Reddet/(?P<referee_pk>\d+)$', RefereeViews.vize_reddet_liste,
        name='hakem-vize-list-reddet'),

    url(r'hakem/kademe-Liste-onay-hepsi$', RefereeViews.kademe_onay_hepsi,
        name='hakem-kademe-list-onay-hepsi'),
    url(r'hakem/kademe-Liste-reddet-hepsi$', RefereeViews.kademe_reddet_hepsi,
        name='hakem-kademe-list-reddet-hepsi'),
    url(r'hakem/Vize-listesi/', RefereeViews.vize_list, name='hakem-vize-listesi'),
    url(r'hakem/vize-Liste-Onayla/(?P<referee_pk>\d+)$', RefereeViews.vize_onayla_liste,
        name='hakem-vize-list-onay'),
    url(r'hakem/hakemCezaKaldır/(?P<athlete_pk>\d+)/(?P<document_pk>\d+)$', RefereeViews.judge_penal_delete,
        name='hakem-ceza-kaldir'),

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

    # Admin
    url(r'admin/admin-profil-guncelle/$', AdminViews.updateProfile,
        name='admin-profil-guncelle'),

    # Kullanıcılar
    url(r'kullanici/kullanicilar/$', UserViews.return_users, name='kullanicilar'),
    url(r'kullanici/kullanici-duzenle/(?P<pk>\d+)$', UserViews.update_user, name='kullanici-duzenle'),
    url(r'kullanici/kullanicilar/aktifet/(?P<pk>\d+)$', UserViews.active_user,
        name='kullanici-aktifet'),
    url(r'kullanici/kullanicilar/kullanici-bilgi-gonder/(?P<pk>\d+)$', UserViews.send_information,
        name='kullanici-bilgi-gonder'),
    # Activity
    url(r'faliyet/faaliyetler/$', ActivityView.return_activity, name='faaliyet'),
    url(r'faliyet/faaliyet-ekle/$', ActivityView.faliyet_ekle, name='faaliyet-ekle'),
    url(r'faliyet/faaliyet-sil(?P<pk>\d+)$', ActivityView.faaliyet_sil, name='faliyet-sil'),
    url(r'faliyet/faaliyet-duzenle/(?P<pk>\d+)$', ActivityView.faliyet_duzenle, name='faliyet-duzenle'),

    # Test
    url(r'sonuclar$', CompetitionViews.return_competition, name='sonuclar'),
    url(r'sonuc/sonuc-liste/(?P<pk>\d+)$', CompetitionViews.result_list, name='sonuc-liste'),
    url(r'sonuc/year', CompetitionViews.return_competition_ajax, name='sonuclar-ajax'),
    url(r'musabaka/basvuru/(?P<pk>\d+)$', CompetitionViews.aplication, name='basvuru'),

    # Competition

    url(r'musabaka/musabakalar/$', CompetitionViews.return_competitions, name='musabakalar'),
    url(r'musabaka/musabaka-ekle/$', CompetitionViews.musabaka_ekle, name='musabaka-ekle'),
    url(r'musabaka/musabaka-duzenle/(?P<pk>\d+)$', CompetitionViews.musabaka_duzenle, name='musabaka-duzenle'),
    url(r'musabaka/musabakalar/musabaka-sil(?P<pk>\d+)$', CompetitionViews.musabaka_sil, name='musabaka-sil'),
    url(r'musabaka/musabaka-sporcu-sec/(?P<pk>\d+)$', CompetitionViews.musabaka_sporcu_sec, name='musabaka-sporcu-sec'),
    url(r'musabaka/sporcu-sec/(?P<pk>\d+)/(?P<competition>\d+)$', CompetitionViews.choose_athlete,
        name='catagori-sporcu-sec-ajax'),
    url(r'musabaka/antrenorler-sec/$', CompetitionViews.antrenor_ajax,name='catagori-antrenor-sec-ajax'),
    url(r'musabaka/antrenorler-sporcu-sec/$', CompetitionViews.antrenor_sporcu_ajax, name='catagori-antrenor-sporcu-sec-ajax'),

    url(r'musabaka/sporcu-sec/update(?P<pk>\d+)/(?P<competition>\d+)$', CompetitionViews.choose_athlete_update,
        name='catagori-sporcu-update-ajax'),

    url(r'musabaka/sporcu-guncelle/(?P<pk>\d+)/(?P<competition>\d+)$', CompetitionViews.update_athlete,
        name='catagori-sporcu-guncelle-ajax'),
    url(r'musabaka/KategorilerinSporculari/$', CompetitionViews.return_sporcu, name='Kategorilerin-Sporculari'),

    url(r'musabaka/Sporcu-sec/ajax/$', CompetitionViews.return_sporcu_ajax, name='Sporcu-sec-ajax'),
    url(r'musabaka/musabaka-duzenle/musabaka_sporcu_ekle/(?P<athlete_pk>\d+)/(?P<competition_pk>\d+)$',
        CompetitionViews.musabaka_sporcu_ekle,
        name='musabaka_sporcu_ekle'),
    url(r'musabaka/musabaka-duzenle/kaldir/(?P<pk>\d+)/$', CompetitionViews.musabaka_sporcu_sil,
        name='musabaka-sporcu-kaldir'),
    url(r'musabaka/KategoriEkle/$', CompetitionViews.categori_ekle, name='kategori-ekle'),
    url(r'musabaka/sonucal/(?P<pk>\d+)$', CompetitionViews.upload, name='competition-result'),
    url(r'musabaka/musabaka-sonucEkle/$', CompetitionViews.musabakaResultAdd, name='musabaka-SonucEkle'),
    url(r'musabaka/musabaka-sonucEkle-ajax/$',CompetitionViews.choose_athlete_competition, name='musabaka-sonuc-ajax'),
    #     Yardım ve destek

    url(r'yardim$', HelpViews.help, name='help'),

    #     basvurular
    url(r'reference/referee/basvuru$', ReferenceView.hakemler, name='basvuru-referee'),
    url(r'reference/coach/basvuru$', ReferenceView.antroner, name='basvuru-coach'),
    url(r'reference/athlete/basvuru$', ReferenceView.sporcular, name='basvuru-athlete'),

    #     sık sorulan sorular
    url(r'sorular', QuestionViews.soru_goster, name='sorular'),

    url(r'soru/ekle', QuestionViews.soru_ekle, name='soru-ekle'),
    url(r'soru/sil/(?P<pk>\d+)$', QuestionViews.categoryItemDelete,
        name='soru-delete'),
    url(r'soru/guncelle/(?P<pk>\d+)$', QuestionViews.soru_update,
        name='soru-guncelle'),

    #   logkayıtlari

    url(r'log/log-kayitlari/$', LogViews.return_log,
        name='logs'),

    url(r'message/messages/$', DashboardViews.return_message,
        name='message'),

    url(r'rol/guncelle/(?P<pk>\d+)$', DashboardViews.activeGroup,
        name='aktive-update'),

    url(r'rol/degisitir/(?P<pk>\d+)$', AdminViews.activeGroup,
        name='sporcu-aktive-group'),

    #     destek ve talep

    url(r'destek-talep-listesi', ClaimView.return_claim, name='destek-talep-listesi'),
    url(r'destek/Destekekle', ClaimView.claim_add, name='destek-talep-ekle'),
    url(r'destek/sil/(?P<pk>\d+)$', ClaimView.claim_delete, name='destek-delete'),
    url(r'destek/guncelle/(?P<pk>\d+)$', ClaimView.claim_update, name='destek-guncelle'),

    url(r'menu', ClaimView.menu, name='destek-talep-menu'),

    #     products
    url(r'urun/ekle', ProductView.add_product, name='urun-ekle'),
    url(r'urun/urunler', ProductView.return_products, name='urunler'),
    url(r'urun/urun-sil(?P<pk>\d+)$', ProductView.product_delete, name='urun-sil'),
    url(r'urun/urun-duzenle/(?P<pk>\d+)$', ProductView.product_update, name='urun-duzenle'),

    #     products deposit
    url(r'emanet/ekle-emanet', ProductView.add_product_deposit, name='urun-ekle-emanet'),
    url(r'emanet/urunler-emanet', ProductView.return_products_deposit, name='urunler-emanet'),
    url(r'emanet/urun-sil-emanet/(?P<pk>\d+)$', ProductView.product_delete_deposit, name='urun-sil-emanet'),
    url(r'emanet/urun-duzenle-emanet/(?P<pk>\d+)$', ProductView.product_update_deposit, name='urun-duzenle-emanet'),

    # aktarma
    url(r'aktarma/kulup-aktar', Aktarma.kulup_aktar, name='kulup-aktar'),
    url(r'aktarma/hakem-aktar', Aktarma.hakem_aktar, name='hakem-aktar'),
    url(r'aktarma/antrenor-aktar', Aktarma.antrenor_aktar, name='antrenor-aktar'),
    url(r'aktarma/sporcu-aktar', Aktarma.sporcu_aktar, name='sporcu-aktar'),
    url(r'aktarma/lisans-aktar', Aktarma.lisans_aktar, name='lisans-aktar'),
    url(r'control', Aktarma.control, name='control-aktar'),
    url(r'aktarma/antrenor-kademe-aktar', Aktarma.kademe_aktar, name='kademe-aktar-antrenor'),
    url(r'aktarma/user-aktar', Aktarma.username_aktar, name='user-aktar'),
    url(r'aktarma/musabaka-aktar', Aktarma.musabaka_aktar, name='musabaka-aktar'),
    url(r'aktarma/musabaka-sporcu-aktar', Aktarma.musabaka_sporcu_aktar, name='musabaka-aktar-sporcu'),
    url(r'aktarma/musabaka-antrenor-aktar', Aktarma.musabaka_antrenor_aktar, name='musabaka-aktar-antrenor'),
    url(r'aktarma/musabaka-hakem-aktar', Aktarma.musabaka_hakem_aktar, name='musabaka-aktar-hakem'),
    url(r'aktarma/musabaka-kategori-aktar', Aktarma.musabaka_kademe_aktar, name='musabaka-aktar-kategori'),
    url(r'control2', Aktarma.control2, name='control-aktar2'),
    url(r'aktarma/malzeme-aktar', Aktarma.mazeme_aktar, name='malzeme-aktar'),
    url(r'aktarma/iletisim-aktar', Aktarma.comminacations_aktar, name='iletisim-aktar'),
    url(r'aktarma/sporcu', Aktarma.SporcuControl, name='control-aktar-sporcu'),
    url(r'aktarma/antrenor', Aktarma.AntenorControl, name='control-aktar-antrenor'),
    url(r'aktarma/TcnoControl', Aktarma.TcnoControl, name='control-aktar-TcnoControl'),
    url(r'aktarma/kanspor', Aktarma.KangrubuSporcu, name='control-kan'),
    url(r'aktarma/kanantrenor', Aktarma.KangrubuAntrenor, name='control-kan-antrenor'),
    url(r'aktarma/kanhakem', Aktarma.KangrubuHakem, name='control-kan-hakem'),
    url(r'aktarma/emanet', Aktarma.Emanet, name='control-emanet'),
    url(r'aktarma/com', Aktarma.communicationAktar, name='control-aktarmatest'),
    url(r'aktarma/hakem', Aktarma.judgeAktar, name='control-aktarhakemvize'),

    #     ceza görüntüleme modulleri
    url(r'ceza/ceza-listesi/', PenalView.return_penal_athlete, name='ceza-listesi'),


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


    url(r'arsiv/Arama/$', ArsivView.birimSearch, name='arama'),
    url(r'arsiv/GenelArama/$', ArsivView.birimGeneralSearch, name='genel-arama'),

    url(r'arsiv/arsiv-Klasor/klasorler/$', ArsivView.arsiv_klasorler, name='klasor-listesi'),
    url(r'arsiv/arsiv-Klasor/klasorEkle/$', ArsivView.arsiv_klasorEkle, name='klasor-ekle'),
    url(r'arsiv/arsiv-klasor/sil/(?P<pk>\d+)$', ArsivView.arsiv_klasor_delete, name='klasor-delete'),
    url(r'arsiv/arsiv-Dosya/DosyaListesi/$', ArsivView.arsiv_dosyalar, name='dosya-listesi'),
    url(r'arsiv/arsiv-Klasor/klasorGuncelle/(?P<pk>\d+)$', ArsivView.arsiv_klasorUpdate,
        name='klasor-guncelle'),

    url(r'arsiv/arsiv-Dosya/dosyaEkle/(?P<pk>\d+)$', ArsivView.arsiv_dosyaEkle, name='dosya-ekle'),
    url(r'arsiv/arsiv-Dosya/dosyaGuncelle/(?P<pk>\d+)$', ArsivView.arsiv_dosyaUpdate,
        name='dosya-guncelle'),
    url(r'arsiv/arsiv-dosya/sil/(?P<pk>\d+)$', ArsivView.arsiv_dosya_delete, name='dosya-delete'),

    url(r'arsiv/arsiv-evrak/evrakEkle/(?P<pk>\d+)$', ArsivView.arsiv_evrakEkle, name='evrak-ekle'),
    url(r'arsiv/arsiv-evrak/evrakSil/(?P<pk>\d+)$', ArsivView.arsiv_evrakDelete, name='evrak-sil'),
    url(r'arsiv/arsiv-evrak/evrakSil/ajax/(?P<pk>\d+)$', ArsivView.arsiv_evrakDelete_ajax, name='evrak-sil-ajax'),

    url(r'arsiv/arsiv-anasayfa/$', ArsivView.arsiv_anasayfa, name='evrak-anasayfa'),
    # evrak
    url(r'arsiv/indir/(?P<pk>\d+)$', ArsivView.zipfile, name='dosya-zip'),
    url(r'arsiv/arsiv-evrakEkle/$', ArsivView.arsiv_dosyaEkle_full, name='evrak-ekle-ajax'),
    url(r'arsiv/klasor$', ArsivView.ajax_klasor, name='birim-klasor-ajax'),
    url(r'arsiv/dosya$', ArsivView.ajax_dosya, name='birim-dosya-ajax'),
    url(r'arsiv/dosyaform/ajax$', ArsivView.ajax_dosyaform, name='dosyaform-ajax'),
    url(r'arsiv/dosyaform/ajax/update$', ArsivView.ajax_dosyaform_update, name='dosyaform-ajax-update'),
    url(r'arsiv/arsiv-birimEkle/ajax/$', ArsivView.ajax_birimAdd, name='evrak-birim-ajax'),
    url(r'arsiv/arsiv-birimguncelle/ajax/$', ArsivView.ajax_birimUpdate, name='evrak-birim-ajax-update'),
    url(r'arsiv/arsiv-birimguncelle/ajax/parametreEkle$', ArsivView.ajax_birimUpdateParametreAdd, name='evrak-birim-ajax-update-parametreAdd'),
    url(r'arsiv/arsiv-birimguncelle/ajax/parametre$', ArsivView.ajax_birimUpdateParametre, name='evrak-birim-ajax-update-parametre'),

    url(r'arsiv/arsiv-klasorEkle/ajax/$', ArsivView.ajax_klasorAdd, name='evrak-klasor-ajax'),
    url(r'arsiv/arsiv-klasorguncelle/ajax/search$', ArsivView.ajax_klasor_update, name='evrak-klasor-ajax-update'),
    url(r'arsiv/arsiv-klasorguncelle/ajax/$', ArsivView.ajax_klasor_update_add, name='evrak-klasor-ajax-update-add'),
# personeller
    url(r'personel/birim-uyeleri/$', EmployeView.return_employes, name='birim-personelleri'),
    url(r'personel/birim-uyesi-ekle/$', EmployeView.add_employe, name='birim-personel-ekle'),
    url(r'personel/birim-uyesi-duzenle/(?P<pk>\d+)$', EmployeView.update_demploye,name='birim-personel-duzenle'),
    url(r'personel/birim-uyeleri/sil/(?P<pk>\d+)$', EmployeView.delete_directory_member,name='personel-sil'),


]
