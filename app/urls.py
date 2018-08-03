from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.app_title, name="app_title"),
    url(r'(?P<article_id>\d)/$', views.app_article, name="blog_detail"),
]