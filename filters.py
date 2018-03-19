# coding: utf-8
from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType

from efenua.models import Favorite


class FavoriteFilter(SimpleListFilter):

    title = _('Favorite')
    parameter_name = 'byfavorite'

    def lookups(self, request, model_admin):
        return (
            ('true', _('In favorite')),
            ('false', _('Outside favorite')),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            model = queryset.model
            model_name = model._meta.model_name
            app_label = model._meta.app_label
            try:
                ctype_id = ContentType.objects.get(app_label=app_label, 
                                                    model=model_name).id
            except ContentType.DoesNotExist:
                pass
            else:
                qs_ids = [q.id for q in queryset]
                item_ids = Favorite.objects.filter(ctype_id=ctype_id, 
                                item__in=qs_ids, 
                                user_id=request.user.id).values_list('item', flat=True)
                if value == 'true':
                    queryset = queryset.filter(id__in=item_ids)
                elif value == 'false':
                    queryset = queryset.exclude(id__in=item_ids)
                else:
                    queryset = queryset.none()
        return queryset
