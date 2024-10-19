from django.shortcuts import render
from stores.models import Store, Category

def show(request):

    category_name = request.GET.get('category', 'All')

    if len(Category.objects.filter(name=category_name)) == 0:
        category_name = 'All'

    if category_name == 'All':
        stores = Store.objects.all()
    else:
        category = Category.objects.filter(name=category_name)[0]
        stores = Store.objects.filter(categories__in=[category])

    return render(request, 'show.html', {
        'categories': Category.objects.all(),
        'category_name': category_name,
        'stores': stores,
    })
