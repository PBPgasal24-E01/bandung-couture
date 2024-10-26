# from django.shortcuts import render, redirect, reverse, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.views.decorators.http import require_POST
# from .models import Promo, RedeemedPromo, HistoryPromo
# from .forms import PromoEntryForm
# from django.contrib import messages
# from django.utils import timezone
# from django.core import serializers
# from django.utils.html import strip_tags
# from django.db import IntegrityError
# from decimal import Decimal
# from django.utils.dateparse import parse_datetime

# @login_required(login_url='/account/login')
# def show_promo(request):
#     expired_promos = Promo.objects.filter(end_date__lt=timezone.now())
 
#     for promo in expired_promos:
#         HistoryPromo.objects.create(
#             title=promo.title,
#             description=promo.description,
#             discount_percentage=promo.discount_percentage,
#             promo_code=promo.promo_code,
#             start_date=promo.start_date,
#             end_date=promo.end_date,
#         )
#         promo.delete()  

#     promos = Promo.objects.all()
#     filter_option = request.GET.get('filter', '')
#     if filter_option == 'highest_discount':
#         promos = promos.order_by('-discount_percentage')
#     elif filter_option == 'nearest_time':
#         promos = promos.order_by('end_date')

#     user_role = request.user.role if request.user.is_authenticated else None

#     # If JSON is requested
#     if request.headers.get('Content-Type') == 'application/json':
#         promo_list = list(promos.values('id', 'title', 'discount_percentage', 'end_date'))
#         return JsonResponse({'status': True, 'promos': promo_list}, status=200)

#     # Otherwise, render HTML template
#     return render(request, 'show_promo.html', {
#         'promos': promos,
#         'user_role': user_role,
#         'filter': filter_option,
#     })



from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .models import Promo
from .forms import PromoEntryForm


@login_required(login_url='/account/login')
def show_promo(request, id=None):
    if id is not None:  # If an ID is provided, show the specific promo
        promo = get_object_or_404(Promo, pk=id)
        return render(request, 'show_promo.html', {'promo': promo})

    user_role = request.user.role if request.user.is_authenticated else None 

    if user_role == 1:  # Visitor
        # Fetch all promos for visitors
        promos = Promo.objects.all()
    elif user_role == 2:  # Contributor
        # Fetch promos created by the logged-in user
        promos = Promo.objects.filter(created_by=request.user)
    else:
        promos = Promo.objects.none()  # No promos to show

    # Prepare messages to display
    success_message = request.session.pop('success_message', None)
    error_message = request.session.pop('error_message', None)

    return render(request, 'show_promo.html', {
        'promos': promos,
        'user_role': user_role,
        'success_message': success_message,
        'error_message': error_message,
    })

@require_POST 
@csrf_exempt
def create_promo(request):
    if request.method == 'POST':
        form = PromoEntryForm(request.POST)
        if form.is_valid():
            promo = form.save(commit=False)
            promo.created_by = request.user  
            promo.save()
            request.session['success_message'] = 'Promo created successfully!'
            return JsonResponse({'status': 'success', 'promo_id': promo.id})
        else:
            request.session['error_message'] = form.errors 
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
   
@csrf_exempt
def update_promo(request, id):
    promo = get_object_or_404(Promo, pk=id)
    if request.method == "POST":
        form = PromoEntryForm(request.POST, instance=promo)
        if form.is_valid():
            form.save()
            request.session['success_message'] = 'Promo updated successfully!' 
            return JsonResponse({'success': True})
        else:
            request.session['error_message'] = form.errors
            return JsonResponse({'success': False, 'errors': form.errors})

def get_promo(request, id):
    if request.method == 'GET':
        promo = get_object_or_404(Promo, pk=id)  # Ensure you're using the correct primary key
        data = {
            'id': promo.id,
            'title': promo.title,
            'description': promo.description,
            'discount_percentage': promo.discount_percentage,
            'promo_code': promo.promo_code,
            'start_date': promo.start_date,
            'end_date': promo.end_date,
        }
        return JsonResponse(data)

@csrf_exempt
def delete_promo(request, id):
    promo = get_object_or_404(Promo, pk=id)
    promo.delete()
    request.session['success_message'] = 'Promo deleted successfully!' 
    return JsonResponse({'success': True})
