from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseNotAllowed
from testimony.models import Testimony
from stores.models import Store
from account.models import User
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
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
            "pk": item.pk,
            "user": item.userId.username,
            "testimony": item.testimony,  # Add other attributes as needed
            "rating": (str(item.rating) if item.rating else 0)
        })

    return JsonResponse(data_new, safe=False)

def get_merchant_rating(request, id):
    testimonies = Testimony.objects.filter(storeId__pk=id)
    num = 0
    for testimony in testimonies:
        num += testimony.rating

    data = {"rating": 0}
    if(len(testimonies) != 0):
        data = {
            "rating": num / len(testimonies)
        }

    return JsonResponse(data, safe=False)

def get_number_of_rating(request, id):
    testimonies = Testimony.objects.filter(storeId__pk=id)
    num = 0
    for testimony in testimonies:
        num += testimony.rating

    data = {
        "rating": 0,
        "count": len(testimonies)
    }

    if(len(testimonies) != 0):
        data = {
            "rating": num / len(testimonies),
            "count": len(testimonies)
        }

    return JsonResponse(data, safe=False)

def exist_testimony_in_store(request, id):
    testimonies = Testimony.objects.filter(storeId__pk=id)
    
    exist = False
    testimony = ""
    rating = 0
    pk = 0
    user = ""

    for item in testimonies:
        if(item.userId == request.user):
            exist = True
            user = item.userId
            testimony = item.testimony
            rating = item.rating
            pk = item.pk

    print(exist, testimony) 
    return JsonResponse({"status": exist, "testimony": testimony, "rating": rating, "pk": pk, "user": (user.username if user != "" else "") }, safe=False) 

def get_all_testimony_by_id(request):
    user_testimony = Testimony.objects.filter(userId=request.user)
    testimony_store = []
    for item in user_testimony:
        testimony_store.append(item.storeId.pk)

    store = Store.objects.filter(pk__in=testimony_store)

    response = []
    for item in store:
        response.append({
            "pk": item.pk,
            "user": item.user, 
            "brand": item.brand,
            "description" : item.description,
            "address": item.address,
            "contact_number": item.contact_number,
            "website": item.contact_number,
            "social_media": item.social_media
        })

    return JsonResponse(response, safe=False)
    
def get_all_store(request):
    store = Store.objects.all()

    response = []
    for item in store:
        response.append({
            "pk": item.pk,
            "user": item.user, 
            "brand": item.brand,
            "description" : item.description,
            "address": item.address,
            "contact_number": item.contact_number,
            "website": item.contact_number,
            "social_media": item.social_media
        })

    return JsonResponse(response, safe=False)

@require_POST
@csrf_exempt
def edit_testimony_flutter(request):
    data = json.loads(request.body)

    testimony = data["testimony"]
    rating = data["rating"]
    pk = data["pk"]
    
    if(not 0 < float(rating) <= 5):
        return JsonResponse({
            "status": False,
            "message": "Angka tidak valid."
        }, status=400)

    current_testimony = Testimony.objects.get(pk=int(pk))

    current_testimony.testimony = testimony
    current_testimony.rating = int(rating)

    current_testimony.save()
    
    return JsonResponse({
            "status": 'success',
            "message": "Testimony berhasil di ubah!"
        }, status=200)


@require_POST
@csrf_exempt
def add_testimony_flutter(request):
    data = json.loads(request.body)

    testimony = data["testimony"]
    rating = data["rating"]
    storeId = data["store_id"]
    store = Store.objects.get(pk=storeId)  # Fetch the Store instance
    
    user = request.user
    
    if(not 0 < float(rating) <= 5):
        return JsonResponse({
            "status": False,
            "message": "Angka tidak valid."
        }, status=400)
    
    payload = Testimony(
        testimony=testimony, 
        rating=rating,
        userId=user,
        storeId=store
    )

    payload.save()
    return JsonResponse({
            "username": user.username,
            "status": 'success',
            "message": "Testimoni berhasil dibuat!"
        }, status=200)

@csrf_exempt
def delete_testimony_flutter(request, id):
    try:
        # Retrieve and delete the Testimony object
        testimony = Testimony.objects.get(pk=id)
        testimony.delete()
        return JsonResponse({
            "status": 'success',
            "message": "Testimoni berhasil dibuat!"
        }, status=200)
    except Testimony.DoesNotExist:
            return JsonResponse({
                    "status": 'failed',
                    "message": "Tidak ada testimoni dengan id ini!"
                }, status=404)
    except Exception as e:
            return JsonResponse({
                    "status": 'failed',
                    "message": f"Terjadi error: {str(e)}"
                }, status=500)



@require_POST
@login_required(login_url='/account/login')
@csrf_exempt
def create_new_testimony(request):
    testimony = request.POST.get("testimony")
    rating = request.POST.get("rating")
    storeId = request.POST.get("store_id")
    store = Store.objects.get(pk=storeId)  # Fetch the Store instance
    user = request.user

    if(not 0 < float(rating) <= 5):
        return HttpResponse(b"FAILED", status=400)

    payload = Testimony(
        testimony=testimony, 
        rating=rating,
        userId=user,
        storeId=store
    )

    payload.save()
    return HttpResponse(b"CREATED", status=201)

@login_required(login_url='/account/login')
@csrf_exempt
def delete_testimony(request, id):
    if request.method == "DELETE":
        try:
            # Retrieve and delete the Testimony object
            testimony = Testimony.objects.get(pk = id)
            testimony.delete()
            return JsonResponse({"message": "Testimony deleted successfully"}, status=200)
        except Testimony.DoesNotExist:
            # Return a 404 if the object does not exist
            return JsonResponse({"error": "Testimony not found"}, status=404)
        except Exception as e:
            # Handle any unexpected errors
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)
    else:
        return HttpResponseNotAllowed(["DELETE"])
