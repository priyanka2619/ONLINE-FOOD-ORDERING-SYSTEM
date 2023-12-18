from django.urls import path
from restaurant import views



urlpatterns = [
    path('',views.showIndex,name='menuitems'),
    path('menuitems/search/',views.MenuSearch.as_view(),name='menu_items_search'),
]


