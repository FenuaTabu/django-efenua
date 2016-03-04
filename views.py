from django.template import RequestContext
from django.shortcuts import render_to_response
from django.apps import apps
from django.contrib.admin.views.decorators import staff_member_required


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
                
                elif field.__class__.__name__=='ManyToOneRel' or field.__class__.__name__=='ManyToManyRel':
                    pass
                
                else:
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