from django.urls import re_path
from . import views
urlpatterns = [
    re_path(r'^$', views.index, name='home'),
    re_path(r'^book/(?P<pk>\d+)$', views.book_detail, name='book_detail'),
    re_path(r'^book/new/$', views.new_book, name='new_book'),
    re_path(r'^book/(?P<pk>\d+)/edit/$', views.edit_book, name='edit_book'),
    re_path(r'^book/(?P<pk>\d+)/delete/$',
            views.delete_book, name='delete_book'),
    re_path(r'^book/list/$', views.BookList.as_view(), name='book_list'),
    re_path(r'^accounts/signup/$', views.signup, name='signup'),
    re_path(r'^user/(?P<username>\w+)$', views.profile, name='profile'),
    re_path(r'^user/edit/$', views.settings, name='settings'),
    re_path(r'^search/$', views.search, name='search'),
]
