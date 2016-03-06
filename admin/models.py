from __future__ import unicode_literals

from django.contrib import admin
from django.conf.urls import url
from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin

from django.http import Http404, HttpResponseRedirect
from django.http.response import HttpResponseBase
from django.core.urlresolvers import reverse

from django.contrib.admin.widgets import ManyToManyRawIdWidget, ForeignKeyRawIdWidget
from django.contrib.admin.sites import site

from django import forms
from django.utils.html import escape

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
                return '<div class="ui label"><a href="%s">%s</a></div>' % (change_url, escape(obj))
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
                    str_values += ['<div class="ui label"><a href="%s">%s</a></div>' % (change_url, escape(x))]
            except self.rel.to.DoesNotExist:
                str_values += [u'???']
        return u', '.join(str_values)

class EfenuaModelAdmin(admin.ModelAdmin):
    
    """
    ModelAdmin mixin to add object-tools just like adding admin actions.

    Attributes
    ----------
    model : django.db.models.Model
        The Django Model these tools work on. This is populated by Django.
    objectactions : list
        Write the names of the callable attributes (methods) of the model admin
        that can be used as tools.
    tools_view_name : str
        The name of the Django Object Actions admin view, including the 'admin'
        namespace. Populated by `get_tool_urls`.
    """
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
        """Get the url patterns that route each tool to a special view."""
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
        """Prepend `get_urls` with our own patterns."""
        urls = super(EfenuaModelAdmin, self).get_urls()
        return self.get_tool_urls() + urls

    def render_change_form(self, request, context, **kwargs):
        """Put `objectactions` into the context."""

        def to_dict(tool_name):
            """To represents the tool func as a dict with extra meta."""
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
        """
        Override this method to customize what actions get sent.

        For example, to restrict actions to superusers, you could do:

            class ChoiceAdmin(DjangoObjectActions, admin.ModelAdmin):
                def get_object_actions(self, request, context, **kwargs):
                    if request.user.is_superuser:
                        return super(ChoiceAdmin, self).get_object_actions(
                            request, context, **kwargs
                        )
                    return []
        """
        return self.objectactions

    def get_djoa_button_attrs(self, tool):
        """
        Get the HTML attributes associated with a tool.

        There are some standard attributes (class and title) that the template
        will always want. Any number of additional attributes can be specified
        and passed on. This is kinda awkward and due for a refactor for
        readability.
        """
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
    """
    The view that runs the tool's callable.

    Attributes
    ----------
    back : str
        The urlpattern name to send users back to. Defaults to the change view.
    model : django.db.model.Model
        The model this tool operates on.
    tools : dict
        A mapping of tool names to tool callables.
    """
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
        """
        Mimic Django admin actions's `message_user`.

        Like the second example:
        https://docs.djangoproject.com/en/1.9/ref/contrib/admin/actions/#custom-admin-action
        """
        messages.info(request, message)