from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.shortcuts import redirect
from django.conf import settings
from django_tables2 import RequestConfig
from efenua.utils import EfenuaMenuItemLink, EfenuaMenuItemBreadcrumbs
import django_filters
from django.contrib.auth.models import User, Group, Permission
from efenua.forms import EfenuaUserForm, EfenuaGroupForm, EfenuaPermissionForm
from efenua.tables import EfenuaTable, EfenuaUserTable, EfenuaGroupTable, EfenuaPermissionTable
  
class EfenuaDashboardView(TemplateView):
    template_name = 'efenua/dashboard.html'
    
    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)
        
class EfenuaCreateView(SuccessMessageMixin, CreateView):
    template_name = 'efenua/createview.html'
    success_message = "%(msg)s a ete creer avec succes"
    action_static = None
    breadcrumbs = None
    formset_class = None

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            msg=self.object,
        )
        
    def get_context_data(self, **kwargs):
        context = super(EfenuaCreateView, self).get_context_data(**kwargs)
        if self.action_static is not None: context['action_static'] = self.action_static
        context['breadcrumbs'] = self.breadcrumbs
        if self.formset_class is not None:
            if self.request.POST:
                context['formset'] = self.formset_class(self.request.POST)
            else:
                context['formset'] = self.formset_class()
        return context
            
class EfenuaUpdateView(SuccessMessageMixin, UpdateView):
    template_name = 'efenua/updateview.html'
    success_message = "%(msg)s a ete mise a jour avec succes"
    action_static = None
    breadcrumbs = None
    formset_class = None

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            msg=self.object,
        )
    
    def get_context_data(self, **kwargs):
        context = super(EfenuaUpdateView, self).get_context_data(**kwargs)
        if self.action_static is not None: context['action_static'] = self.action_static
        context['breadcrumbs'] = self.breadcrumbs
        if self.formset_class is not None:
            if self.request.POST:
                context['formset'] = self.formset_class(self.request.POST)
            else:
                context['formset'] = self.formset_class()
        return context
        
class EfenuaDeleteView(DeleteView):
    template_name = 'efenua/deleteview.html'

class EfenuaDetailView(DetailView):
    template_name = 'efenua/detailview.html'
    fields = None
    action_static = None
    breadcrumbs = None
     
    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        if self.action_static is not None: context['action_static'] = self.action_static
        context['fields'] = self.fields
        context['breadcrumbs'] = self.breadcrumbs
        return context
        
class EfenuaListView(TemplateView):
    template_name = 'efenua/listview.html'
    table_header = None
    table_class = None
    filter_class = None
    action_static = None
    action_many = None
    action_one = None
    model = None
    breadcrumbs = None
    
    def post(self, request, *args, **kwargs):
        self.selectable = self.request.POST.getlist("selectable", None)
        get_action = self.request.POST.get("action", None)
        if get_action is not None:
            if get_action in vars(self.__class__) or get_action in vars(EfenuaListView):
                f = getattr(self, get_action)
                f(self.queryset.filter(pk__in=self.selectable))
        return self.get(request, *args, **kwargs)

    def context(self):
        data = {}
        data['url_full_path'] = self.request.get_full_path()
        if self.table_header is None : data['table_header'] = self.model._meta.verbose_name_plural.title()
        else : data['table_header'] = self.table_header
        self.filter = self.filter_class(self.request.GET, queryset=self.queryset)
        data['filter'] = self.filter
        data['table'] = self.table_class(self.filter.qs)
        RequestConfig(self.request, paginate=False).configure(data['table'])
        data['queryset'] = self.filter.qs
        data['breadcrumbs'] = self.breadcrumbs
        data['action_many'] = self.action_many
        data['action_one'] = self.action_one
        if self.action_static is not None: data['action_static'] = self.action_static
        return data
        
    def get_context_data(self, **kwargs):
        context = super(EfenuaListView, self).get_context_data(**kwargs)
        context.update(self.context())
        context['table_count'] = self.filter.qs.count()
        return context
    
class EfenuaUserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = ['username', 'last_name', 'first_name', 'is_active']  
       
@method_decorator(login_required, name='dispatch')
class EfenuaUserListView(EfenuaListView):
    queryset = User.objects.all()
    table_class = EfenuaUserTable
    filter_class = EfenuaUserFilter
    table_header = "Utilisateurs"
    action_static = (EfenuaMenuItemLink('user-create', 'Creer', icon="plus", options="primary"),)
    breadcrumbs = (EfenuaMenuItemBreadcrumbs('user-list', 'Liste des utilisateurs'),)

@method_decorator(permission_required('change_user'), name='dispatch')
@method_decorator(login_required, name='dispatch')
class EfenuaUserUpdateView(EfenuaUpdateView):
    model = User
    form_class = EfenuaUserForm
    breadcrumbs = (EfenuaMenuItemBreadcrumbs('user-list', 'Liste des utilisateurs'),)

@method_decorator(login_required, name='dispatch')
class EfenuaUserDetailView(EfenuaDetailView):
    model = User
    fields = ('username',)
    breadcrumbs = (EfenuaMenuItemBreadcrumbs('user-list', 'Liste des utilisateurs'),
                   EfenuaMenuItemBreadcrumbs('user-detail', 'Detail de l utilisateur'))
    
@method_decorator(permission_required('add_user'), name='dispatch')    
@method_decorator(login_required, name='dispatch')
class EfenuaUserCreateView(EfenuaCreateView):
    model = User
    form_class = EfenuaUserForm
    breadcrumbs = (EfenuaMenuItemBreadcrumbs('user-list', 'Liste des utilisateurs'),
                   EfenuaMenuItemBreadcrumbs('user-create', 'Creer un utilisateur'))
        
class EfenuaGroupFilter(django_filters.FilterSet):
    class Meta:
        model = Group
        fields = ['name', 'permissions'] 
       
@method_decorator(login_required, name='dispatch')
class EfenuaGroupListView(EfenuaListView):
    queryset = Group.objects.all()
    table_class = EfenuaGroupTable
    filter_class = EfenuaGroupFilter
    table_header = "Groupes"
    action_static = (EfenuaMenuItemLink('group-create', 'Creer', icon="plus", options="primary"),)
    breadcrumbs = (EfenuaMenuItemBreadcrumbs('group-list', 'Liste des groupes'),)
        
@method_decorator(permission_required('change_permission'), name='dispatch')
@method_decorator(login_required, name='dispatch')
class EfenuaGroupUpdateView(EfenuaUpdateView):
    model = Group
    form_class = EfenuaGroupForm
    breadcrumbs = (EfenuaMenuItemBreadcrumbs('group-list', 'Liste des groupes'),)
    
@method_decorator(login_required, name='dispatch')
class EfenuaGroupDetailView(EfenuaDetailView):
    model = Group
    fields = ('name',)
    breadcrumbs = (EfenuaMenuItemBreadcrumbs('group-list', 'Liste des groupes'),
                   EfenuaMenuItemBreadcrumbs('group-detail', 'Detail du groupe'))

@method_decorator(permission_required('add_group'), name='dispatch') 
@method_decorator(login_required, name='dispatch')
class EfenuaGroupCreateView(EfenuaCreateView):
    model = Group
    form_class = EfenuaGroupForm
    breadcrumbs = (EfenuaMenuItemBreadcrumbs('group-list', 'Liste des groupes'),
                   EfenuaMenuItemBreadcrumbs('group-create', 'Creer un groupe'))
    
class EfenuaPermissionFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_type='icontains')
    class Meta:
        model = Permission
        fields = ['name', 'codename']
       
@method_decorator(login_required, name='dispatch')
class EfenuaPermissionListView(EfenuaListView):
    queryset = Permission.objects.all()
    breadcrumbs = (EfenuaMenuItemBreadcrumbs('permission-list', 'Liste des permissions'),)
    table_class = EfenuaPermissionTable
    filter_class = EfenuaPermissionFilter
    table_header = "Permission"
    
@method_decorator(login_required, name='dispatch')
class EfenuaPermissionDetailView(EfenuaDetailView):
    model = Permission
    fields = ('name',)
    breadcrumbs = (EfenuaMenuItemBreadcrumbs('permission-list', 'Liste des permissions'),
                   EfenuaMenuItemBreadcrumbs('permission-detail', 'Detail de la permission'))

 
