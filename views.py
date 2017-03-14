from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.apps import apps
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.contenttypes.models import ContentType

from django.core.urlresolvers import reverse
from efenua.models import Favorite

def add_to_favorite(request, app_label, model_name, item_id):
    try:
        item_id = int(item_id)
    except ValueError:
        pass
    else:
        try:
            ctype_id = ContentType.objects.get(app_label=app_label, 
                                                model=model_name).id
        except ContentType.DoesNotExist:
            pass
        else:
            favorites = Favorite.objects.filter(user_id=request.user.id, 
                                                ctype_id=ctype_id, 
                                                item=item_id)
            if not favorites:
                Favorite.objects.create(user_id=request.user.id,
                                        ctype_id=ctype_id,
                                        item=item_id)
    next = request.GET.get('next', '') or ''
    if not next:
        next = reverse('admin:index')
    return redirect(next)


def delete_from_favorite(request, app_label, model_name, item_id):
    try:
        item_id = int(item_id)
    except ValueError:
        pass
    else:
        try:
            ctype_id = ContentType.objects.get(app_label=app_label, 
                                                model=model_name).id
        except ContentType.DoesNotExist:
            pass
        else:
            Favorite.objects.filter(user_id=request.user.id, 
                                    ctype_id=ctype_id, 
                                    item=item_id).delete()
    next = request.GET.get('next', '') or ''
    if not next:
        next = reverse('admin:index')
    return redirect(next)

def yuml(request):
    loaded_models = apps.get_models()
    
    excludes = ['sessions.session', 'contenttypes.contenttype', 'admin.logentry']
    
    result = []
    
    for model in loaded_models:
        if str(model._meta) not in excludes:
            r = str(model._meta) + '|'
            relations = []
    
            for field in model._meta.get_fields():
                if field.__class__.__name__=='AutoField':
                    pass
                
                elif field.__class__.__name__=='ForeignKey':
                    if str(field.rel.to._meta) not in excludes:
                        relations.append("[%s]1-0..*[%s]" % (model._meta, field.rel.to._meta))
                    
                elif field.__class__.__name__=='ManyToManyField':
                    if str(field.rel.to._meta) not in excludes:
                        relations.append("[%s]0..*-0..*[%s]" % (model._meta, field.rel.to._meta))
                
                elif field.__class__.__name__=='ManyToOneRel' or field.__class__.__name__=='ManyToManyRel' or field.__class__.__name__=='GenericForeignKey':
                    pass
                    
                elif field.__class__.__name__=='OneToOneRel':
                    pass
                
                else:
                    pass
                    r += "%s:%s;" % (field.attname, field.__class__.__name__)
            result.append('[' + r  + ']')
            for relation in relations:
                result.append(relation)
    
    
    return render_to_response(
        "efenua/yuml.html",
        {'objects' : result},
        RequestContext(request, {}),
    )
yuml = staff_member_required(yuml)
