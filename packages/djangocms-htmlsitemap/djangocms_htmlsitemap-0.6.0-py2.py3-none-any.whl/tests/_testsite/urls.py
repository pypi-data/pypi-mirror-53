# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Local application / specific library imports


admin.autodiscover()

urlpatterns = [url(r"admin/", admin.site.urls), url(r"", include("cms.urls"))]

urlpatterns += staticfiles_urlpatterns()
