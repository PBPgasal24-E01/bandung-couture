from django.shortcuts import render
from stores.models import Store, Category

def show(request):

    return render(request, 'show.html', {
        'categories': Category.objects.all(),
        'stores': Store.objects.all(),
    })
