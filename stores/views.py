from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from stores.models import Store, Category
from stores.forms import StoreForm

@login_required(login_url='/account/login')
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

def show_own(request):
    if request.user.is_authenticated and request.user.role == 2:

        stores = Store.objects.filter(user = request.user)
        categories = Category.objects.all()

        return render(request, 'show-own.html', {   
            'stores': stores,
            'categories': categories,
            'csrf_token': request.COOKIES.get('csrftoken'),
            'form': StoreForm(),
        })
    
    #redirect to login page if the user is not authenticated or authorized as contributor
    return HttpResponseRedirect(reverse('account:login') + f'?next={request.get_full_path()}')

@require_POST
def add(request):

    form = StoreForm(request.POST)

    if form.is_valid():
        store = form.save(commit=False)
        store.user = request.user
        store.save()
        return JsonResponse({'message': 'SUCCESS'}, status=200)
    
    return JsonResponse({'message': 'NOT SUCCESS'}, status=400)
    
    
    
