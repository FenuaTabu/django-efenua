from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy
import efenua.views as v
from django.contrib.auth.models import User, Group, Permission

class URLGenerator(object):
    """
    Constructs and returns CRUD urls for generic BSCT views for a given model.
    URL names follow the pattern: <lower case model name>_<action>
        - ``lowercasemodelname_detail``: For the DetailView.
        - ``lowercasemodelname_create``: For the CreateView.
        - ``lowercasemodelname_list``:   For the ListView.
        - ``lowercasemodelname_update``: For the UpdateView.
        - ``lowercasemodelname_delete``: For the DeleteView.
    """

    def __init__(self, model, bsct_view_prefix=None):
        """
        Internalize the model and set the view prefix. 
        """
        self.model = model
        self.bsct_view_prefix = bsct_view_prefix or model.__name__.lower()

    def get_create_url(self, view, **kwargs):
        """
        Generate the create URL for the model.
        """
        return url(
            r'%s/create/?$' % self.bsct_view_prefix,
            view.as_view(
                model=self.model,
                success_url=reverse_lazy('%s-list' % self.bsct_view_prefix),
                **kwargs),
            name='%s-create' % self.bsct_view_prefix,
        )

    def get_update_url(self, view, **kwargs):
        """
        Generate the update URL for the model.
        """
        return url(
            r'%s/update/(?P<pk>\d+)/?$' % self.bsct_view_prefix,
            view.as_view(
                model=self.model,
                success_url=reverse_lazy('%s-list' % self.bsct_view_prefix),
                **kwargs),
            name='%s-update' % self.bsct_view_prefix,
        )

    def get_list_url(self, view, **kwargs):
        """
        Generate the list URL for the model.
        """
        return url(
            r'%s/(list/?)?$' % self.bsct_view_prefix,
            view.as_view(model=self.model, **kwargs),
            name='%s-list' % self.bsct_view_prefix,
        )

    def get_delete_url(self, view, **kwargs):
        """
        Generate the delete URL for the model.
        """
        return url(
            r'%s/delete/(?P<pk>\d+)/?$' % self.bsct_view_prefix,
            view.as_view(
                model=self.model,
                success_url=reverse_lazy('%s-list' % self.bsct_view_prefix),
                **kwargs
            ),
            name='%s-delete' % self.bsct_view_prefix,
        )

    def get_detail_url(self, view, **kwargs):
        """
        Generate the detail URL for the model.
        """
        return url(
            r'%s/(?P<pk>\d+)/?$' % self.bsct_view_prefix,
            view.as_view(model=self.model, **kwargs),
            name='%s-detail' % self.bsct_view_prefix,
        )

    def get_urlpatterns(self, view=None, paginate_by=10):
        """
        Generate the entire set URL for the model and return as a patterns
        object.
        """
        self.view = view
        return patterns('',
#             self.get_create_url(),
#             self.get_update_url(),
#             self.get_list_url(),
#             self.get_delete_url(),
#             self.get_detail_url()
        )

from django.conf.urls import include
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/login/'}, name='logout'),
    #Users
    URLGenerator( User ).get_list_url(v.EfenuaUserListView),
    URLGenerator( User ).get_create_url(v.EfenuaUserCreateView),
    URLGenerator( User ).get_detail_url(v.EfenuaUserDetailView),
    URLGenerator( User ).get_update_url(v.EfenuaUserUpdateView),
    #Groupes
    URLGenerator( Group ).get_list_url(v.EfenuaGroupListView),
    URLGenerator( Group ).get_create_url(v.EfenuaGroupCreateView),
    URLGenerator( Group ).get_detail_url(v.EfenuaGroupDetailView),
    URLGenerator( Group ).get_update_url(v.EfenuaGroupUpdateView),
    #permissions
    URLGenerator( Permission ).get_list_url(v.EfenuaPermissionListView),
    URLGenerator( Permission ).get_create_url(v.EfenuaPermissionCreateView),
    URLGenerator( Permission ).get_detail_url(v.EfenuaPermissionDetailView),
    URLGenerator( Permission ).get_update_url(v.EfenuaPermissionUpdateView),
    
    url('^dashboard', v.EfenuaDashboardView.as_view(), name="dashboard")
]