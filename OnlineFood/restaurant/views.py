from django.db.models import Q
from django.shortcuts import render
from django.views import View

from restaurant.models import MenuItem,Category
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger


def showIndex(request):
    all_menuitems = MenuItem.objects.all()
    paginator = Paginator(all_menuitems, 4)
    page_number = request.GET.get('page')
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request,"restaurant/menu_items.html",{'menu_items':all_menuitems,'posts':posts})

class MenuSearch(View):
    def get(self,request):
        query = request.GET.get("q")
        menu_items = MenuItem.objects.filter(
            Q(name__icontains=query)
        )

        context = {
            'menu_items': menu_items
        }

        return render(request,'restaurant/menu_items.html', context)