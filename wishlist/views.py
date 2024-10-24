from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from wishlist.models import Wishlist
from stores.models import Store,Category
from django.http import JsonResponse

def wishlist_view(request):
    # Assuming you have a user and a wishlist associated with that user
    wishlist_items = Wishlist.objects.filter(user=request.user)
    wishlisted_store_ids = wishlist_items.values_list('store__id', flat=True)

    # Fetch products that are not in the wishlist
    non_wishlist_stores = Store.objects.exclude(id__in=wishlisted_store_ids)
    print(f"Non-wishlist Stores: {non_wishlist_stores}")
    recommended_stores = non_wishlist_stores.order_by('?')[:2]

    return render(request, 'wishlist.html', {
        'wishlists': wishlist_items,
        'categories': Category.objects.all(),
        'recommended_stores': recommended_stores  
    })


@login_required(login_url='/account/login')
def add_to_wishlist(request, store_id):
    store = Store.objects.get(id=store_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, store=store)

    if created:
        # Store added to wishlist
        return JsonResponse({'message': 'added', 'store_id': store_id})
    else:
        # Item already in wishlist, return message
        return JsonResponse({'message': 'exists', 'store_id': store_id})

@login_required(login_url='/account/login')
def remove_from_wishlist(request, store_id):
    store = Store.objects.get(id=store_id)
    wishlist_item = Wishlist.objects.filter(user=request.user, store=store)

    if wishlist_item.exists():
        wishlist_item.delete()
        return JsonResponse({'message': 'removed', 'store_id': store_id})
    else:
        # Store not in wishlist
        return JsonResponse({'message': 'not_found', 'store_id': store_id})


def wishlist_view(request):
    wishlists = Wishlist.objects.filter(user=request.user)
    categories = Category.objects.all()  # Get all categories
    return render(request, 'wishlist.html', {'wishlists': wishlists, 'categories': categories})  # Pass categories to template

@login_required(login_url='/account/login')
def filter_by_category(request, category_id):
    categories = Category.objects.all()
    if (category_id == "all"):
        stores = Store.objects.all()
    else :
        stores = Store.objects.filter(categories__id=category_id)
    
    # Get the wishlist items based on the filtered stores
    wishlists = Wishlist.objects.filter(user=request.user, store__in=stores)
    
    return render(request, 'wishlist.html', {
        'wishlists': wishlists,
        'categories': categories,  
    })

