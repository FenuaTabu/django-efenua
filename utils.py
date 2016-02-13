import csv
from django.http import HttpResponse
  

class EfenuaMenuItem():
    label = None
    url = None
    icon = None
    options = 'btn-default'
    attrs = None
    permissions_required = None
    
    def __init__(self, url, label, **kwargs):
        self.url = url
        self.label = label
        for name, value in kwargs.items():
            if name == "icon":
                self.icon = value
            if name == "permissions_required":
                self.permissions_required = value
            if name == "attrs":
                self.attrs = value
            if name == "options":
                self.options = 'btn-'+value
                
class EfenuaMenuItemLink(EfenuaMenuItem):                
    pass

class EfenuaMenuItemSubmit(EfenuaMenuItem): 
    pass

class EfenuaMenuItemBreadcrumbs(EfenuaMenuItem): 
    pass

class EfenuaMenu():
    items = []