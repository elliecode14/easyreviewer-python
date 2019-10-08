from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^home$', views.homepage),
    url(r'^logout$', views.logout),
    url(r'^newreviews/(?P<b_id>\d+)$', views.add_more_review),
    url(r'^books/add$', views.add_books_reviews),
    url(r'^books/(?P<b_id>\d+)$', views.view_review),
    url(r'^users/(?P<u_id>\d+)$', views.user_info),
    url(r'^delete/(?P<b_id>\d+)/(?P<r_id>\d+)$', views.delete_reviews),
]
