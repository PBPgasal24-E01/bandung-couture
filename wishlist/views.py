from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from wishlist.models import Wishlist
from stores.models import Store,Category
from django.http import HttpResponse, JsonResponse
from django.core import serializers

@login_required(login_url='/account/login')
def wishlist_view(request):
    return render(request, 'wishlist.html', {
        'categories': Category.objects.all()
    })

@require_GET
def wishlist_view_mobile(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize('json', wishlist_items), content_type='application/json')

def fetch_reccomended (request) :
    wishlist_items = Wishlist.objects.filter(user=request.user)
    wishlisted_store_ids = wishlist_items.values_list('store__id', flat=True)
    non_wishlist_stores = Store.objects.exclude(id__in=wishlisted_store_ids)
    recommended_stores = non_wishlist_stores.order_by('?')[:2]
    return recommended_stores

@login_required(login_url='/account/login')
def recommened_wishlist(request):
    recommended_stores = fetch_reccomended(request)
    return render(request, 'recommended.html', {
        'recommended_stores': recommended_stores
    })

@require_GET
def recommended_wishlist_mobile(request):
    recommended_stores = fetch_reccomended(request)
    return HttpResponse(serializers.serialize('json', recommended_stores), content_type='application/json')


def add_to_wishlist(request, store_id):
    store = Store.objects.get(id=store_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, store=store)

    if created:
        # Store added to wishlist
        return JsonResponse({'message': 'added', 'store_id': store_id})
    else:
        # Item already in wishlist, return message
        return JsonResponse({'message': 'exists', 'store_id': store_id})
    

def remove_from_wishlist(request, store_id):
    store = Store.objects.get(id=store_id)
    wishlist_item = Wishlist.objects.filter(user=request.user, store=store)

    if wishlist_item.exists():
        wishlist_item.delete()
        return JsonResponse({'message': 'removed', 'store_id': store_id})
    else:
        # Store not in wishlist
        return JsonResponse({'message': 'not_found', 'store_id': store_id})

def remove_mobile(request, pk):  # Hanya izinkan HTTP DELETE
    try:
        # Ambil item wishlist berdasarkan pk dan user yang sedang login
        wishlist_item = get_object_or_404(Wishlist, pk=pk, user=request.user)

        # Hapus item dari wishlist
        wishlist_item.delete()

        # Kembalikan respons sukses
        return JsonResponse({"status": "success", "message": "Item removed from wishlist."})
    except Exception as e:
        # Tangani error, misalnya pk tidak ditemukan
        return JsonResponse({"status": "error", "message": str(e)}, status=400)

@login_required(login_url='/account/login')
def filter_by_category(request, category_id):
    categories = Category.objects.all()
    if (category_id == "all"):
        stores = Store.objects.all()
    else :
        stores = Store.objects.filter(categories__id=category_id)
    # Get the wishlist items based on the filtered stores
    wishlists = Wishlist.objects.filter(user=request.user, store__in=stores)
    
    return render(request, 'products.html', {
        'wishlists': wishlists
    })


