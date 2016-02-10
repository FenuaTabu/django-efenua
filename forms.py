from copy import deepcopy

from django import forms
from django.forms.utils import flatatt
from django.utils.safestring import mark_safe
from form_utils.forms import BetterModelForm
from django.contrib.auth.models import User, Group, Permission
from django_select2.forms import Select2MultipleWidget

class Efenuaforms(BetterModelForm):
    pass

class EfenuaUserForm(Efenuaforms):
    class Meta:
        model = User
        fields = '__all__'
#         fieldsets = [('main', {'fields': ['username', 'password', 'last_name', 'first_name', 'email'], 'legend': ''}),
#                      ('Acces', {'fields': ['groups', 'user_permissions'],}),
#                      ('Autres', {'fields': ['is_staff', 'is_active', 'is_superuser'],})]
        widgets = {
            'groups': Select2MultipleWidget,
            'user_permissions': Select2MultipleWidget
        }
        
class EfenuaGroupForm(Efenuaforms):
    class Meta:
        model = Group
        fields = '__all__'
        widgets = {
            'permissions': Select2MultipleWidget
        }