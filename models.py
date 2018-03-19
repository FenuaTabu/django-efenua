from __future__ import unicode_literals

from django.contrib import admin
from django.conf.urls import url
from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin
from django.http import Http404, HttpResponseRedirect
from django.http.response import HttpResponseBase
from django.urls import reverse
from django.contrib.admin.widgets import ManyToManyRawIdWidget, ForeignKeyRawIdWidget
from django.contrib.admin.sites import site
from django.utils.html import escape
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.conf import settings

from efenua.middleware.current_user import get_current_user


class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=get_current_user, editable=False)
    ctype = models.ForeignKey(ContentType, related_name='ctype_favorite')
    item = models.PositiveIntegerField()
    deadline = models.DateField(null=True, blank=True)
    label = models.CharField(null=True, max_length=150)
    description = models.TextField(null=True, blank=True)
    
    class Meta:
        unique_together = ('user', 'ctype', 'item')


class VerboseForeignKeyRawIdWidget(ForeignKeyRawIdWidget):
    def label_for_value(self, value):
        key = self.rel.get_related_field().name
        try:
            obj = self.rel.to._default_manager.using(self.db).get(**{key: value})
            
            if 'raw_id_value' in dir(obj):
                    str_values += [obj.raw_id_value()]
            else:
                change_url = reverse(
                    "admin:%s_%s_change" % (obj._meta.app_label, obj._meta.object_name.lower()),
                    args=(obj.pk,)
                )
                return '<a href="%s" class="label label-default">%s</a>' % (change_url, escape(obj))
        except (ValueError, self.rel.to.DoesNotExist):
            return '???'


class VerboseManyToManyRawIdWidget(ManyToManyRawIdWidget):
    def label_for_value(self, value):
        values = value.split(',')
        str_values = []
        key = self.rel.get_related_field().name
        for v in values:
            try:
                obj = self.rel.to._default_manager.using(self.db).get(**{key: v})
                if 'raw_id_value' in dir(obj):
                    str_values += [obj.raw_id_value()]
                else:
                    x = obj
                    change_url = reverse(
                        "admin:%s_%s_change" % (obj._meta.app_label, obj._meta.object_name.lower()),
                        args=(obj.pk,)
                    )
                    str_values += ['<a href="%s" class="label label-default">%s</a>' % (change_url, escape(x))]
            except self.rel.to.DoesNotExist:
                str_values += [u'???']
        return u', '.join(str_values)


class EfenuaModelAdmin(admin.ModelAdmin):
    objectactions = []
    tools_view_name = None
    
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name in self.raw_id_fields:
            kwargs.pop("request", None)
            type = db_field.rel.__class__.__name__
            if type == "ManyToOneRel":
                kwargs['widget'] = VerboseForeignKeyRawIdWidget(db_field.rel, site)
            elif type == "ManyToManyRel":
                kwargs['widget'] = VerboseManyToManyRawIdWidget(db_field.rel, site)
            return db_field.formfield(**kwargs)
        return super(EfenuaModelAdmin, self).formfield_for_dbfield(db_field, **kwargs)

    def get_tool_urls(self):
        tools = {}

        # Look for the default change view url and use that as a template
        try:
            model_name = self.model._meta.model_name
        except AttributeError:
            # DJANGO15
            model_name = self.model._meta.module_name
        base_url_name = '%s_%s' % (self.model._meta.app_label, model_name)
        model_tools_url_name = '%s_tools' % base_url_name
        change_view = 'admin:%s_change' % base_url_name

        self.tools_view_name = 'admin:' + model_tools_url_name

        for tool in self.objectactions:
            tools[tool] = getattr(self, tool)
        return [
            # supports pks that are numbers or uuids
            url(r'^(?P<pk>[0-9a-f\-]+)/tools/(?P<tool>\w+)/$',
                self.admin_site.admin_view(  # checks permissions
                    ModelToolsView.as_view(
                        model=self.model,
                        tools=tools,
                        back=change_view,
                    )
                ),
                name=model_tools_url_name)
        ]

    # EXISTING ADMIN METHODS MODIFIED
    #################################

    def get_urls(self):
        urls = super(EfenuaModelAdmin, self).get_urls()
        return self.get_tool_urls() + urls

    def render_change_form(self, request, context, **kwargs):

        def to_dict(tool_name):
            tool = getattr(self, tool_name)
            standard_attrs, custom_attrs = self.get_djoa_button_attrs(tool)
            return dict(
                name=tool_name,
                label=getattr(tool, 'label', tool_name),
                standard_attrs=standard_attrs,
                custom_attrs=custom_attrs,
            )

        context['objectactions'] = map(
            to_dict,
            self.get_object_actions(request, context, **kwargs)
        )
        context['tools_view_name'] = self.tools_view_name
        return super(EfenuaModelAdmin, self).render_change_form(
            request, context, **kwargs)

    # CUSTOM METHODS
    ################

    def get_object_actions(self, request, context, **kwargs):
        return self.objectactions

    def get_djoa_button_attrs(self, tool):
        attrs = getattr(tool, 'attrs', {})
        # href is not allowed to be set. should an exception be raised instead?
        if 'href' in attrs:
            attrs.pop('href')
        # title is not allowed to be set. should an exception be raised instead?
        # `short_description` should be set instead to parallel django admin
        # actions
        if 'title' in attrs:
            attrs.pop('title')
        default_attrs = {
            'class': attrs.get('class', ''),
            'title': getattr(tool, 'short_description', ''),
        }
        standard_attrs = {}
        custom_attrs = {}
        for k, v in dict(default_attrs, **attrs).items():
            if k in default_attrs:
                standard_attrs[k] = v
            else:
                custom_attrs[k] = v
        return standard_attrs, custom_attrs


class ModelToolsView(SingleObjectMixin, View):
    back = None
    model = None
    tools = None

    def get(self, request, **kwargs):
        # SingleOjectMixin's `get_object`. Works because the view
        #   is instantiated with `model` and the urlpattern has `pk`.
        obj = self.get_object()
        try:
            tool = self.tools[kwargs['tool']]
        except KeyError:
            raise Http404(u'Tool does not exist')

        ret = tool(request, obj)
        if isinstance(ret, HttpResponseBase):
            return ret

        back = reverse(self.back, args=(kwargs['pk'],))
        return HttpResponseRedirect(back)

    # HACK to allow POST requests too easily
    post = get

    def message_user(self, request, message):
        messages.info(request, message)
