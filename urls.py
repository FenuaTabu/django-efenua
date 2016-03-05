from django.conf.urls import url, patterns
from efenua import views

urlpatterns = [
    url(r'^admin/yuml/$', views.yuml, name='yuml'),
]