# from django.contrib.messages.views import SuccessMessageMixin
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
import django_tables2 as tables
import django_filters
from django.contrib.auth.models import User, Group, Permission

from efenua.widgets import DateTimePicker
from django_select2.forms import Select2MultipleWidget, Select2Widget
from django import forms
from efenua.form import Efenuaforms

forms.DateField.widget = DateTimePicker(options={"format": "YYYY-MM-DD","pickTime": False})
forms.ChoiceField.widget = Select2Widget()
forms.ModelMultipleChoiceField.widget = Select2MultipleWidget()

class EfenuaTable(tables.Table):
    pass
  
class EfenuaDashboardView(TemplateView):
    template_name = 'efenua/dashboard.html'
    
    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)
        
# class CreateView(SuccessMessageMixin, CreateView):
class EfenuaCreateView(CreateView):
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
            
# class UpdateView(SuccessMessageMixin, UpdateView):
class EfenuaUpdateView(UpdateView):
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
    
# class EfenuaDetailView(UpdateView):
#     template_name = 'efenua/detailview.html'
#     success_message = "%(msg)s a ete mise a jour avec succes"
#     action_static = None
#     breadcrumbs = None
# 
#     def get_success_message(self, cleaned_data):
#         return self.success_message % dict(
#             cleaned_data,
#             msg=self.object,
#         )
#     
#     def get_context_data(self, **kwargs):
#         context = super(EfenuaDetailView, self).get_context_data(**kwargs)
#         if self.action_static is not None: context['action_static'] = self.action_static
#         context['breadcrumbs'] = self.breadcrumbs
#         return context
    
class EfenuaDetailView(DetailView):
    template_name = 'efenua/detailview.html'
    fields = None
     
    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['fields'] = self.fields
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
        fields = ['username', 'last_name']

class EfenuaUserTable(tables.Table):
    selectable = tables.CheckBoxColumn(accessor='pk')
    actions = tables.TemplateColumn('<a href="{% url \'user-detail\' record.pk %}"><span class="glyphicon glyphicon-eye-open" aria-hidden="true"></span></a> <a href="{% url \'user-update\' record.pk %}"><span class="glyphicon glyphicon-edit" aria-hidden="true"></span></a>', verbose_name=" ")
    class Meta:
        model = User
        fields = ("selectable", "username", "email", "actions")
        attrs = {"class": "table"}   
       
@method_decorator(login_required, name='dispatch')
class EfenuaUserListView(EfenuaListView):
    queryset = User.objects.all()
    table_class = EfenuaUserTable
    filter_class = EfenuaUserFilter
    table_header = "Utilisateurs"
    action_static = (EfenuaMenuItemLink('user-create', 'Creer', icon="plus", options="primary"),)
    
class EfenuaUserForm(Efenuaforms):
    class Meta:
        model = User
        fields = '__all__'

@method_decorator(permission_required('change_user'), name='dispatch')
@method_decorator(login_required, name='dispatch')
class EfenuaUserUpdateView(EfenuaUpdateView):
    model = User
    form_class = EfenuaUserForm

@method_decorator(login_required, name='dispatch')
class EfenuaUserDetailView(EfenuaDetailView):
    model = User
    fields = ('username',)
    
@method_decorator(permission_required('add_user'), name='dispatch')    
@method_decorator(login_required, name='dispatch')
class EfenuaUserCreateView(EfenuaCreateView):
    model = User
    form_class = EfenuaUserForm
    
class EfenuaGroupFilter(django_filters.FilterSet):
    class Meta:
        model = Group
        fields = ['name', 'permissions']

class EfenuaGroupTable(tables.Table):
    selectable = tables.CheckBoxColumn(accessor='pk')
    actions = tables.TemplateColumn('<a href="{% url \'group-detail\' record.pk %}"><span class="glyphicon glyphicon-eye-open" aria-hidden="true"></span></a> <a href="{% url \'group-update\' record.pk %}"><span class="glyphicon glyphicon-edit" aria-hidden="true"></span></a>', verbose_name=" ")
    class Meta:
        model = Group
        fields = ("selectable", "name", "permissions", "actions")
        attrs = {"class": "table"}   
       
@method_decorator(login_required, name='dispatch')
class EfenuaGroupListView(EfenuaListView):
    queryset = Group.objects.all()
    table_class = EfenuaGroupTable
    filter_class = EfenuaGroupFilter
    table_header = "Groupes"
    action_static = (EfenuaMenuItemLink('group-create', 'Creer', icon="plus", options="primary"),)
   
class EfenuaGroupForm(Efenuaforms):
    class Meta:
        model = Group
        fields = '__all__'
        
@method_decorator(permission_required('change_permission'), name='dispatch')
@method_decorator(login_required, name='dispatch')
class EfenuaGroupUpdateView(EfenuaUpdateView):
    model = Group
    form_class = EfenuaGroupForm
    
@method_decorator(login_required, name='dispatch')
class EfenuaGroupDetailView(EfenuaDetailView):
    model = Group
    fields = ('name',)

@method_decorator(permission_required('add_group'), name='dispatch') 
@method_decorator(login_required, name='dispatch')
class EfenuaGroupCreateView(EfenuaCreateView):
    model = Group
    form_class = EfenuaGroupForm
    
class EfenuaPermissionFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_type='icontains')
    class Meta:
        model = Permission
        fields = ['name', 'codename']

class EfenuaPermissionTable(tables.Table):
    selectable = tables.CheckBoxColumn(accessor='pk')
    actions = tables.TemplateColumn('<a href="{% url \'permission-detail\' record.pk %}"><span class="glyphicon glyphicon-eye-open" aria-hidden="true"></span></a> <a href="{% url \'permission-update\' record.pk %}"><span class="glyphicon glyphicon-edit" aria-hidden="true"></span></a>', verbose_name=" ")
    class Meta:
        model = Permission
        fields = ("selectable", "name", "codename", "actions")
        attrs = {"class": "table"}   
       
@method_decorator(login_required, name='dispatch')
class EfenuaPermissionListView(EfenuaListView):
    queryset = Permission.objects.all()
    breadcrumbs = (EfenuaMenuItemBreadcrumbs('permission-list', 'Liste des permissions'),)
    table_class = EfenuaPermissionTable
    filter_class = EfenuaPermissionFilter
    table_header = "Permission"
    action_static = (EfenuaMenuItemLink('permission-create', 'Creer', icon="plus", options="primary"),)
    
class EfenuaPermissionForm(Efenuaforms):
    class Meta:
        model = Permission
        fields = '__all__'

@method_decorator(permission_required('change_permission'), name='dispatch')
@method_decorator(login_required, name='dispatch')
class EfenuaPermissionUpdateView(EfenuaUpdateView):
    model = Permission
    form_class = EfenuaPermissionForm
    breadcrumbs = (EfenuaMenuItemBreadcrumbs('permission-list', 'Liste des permissions'),)
    
@method_decorator(login_required, name='dispatch')
class EfenuaPermissionDetailView(EfenuaDetailView):
    model = Permission
    fields = ('name',)
    breadcrumbs = (EfenuaMenuItemBreadcrumbs('permission-list', 'Liste des permissions'),
                   EfenuaMenuItemBreadcrumbs('permission-detail', 'Detail de la permission'))

@method_decorator(permission_required('add_permission'), name='dispatch')
@method_decorator(login_required, name='dispatch')
class EfenuaPermissionCreateView(EfenuaCreateView):
    model = Permission
    form_class = EfenuaPermissionForm
    breadcrumbs = (EfenuaMenuItemBreadcrumbs('permission-list', 'Liste des permissions'),
                   EfenuaMenuItemBreadcrumbs('permission-create', 'Creer une permission'))