from django.conf.urls import url

from .views import AngelView

urlpatterns = [
    url(r'^search/$', AngelView.as_view(), name='search'),
]
