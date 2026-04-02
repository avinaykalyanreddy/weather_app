from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticSitemap(Sitemap):
    priority = 0.9
    changefreq = "daily"

    def items(self):
        return ['home']   # this must match your URL name

    def location(self, item):
        return reverse(item)
