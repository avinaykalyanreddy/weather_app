from django.urls import  path
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticSitemap
from . import views

sitemaps = {
    'static': StaticSitemap(),
}


urlpatterns = [

    path("",views.input_func,name="home"),
    path("sitemap.xml", sitemap, {'sitemaps': sitemaps}),
]