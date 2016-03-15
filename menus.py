from efenua.menu import Menu, MenuItem
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _


if (lambda request: request.user.is_anonymous) and (lambda request: request.user.has_usable_password):
    Menu.add_item("user", MenuItem(_("Change password"),
                               reverse("admin:password_change"),
                               weight=10,
                               icon="tools",))
    


# Menu.add_item("main", MenuItem(_("View site"),
                               # reverse("site_url"),
                               # weight=10,
                               # icon="tools",
                               # check = lambda request: request.docsroot))
                               
# Menu.add_item("dev", MenuItem(_("Documentation"),
#                                reverse("django-admindocs-docroot"),
#                                weight=10,
#                                icon="tools",
#                                check = lambda request: request'django-admindocs-docroot'))
                               
Menu.add_item("dev", MenuItem(_("yUML"),
                               reverse("yuml"),
                               weight=10,
                               icon="tools"))
                               

                               
Menu.add_item("user", MenuItem(_("Log out"),
                               reverse("admin:logout"),
                               weight=100,
                               icon="tools"))
                               
