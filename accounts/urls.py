# import patterns as patterns
from django.urls import path, include
from . import views

app_name = "accounts"

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.login, name='login'),
    path('forgot/', views.forgot, name='view_forgot'),
    path('logout/', views.pagelogout, name='view_logout'),
    path('permission/Add', views.show_urls, name='add_permission'),
    path('error/404/', views.handle400Template, name='404'),
    path('error/500/', views.handle500Template, name='500'),

]
