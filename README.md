# django-efenua
A Django app for adding extra in the admin.

# Decorateurs

## Ajouter une colonne
```python
#admin.py
from efenua.models import EfenuaModelAdmin
from efenua.decorators import field

@admin.register(Mymodel)
class MymodelAdmin(EfenuaModelAdmin)
    list_display = ['foo']
    
    @field('my short description', admin_order_field='author.firstname', allow_tags=True)
    def foo(self, obj):
        return obj.author.first_name
```

## Ajouter une action
```python
#admin.py
from efenua.models import EfenuaModelAdmin
from efenua.decorators import action

@admin.register(Mymodel)
class MymodelAdmin(EfenuaModelAdmin)
    actions = ['foo']
    objectactions = ['foo']
    
    @action('my label', 'my short description')
    def foo(self, request, queryset):
        queryset.update(field='value')
```

# Ajouter des favoris sur des modeles
```python
#admin.py
from efenua.models import EfenuaModelAdmin
from efenua.utils import FavoriteFilter, add_to_favorite, delete_from_favorite

@admin.register(Mymodel)
class MymodelAdmin(EfenuaModelAdmin):
    list_filter = (FavoriteFilter,)
    actions = (add_to_favorite, delete_from_favorite)
```
