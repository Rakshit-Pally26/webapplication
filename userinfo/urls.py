from django.conf.urls import url
from . import views
from django.urls import path
urlpatterns = [
    url(r'^$', views.index, name= 'index'),
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^contact/$', views.ContactUs, name='contact'),
    url(r'^contactinfo/', views.ContactInfo, name='contactinfo'),
    url(r'^slackmenu/$', views.SlackMenu, name='slackmenu'),
    url(r'^documents/$', views.document_list, name='document_list'),
    url(r'^documents_upload/$', views.document_upload, name='document_upload'),
    url(r'^add_user/$', views.AddUser, name= 'add_user'),
    url(r'^all_users/$', views.AllUsers, name= 'all_users'),
    path('pdf_view/<int:id>/', views.Generate, name="pdf_generate"),
    path('map_view/', views.default_map, name="default_map"),
    path('drought_monitor/', views.drought_monitor, name="drought_monitor"),
    path('map_view1/', views.default_map1, name="default_map1"),
]