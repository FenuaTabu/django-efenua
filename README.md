# django-efenua
A Django app for adding extra in the admin.

# Ajouter des favoris sur des models
```python
from efenua.utils import FavoriteFilter, add_to_favorite, delete_from_favorite

@admin.register(MyModel)
class MyModelAdmin(EfenuaModelAdmin):
    list_filter = (FavoriteFilter,)
    actions = (add_to_favorite, delete_from_favorite)
admin.site.register(MyModel, MyModelAdmin)
```
