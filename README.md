# django-efenua
A Django app for adding extra in the admin.

# Decorateurs

## Ajouter une colonne
```python
from efenua.models import EfenuaModelAdmin

class MymodelAdmin(EfenuaModelAdmin)
    list_display = ['foo']
    
    @field('my short description', admin_order_field='author.firstname', allow_tags=True)
    def foo(self, obj):
        return obj.author.first_name
```

## Ajouter une action
```python
from efenua.models import EfenuaModelAdmin
from efenua.decorators import action

class MymodelAdmin(EfenuaModelAdmin)
    actions = ['foo']
    objectactions = ['foo']
    
    @action('my label', 'my short description')
    def foo(self, request, queryset):
        queryset.update(field='value')
```

# Ajouter des favoris sur des models
```python
from efenua.utils import FavoriteFilter, add_to_favorite, delete_from_favorite

@admin.register(MyModel)
class MyModelAdmin(EfenuaModelAdmin):
    list_filter = (FavoriteFilter,)
    actions = (add_to_favorite, delete_from_favorite)
admin.site.register(MyModel, MyModelAdmin)
```
