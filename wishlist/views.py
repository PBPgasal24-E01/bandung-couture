from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from wishlist.models import Wishlist
from stores.models import Store
from django.http import JsonResponse

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


@login_required(login_url='/account/login')
def wishlist_view(request):
    wishlists = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'wishlists': wishlists})

