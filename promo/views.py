from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Promo, RedeemedPromo, HistoryPromo
from .forms import PromoEntryForm
from django.contrib import messages
from django.utils import timezone
from django.core import serializers

@login_required(login_url='/account/login')
def show_promo(request):
    expired_promos = Promo.objects.filter(end_date__lt=timezone.now())
 
    for promo in expired_promos:
        HistoryPromo.objects.create(
            title=promo.title,
            description=promo.description,
            discount_percentage=promo.discount_percentage,
            promo_code=promo.promo_code,
            start_date=promo.start_date,
            end_date=promo.end_date,
        )
        promo.delete()  

    promos = Promo.objects.all()
    filter_option = request.GET.get('filter', '')
    if filter_option == 'highest_discount':
        promos = promos.order_by('-discount_percentage')
    elif filter_option == 'nearest_time':
        promos = promos.order_by('end_date')

    user_role = request.user.role if request.user.is_authenticated else None

    # If JSON is requested
    if request.headers.get('Content-Type') == 'application/json':
        promo_list = list(promos.values('id', 'title', 'discount_percentage', 'end_date'))
        return JsonResponse({'status': True, 'promos': promo_list}, status=200)

    # Otherwise, render HTML template
    return render(request, 'show_promo.html', {
        'promos': promos,
        'user_role': user_role,
        'filter': filter_option,
    })

@csrf_exempt
@require_POST
def create_promo(request):
    title = request.POST.get("title")
    description = request.POST.get("description")
    discount_percentage = request.POST.get("discount_percentage")
    promo_code = request.POST.get("promo_code")
    start_date = request.POST.get("start_date")
    end_date = request.POST.get("end_date")
    user = request.user

    new_promo = Promo(
        title=title, description=description,
        discount_percentage=discount_percentage,
        promo_code=promo_code,
        start_date=start_date,
        end_date=end_date,
        created_by=user
    )
    new_promo.save()

    return JsonResponse({
        'status': 'success',
        'message': 'Promo created successfully!',
        'promo': {
            'id': new_promo.id,
            'title': new_promo.title,
            'discount_percentage': new_promo.discount_percentage,
            'end_date': new_promo.end_date.strftime('%Y-%m-%d')
        }
    }, status=201)

@csrf_exempt
@require_POST
def update_promo(request, id):
    promo = get_object_or_404(Promo, pk=id)
    title = request.POST.get("title")
    description = request.POST.get("description")
    discount_percentage = request.POST.get("discount_percentage")
    promo_code = request.POST.get("promo_code")
    end_date = request.POST.get("end_date")

    promo.title = title
    promo.description = description
    promo.discount_percentage = discount_percentage
    promo.promo_code = promo_code
    promo.end_date = end_date
    promo.save()

    return JsonResponse({
        'status': 'success',
        'message': 'Promo updated successfully!',
        'promo': {
            'id': promo.id,
            'title': promo.title,
            'discount_percentage': promo.discount_percentage,
            'end_date': promo.end_date.strftime('%Y-%m-%d')
        }
    }, status=200)

def show_json(request):
    data = Promo.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def delete_promo(request, id):
    promo = get_object_or_404(Promo, pk=id)
    promo.delete()
    
    # JSON response for deletion
    if request.headers.get('Content-Type') == 'application/json':
        return JsonResponse({'status': True, 'message': 'Promo deleted successfully!'}, status=200)

    return HttpResponseRedirect(reverse('promo:show_promo'))

def redeem_promo(request, promo_id):
    promo = get_object_or_404(Promo, id=promo_id)
    already_redeemed = RedeemedPromo.objects.filter(user=request.user, promo=promo).exists()

    if already_redeemed:
        message = "Kamu sudah mereedem kupon ini sebelumnya."
        messages.error(request, message)
        
        if request.headers.get('Content-Type') == 'application/json':
            return JsonResponse({'status': False, 'message': message}, status=403)
    else:
        RedeemedPromo.objects.create(user=request.user, promo=promo)
        message = "Kupon berhasil diredeem!"
        messages.success(request, message)
        
        if request.headers.get('Content-Type') == 'application/json':
            return JsonResponse({'status': True, 'message': message}, status=200)

    return redirect('promo:show_promo')

def get_total_redeemed(request):
    total_redeemed = RedeemedPromo.objects.filter(promo__created_by=request.user).count()
    return JsonResponse({'total_redeemed': total_redeemed})

@csrf_exempt
def rewards_promo_ajax(request):
    if request.method == "GET":
        redeemed_count = RedeemedPromo.objects.filter(user=request.user).count()
        streak = min(redeemed_count, 5)
        remaining_for_next_streak = max(5 - streak, 0)

        return JsonResponse({
            'status': 'success',
            'streak': streak,
            'remaining_for_next_streak': remaining_for_next_streak,
        }, status=200)

@csrf_exempt
def history_promo_ajax(request):
    if request.method == "GET":
        user_history = HistoryPromo.objects.filter(user=request.user)
        history_list = list(user_history.values())
        total_redeemed = RedeemedPromo.objects.filter(promo__created_by=request.user).count()

        return JsonResponse({
            'status': 'success',
            'history': history_list,
            'total_redeemed': total_redeemed,
        }, status=200)

def delete_history(request, history_id):
    history = get_object_or_404(HistoryPromo, id=history_id)
    history.delete()

    return redirect('promo:history_promo')
