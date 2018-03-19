from django.conf.urls import url
from efenua import views

urlpatterns = [
    url(r'^admin/add/(?P<app_label>[a-z]+)/(?P<model_name>[a-z]+)/(?P<item_id>\d+)/$',
            views.add_to_favorite),
    url(r'^admin/delete/(?P<app_label>[a-z]+)/(?P<model_name>[a-z]+)/(?P<item_id>\d+)/$',
            views.delete_from_favorite),
]
