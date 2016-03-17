# django-efenua
A Django app for adding extra in the admin.

#Pre requis
Ajouter dans INSTALLED_APPS
```python
 INSTALLED_APPS = [
    ...
    'efenua',
]
```

Ajouter dans MIDDLEWARE_CLASSES
```python
MIDDLEWARE_CLASSES = [
    ...
    'efenua.middleware.current_user.CurrentUserMiddleware',
]
```
# Export
Pour ajouter une action export CSV
```python
#admin.py
from efenua.models import EfenuaModelAdmin
from efenua.actions import export_as_csvAction

class FooAdmin(EfenuaModelAdmin):
    actions = ['...', export_as_csvAction(fields=['title'])]
```
.
# Favoris
Pour ajouter une colonne favorie dans list_view
```python
#admin.py
from efenua.models import EfenuaModelAdmin
from efenua.fields import favoriteField

class FooAdmin(EfenuaModelAdmin):
    list_display = ['...', favoriteField]
```

Pour ajouter un filtre favori
```python
#admin.py
from efenua.models import EfenuaModelAdmin
from efenua.filters import FavoriteFilter

class FooAdmin(EfenuaModelAdmin):
	list_filter = ['...', FavoriteFilter]
```

Pour ajouter des actions favoris
```python
#admin.py
from efenua.models import EfenuaModelAdmin
from efenua.actions import add_to_favoriteAction, delete_from_favoriteAction

class FooAdmin(EfenuaModelAdmin):
	actions = ['...', add_to_favoriteAction, delete_from_favoriteAction]
```

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

