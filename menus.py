from menu import Menu, MenuItem
from django.core.urlresolvers import reverse

Menu.add_item("user", MenuItem("Deconnexion",
   reverse("logout"),
   weight=100,
   icon="off",
   check=lambda request: request.user.is_authenticated),
)

Menu.add_item("main", MenuItem("Dashboard",
    reverse("dashboard"),
    weight=10,
    icon="home",
    check=lambda request: request.user.is_authenticated),
)
              
myaccount_children = (
    MenuItem("Groupes",
             reverse("group-list"),
             weight=10,
             icon="cog"),
    MenuItem("Permissions",
             reverse("permission-list"),
             weight=20,
             icon="lock"),
    MenuItem("Utilisateurs",
             reverse("user-list"),
             weight=30,
             icon="user"),
)
              
Menu.add_item("main", MenuItem("Systeme",
   reverse("user-list"),
   weight=100,
   icon="cog",
   children=myaccount_children,
   check=lambda request: request.user.is_authenticated),
)