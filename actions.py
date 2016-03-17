import csv
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from efenua.decorators import action

@action(_('Ajouter aux favoris'), _('Ajouter aux favoris'))
def add_to_favoriteAction(modeladmin, request, queryset):
    model = modeladmin.model
    model_name = model._meta.model_name
    app_label = model._meta.app_label
    try:
        ctype_id = ContentType.objects.get(app_label=app_label, 
                                            model=model_name).id
    except ContentType.DoesNotExist:
        pass
    else:
        qs_ids = [q.id for q in queryset]
        exist_ids = Favorite.objects.filter(user_id=request.user.id,
                                    ctype_id=ctype_id,
                                    item__in=qs_ids)
        queryset = queryset.exclude(id__in=exist_ids)
        for q in queryset:
            Favorite.objects.create(user_id=request.user.id, item=q.id, ctype_id=ctype_id)

@action(_('Enlever des favoris'), _('Enlever Des favoris'))
def delete_from_favoriteAction(modeladmin, request, queryset):
    model = modeladmin.model
    model_name = model._meta.model_name
    app_label = model._meta.app_label
    try:
        ctype_id = ContentType.objects.get(app_label=app_label, 
                                            model=model_name).id
    except ContentType.DoesNotExist:
        pass
    else:
        qs_ids = [q.id for q in queryset]
        Favorite.objects.filter(user_id=request.user.id,
                                ctype_id=ctype_id,
                                item__in=qs_ids).delete()

def export_as_csvAction(fields=None, exclude=None, header=True):
    """
    This function returns an export csv action
    'fields' and 'exclude' work like in django ModelForm
    'header' is whether or not to output the column names as the first row
    """

    from itertools import chain

    @action(_('Export CSV'), _('Export CSV'))
    def export_as_csvAction(modeladmin, request, queryset):
        """
        Generic csv export admin action.
        """
        opts = modeladmin.model._meta
        field_names = set([field.name for field in opts.fields])
        many_to_many_field_names = set([many_to_many_field.name for many_to_many_field in opts.many_to_many])
        if fields:
            fieldset = set(fields)
            field_names = field_names & fieldset
        elif exclude:
            excludeset = set(exclude)
            field_names = field_names - excludeset

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s.csv' % str(opts).replace('.', '_')

        writer = csv.writer(response)
        if header:
            writer.writerow(list(chain(field_names, many_to_many_field_names)))
        for obj in queryset:
            row = []
            for field in field_names:
                row.append(getattr(obj, field))
            for field in many_to_many_field_names:
                row.append(getattr(obj, field).all())

            writer.writerow(row)
        return response
    return export_as_csvAction