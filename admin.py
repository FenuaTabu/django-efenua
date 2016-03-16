# coding: utf-8
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType

from efenua.models import Favorite


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['label', 'ctype', 'deadline']

    def queryset(self, request):
        queryset = super(FavoriteAdmin, self).queryset(request)
        model = self.model
        model_name = model._meta.module_name
        app_label = model._meta.app_label
        qs_ids = [i.id for i in queryset]
        try:
            ctype_id = ContentType.objects.get(app_label=app_label, 
                                                model=model_name).id
        except ContentType.DoesNotExist:
            pass
        else:
            favorites = Favorite.objects.filter(user_id=request.user.id, 
                                ctype_id=ctype_id, 
                                item__in=qs_ids).values_list('item', flat=True)
            self.model.items_list = favorites
            self.model.next = request.get_full_path()
        return queryset