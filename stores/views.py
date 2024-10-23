from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseBadRequest, HttpResponse, HttpResponseForbidden
from stores.models import Store, Category
from stores.forms import StoreForm

@login_required(login_url='/account/login')
def show(request):
    return render(request, 'show.html', {
        'categories': Category.objects.all(),
    })

def show_own(request):
    if not (request.user.is_authenticated and request.user.role == 2):
        #redirect to login page if the user is not authenticated or authorized as contributor
        return HttpResponseRedirect(reverse('account:login') + f'?next={request.get_full_path()}')

    categories = Category.objects.all()

    return render(request, 'show-own.html', {   
        'categories': categories,
        'csrf_token': request.COOKIES.get('csrftoken'),
        'form': StoreForm(),
    })

@require_POST
def add(request):

    form = StoreForm(request.POST)

    if form.is_valid():
        store = form.save() #safe with commit True to insert to database 
        #(so that manytomanyrelationship addition can be performed)

        store.user = request.user

        category_pks = request.POST.getlist('categories')
        for category_pk in category_pks:
            category = Category.objects.get(pk=category_pk)
            store.categories.add(category)

        #resave to update the changes in db
        store.save()

        return JsonResponse({'message': 'SUCCESS'}, status=200)
    
    return JsonResponse({'message': 'NOT SUCCESS'}, status=400)
    
@login_required(login_url='/account/login')
def deliver_all_stores_content_component(request):

    category_name = request.GET.get('category', 'All')

    if category_name != 'All' and not Category.objects.filter(name=category_name):
        return HttpResponseBadRequest()
    
    if category_name == 'All':
        stores = Store.objects.all()
    else:
        category = Category.objects.filter(name=category_name)[0]
        stores = Store.objects.filter(categories__in=[category])

    return render(request, 'stores-components/stores-content.html', {
        'stores': stores,
    })

def deliver_own_stores_content_component(request):
    if not (request.user.is_authenticated and request.user.role == 2):
        return HttpResponseRedirect(reverse('account:login') + f'?next={request.get_full_path()}')

    stores = Store.objects.filter(user=request.user)

    return render(request, 'stores-components/stores-content.html', {
        'stores': stores,
    })