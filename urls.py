from django.conf.urls import url, patterns

urlpatterns = [
    url(r'^admin/yuml/$', 'efenua.views.yuml', name='yuml'),
]