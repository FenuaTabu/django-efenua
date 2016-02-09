import django_tables2 as tables
from django.contrib.auth.models import User, Group, Permission

class EfenuaTable(tables.Table):
    pass

class EfenuaUserTable(tables.Table):
    selectable = tables.CheckBoxColumn(accessor='pk')
    actions = tables.TemplateColumn('<a href="{% url \'user-detail\' record.pk %}"><span class="glyphicon glyphicon-eye-open" aria-hidden="true"></span></a> <a href="{% url \'user-update\' record.pk %}"><span class="glyphicon glyphicon-edit" aria-hidden="true"></span></a>', verbose_name=" ")
    class Meta:
        model = User
        fields = ("selectable", "username", "email", "actions")
        attrs = {"class": "table"} 
        
class EfenuaGroupTable(tables.Table):
    selectable = tables.CheckBoxColumn(accessor='pk')
    actions = tables.TemplateColumn('<a href="{% url \'group-detail\' record.pk %}"><span class="glyphicon glyphicon-eye-open" aria-hidden="true"></span></a> <a href="{% url \'group-update\' record.pk %}"><span class="glyphicon glyphicon-edit" aria-hidden="true"></span></a>', verbose_name=" ")
    class Meta:
        model = Group
        fields = ("selectable", "name", "permissions", "actions")
        attrs = {"class": "table"}
        
class EfenuaPermissionTable(tables.Table):
    selectable = tables.CheckBoxColumn(accessor='pk')
    actions = tables.TemplateColumn('<a href="{% url \'permission-detail\' record.pk %}"><span class="glyphicon glyphicon-eye-open" aria-hidden="true"></span></a> <a href="{% url \'permission-update\' record.pk %}"><span class="glyphicon glyphicon-edit" aria-hidden="true"></span></a>', verbose_name=" ")
    class Meta:
        model = Permission
        fields = ("selectable", "name", "codename", "actions")
        attrs = {"class": "table"}   