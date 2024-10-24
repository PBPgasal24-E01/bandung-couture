from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from testimony.models import Testimony
from stores.models import Store
from account.models import User
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.core import serializers
import json
# Create your views here.
def show_testimony_by_merchant(request, id):
    store = Store.objects.get(pk=id) 
    context = {
        'store': store
    }    
    return render(request, "show_testimony.html", context)

def show_testimony_by_merchant_json(request, id):
    data = Testimony.objects.filter(storeId__pk=id)

    data_new = []
    for item in data:
        # Construct a dictionary from the model instance
        data_new.append({
            "user": item.userId.username,
            "testimony": item.testimony,  # Add other attributes as needed
            "rating": (str(item.rating) if item.rating else 0) ,
        })
    print(data_new)

    return JsonResponse(data_new, safe=False)


@require_POST
@csrf_exempt
def create_new_testimony(request):
    testimony = request.POST.get("testimony")
    rating = request.POST.get("rating")
    storeId = request.POST.get("store_id")
    store = Store.objects.get(pk=storeId)  # Fetch the Store instance
    user = request.user

    payload = Testimony(
        testimony=testimony, 
        rating=rating,
        userId=user,
        storeId=store
    )

    payload.save()
    return HttpResponse(b"CREATED", status=201)
