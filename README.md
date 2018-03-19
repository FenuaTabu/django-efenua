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

Ajouter l'url suivante dans le projet
```python
url(r'^efenua/', include('efenua.urls')),
```

# Fonctionnaliés
- Nouvelle interface ADMIN
- Decorateur pour les actions

# Export
Pour ajouter une action export CSV
```python
#admin.py
from efenua.models import EfenuaModelAdmin
from efenua.actions import make_export_as_csv

class FooAdmin(EfenuaModelAdmin):
    actions = ['...', make_export_as_csv(fields=['title'])]
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

