from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.core import serializers
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseBadRequest, HttpResponse
from stores.models import Store, Category
from stores.forms import StoreForm
from wishlist.models import Wishlist
import json

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

@require_POST
def edit(request, pk):

    stores = Store.objects.filter(pk=pk, user=request.user)

    if not stores:
        return HttpResponseBadRequest()
    
    store = stores[0]

    form = StoreForm(request.POST, instance=store)

    if form.is_valid():
        category_pks = request.POST.getlist('categories')
        for category_pk in category_pks:
            category = Category.objects.get(pk=category_pk)
            store.categories.add(category)

        #resave to update the changes in db
        store.save()

        return JsonResponse({'message': 'SUCCESS'}, status=200)
    
    return JsonResponse({'message': 'NOT SUCCESS'}, status=400)


@require_POST
def delete(request, pk):

    stores = Store.objects.filter(pk=pk, user=request.user)

    #if no store found with specified primary key or requesting user is not the owner of the store
    if not stores:
        return JsonResponse({'message': 'NOT SUCCESS'}, status=400)
    
    stores[0].delete()
    return JsonResponse({'message': 'SUCCESS'}, status=200)
    
    
@login_required(login_url='/account/login')
def deliver_all_stores_content_component(request):

    category_name = request.GET.get('category', 'All')

    if category_name != 'All' and not Category.objects.filter(name=category_name):
        return HttpResponseBadRequest()
    
    wishlist_items = Wishlist.objects.filter(user=request.user).values_list('store_id', flat=True)
    
    if category_name == 'All':
        stores = Store.objects.all()
    else:
        category = Category.objects.filter(name=category_name)[0]
        stores = Store.objects.filter(categories__in=[category])

    return render(request, 'stores-components/stores-content.html', {
        'stores': stores,
        'edit': False,
        'wishlist_items': wishlist_items
    })

def deliver_own_stores_content_component(request):
    if not (request.user.is_authenticated and request.user.role == 2):
        return HttpResponseRedirect(reverse('account:login') + f'?next={request.get_full_path()}')

    stores = Store.objects.filter(user=request.user)

    return render(request, 'stores-components/stores-content.html', {
        'stores': stores,
        'edit': True,
    })

@require_GET
def deliver_store_form(request, pk=None):

    #require to be authenticated as contributor
    if not (request.user.is_authenticated and request.user.role == 2):
        return HttpResponseRedirect(reverse('account:login') + f'?next={request.get_full_path()}')

    if pk == None:
        form = StoreForm()
    else:
        stores = Store.objects.filter(pk=pk, user=request.user)
        if not stores:
            return HttpResponseBadRequest()
        
        form = StoreForm(instance=stores[0])

    return HttpResponse(form)

@require_GET
def show_rest_all(request):
    stores = Store.objects.all()
    return HttpResponse(serializers.serialize('json', stores), content_type='application/json')

@require_GET
def show_rest_own(request):
    if request.user.is_authenticated and request.user.role == 2:
        stores = Store.objects.filter(user = request.user)
    else: 
        stores = Store.objects.none()
    
    return HttpResponse(serializers.serialize('json', stores), content_type='application/json')

@require_POST
@csrf_exempt #does not require csrf token from mobile unless csrf can be fetched to the mobile
def add_mobile(request):

    if not request.user.is_authenticated or request.user.role != 2:
        return JsonResponse({
            'status': 'error',
            'description': 'failed: attempted to contribute a store as a non-contributor',
        }, status=400)
    
    try:
        data = json.loads(request.body)
        brand = data['brand']
        description = data['description']
        address = data['address']
        contact_number = data['contact_number']
        website = data['website']
        social_media = data['social_media']

        store = Store.objects.create(user=request.user, brand=brand, description=description, address=address,
                             contact_number=contact_number, website=website, social_media=social_media)
        store.save()

        return JsonResponse({
            'status': 'success',
            'description': 'successfully stored contributed store to database',
        }, status=200)

    except KeyError:
        return JsonResponse({
            'status': 'error',
            'description': 'incomplete parameters',
        }, status=400)

@require_POST
@csrf_exempt
def edit_mobile(request):
    if not request.user.is_authenticated or request.user.role != 2:
        return JsonResponse({
            'status': 'error',
            'description': 'attempted to contribute a store as a non-contributor',
        }, status=400)

    try:
        data = json.loads(request.body)
        pk = int(data['pk'])

        stores = Store.objects.filter(pk=pk, user=request.user)
        if len(stores) == 0:
            return JsonResponse({
                'status': 'error',
                'description': 'referred store does not exist',
            }, status=400)
        
        store = stores[0]

        brand = data['brand']
        description = data['description']
        address = data['address']
        contact_number = data['contact_number']
        website = data['website']
        social_media = data['social_media']

        store.brand = brand
        store.description = description
        store.address = address
        store.contact_number = contact_number
        store.website = website
        store.social_media = social_media

        store.save()

        return JsonResponse({
            'status': 'success',
            'description': 'store successfully updated',
        }, status=200)

    except KeyError:
        return JsonResponse({
            'status': 'error',
            'description': 'incomplete parameters',
        }, status=400)

    except:
        return JsonResponse({
            'status': 'error',
            'description': 'unexpected error',
        }, status=500)

@require_POST
@csrf_exempt
def delete_mobile(request):

    if not request.user.is_authenticated or request.user.role != 2:
        return JsonResponse({
            'status': 'error',
            'description': 'store deletion attempt by non-contributor',
        }, status=400)

    data = json.loads(request.body)
    pk = int(data['pk'])

    stores = Store.objects.filter(user=request.user, pk=pk)
    if len(stores) == 0:
        return JsonResponse({
            'status': 'error',
            'description': 'store not found, perhaps already deleted',
        }, status=400)
    store = stores[0]
    store.delete()

    return JsonResponse({
        'status': 'success',
        'description': f'successfully deleted store {store.brand}',
    }, status=200)


