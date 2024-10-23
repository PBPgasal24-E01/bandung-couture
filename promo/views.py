from django.shortcuts import render, redirect, reverse,  get_object_or_404
from .models import Promo, RedeemedPromo
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .forms import PromoEntryForm
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

@login_required(login_url='/account/login')
def show_promo(request):
    now = timezone.now()
    promos = Promo.objects.filter(
        is_active = True, start_date__lte = now, end_date__gte = now
    ).order_by('-discount_percentage', 'start_date')
    
    user_role = request.user.role if request.user.is_authenticated else None  

    return render(request, 'show_promo.html', { 
        'promos': promos,
        'user_role' : user_role
        
    })


def create_promo(request):
    if request.method == 'POST':
        form = PromoEntryForm(request.POST)
        if form.is_valid():
            promo = form.save(commit=False)
            promo.created_by = request.user
            promo.save()
            return HttpResponseRedirect(reverse('promo:show_promo'))
    else:
        form = PromoEntryForm()
    return render(request, 'create_promo.html', {'form': form})

def update_promo(request, id):
    promos = Promo.objects.get(pk=id)
    form = PromoEntryForm(request.POST or None, instance=promos)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('promo:show_promo'))
    return render(request, "update_promo.html", {'form': form})












def delete_promo(request, id):
    promos = Promo.objects.get(pk=id)  
    promos.delete()
    return HttpResponseRedirect(reverse('promo:show_promo'))

def delete_promo_cookie(request):
    response = HttpResponseRedirect('/rewards-promo/')
    response.delete_cookie('promo_visited')  
    return response

def redeem_promo(request, promo_id):
    promo = get_object_or_404(Promo, id=promo_id)
    already_redeemed = RedeemedPromo.objects.filter(user=request.user, promo=promo).exists()

    if already_redeemed:
        messages.error(request, "Kamu sudah mereedem kupon ini sebelumnya.")
    else:
        RedeemedPromo.objects.create(user=request.user, promo=promo)
        messages.success(request, "Kupon berhasil diredeem!")

    return redirect('promo:show_promo')

def rewards_promo_view(request):
    redeemed_count = RedeemedPromo.objects.filter(user=request.user).count()
    streak = min(redeemed_count, 5)
    remaining_for_next_streak = max(5 - streak, 0)
    promo_visited = 'promo_visited' in request.COOKIES
    response = render(request, 'rewards_promo.html', {
        'streak': streak,
        'redeemed_kupons': RedeemedPromo.objects.filter(user=request.user),
        'remaining_for_next_streak': remaining_for_next_streak,
        'promo_visited': promo_visited
    })
    if not promo_visited:
        response.set_cookie('promo_visited', 'yes', max_age=60*60*24*7)

    return response

def history_promo_view(request):
    user_promos = Promo.objects.filter(created_by=request.user)
    total_redeemed = RedeemedPromo.objects.filter(promo__created_by=request.user).count()

    context = {
        'user_promos': user_promos,
        'total_redeemed': total_redeemed,
        'current_time': timezone.now(),  
    }
    return render(request, 'history_promo.html', context)

def get_total_redeemed(request):
    total_redeemed = RedeemedPromo.objects.filter(promo__created_by=request.user).count()
    return JsonResponse({'total_redeemed': total_redeemed})