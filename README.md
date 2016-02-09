# django-efenua
django-efenua simplifie la création d'application.
Le package utilise les vue basé sur les classes de django

# Configuration
- Ajouter dans votre `settings.py`

```python
#settings.py
INSTALLED_APPS = [
    ...
    'efenua',
    ...
]

LOGIN_REDIRECT_URL = "dashboard
```

- Ajouter dans votre fichier `url.py`
 
```python
url(r'^', include('efenua.urls'))
```

# Exemple
## Créer une vue de type liste

```python
# views.py
from efenua import efenuaListView
import django_tables2 as tables
import django_filters
from app.models import Foo
  
class FooFilter(django_filters.FilterSet):
    class Meta:
        model = Foo
        fields = ['field_1', 'field2']

class FooTable(tables.Table):
    class Meta:
        model = Foo
        fields = ("field_1", "field_2")

class FooListView(EfenuaListView):
    queryset = Foo.objects.all()
    table_class = FooTable
    filter_class = FooFilter
    table_header = "Foo"
```

```python
# urls.py
from efenua.urls import URLGenerator
from uis.models import Foo
from uis.views import FooListView

urlpatterns = [
  ...
  URLGenerator( Foo ).get_list_url(FooListView),
  ...
]
```

## Créer une vue de type Create
```python
# forms.py
from efenua.forms import Efenuaforms

class FooForm(Efenuaforms):
    class Meta:
        model = Foo
        fields = '__all__'

```

```python
# views.py
from efenua.views import EfenuaCreateView
from app.forms import FooForm

class FooCreateView(EfenuaCreateView):
    model = Foo
    form_class = FooForm
```

```python
# urls.py
from efenua.urls import URLGenerator
from uis.models import Foo
from uis.views import FooCreateView

urlpatterns = [
  ...
  URLGenerator( Foo ).get_create_url(FooCreateView),
  ...
]
```

## Créer une vue de type Update
```python
# forms.py
from efenua.forms import Efenuaforms

class FooForm(Efenuaforms):
    class Meta:
        model = Foo
        fields = '__all__'

```

```python
# views.py
from efenua.views import EfenuaUpdateView
from app.forms import FooForm

class FooUpdateView(EfenuaUpdateView):
    model = Foo
    form_class = FooForm
```

```python
# urls.py
from efenua.urls import URLGenerator
from uis.models import Foo
from uis.views import FooUpdateView

urlpatterns = [
  ...
  URLGenerator( Foo ).get_update_url(FooUpdateView),
  ...
]
```
