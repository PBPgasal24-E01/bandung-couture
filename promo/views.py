from django.shortcuts import render, redirect, reverse,  get_object_or_404
from .models import Promo, RedeemedPromo, HistoryPromo
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .forms import PromoEntryForm
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone


@login_required(login_url='/login')
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

    return render(request, 'show_promo.html', { 
        'promos': promos,
        'user_role': user_role,
        'filter': filter_option, 
    })


def create_promo(request):
    if request.method == 'POST':
        form = PromoEntryForm(request.POST)
        if form.is_valid():
            promo = form.save(commit=False)
            promo.created_by = request.user  # Menetapkan pengguna yang membuat promo
            promo.save()  # Simpan objek promo
            return HttpResponseRedirect(reverse('promo:show_promo'))  # Redirect ke halaman promo
    else:
        form = PromoEntryForm()  # Buat instance form baru jika bukan POST

    return render(request, 'create_promo.html', {'form': form})

def update_promo(request, id):
    promo = get_object_or_404(Promo, pk=id)  # Mengambil promo dengan ID yang diberikan
    form = PromoEntryForm(request.POST or None, instance=promo)  # Mengisi form dengan data yang ada

    if request.method == "POST":
        if form.is_valid():  # Validasi form
            form.save()  # Simpan perubahan ke promo
            return HttpResponseRedirect(reverse('promo:show_promo'))  # Redirect ke halaman promo
        else:
            # Jika form tidak valid, akan kembali ke halaman update dengan error
            # Form sudah menangani kesalahan validasi, jadi tidak perlu penanganan tambahan di sini
            pass

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

def get_total_redeemed(request):
    total_redeemed = RedeemedPromo.objects.filter(promo__created_by=request.user).count()
    return JsonResponse({'total_redeemed': total_redeemed})

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
    total_redeemed = RedeemedPromo.objects.filter(promo__created_by=request.user).count()
    user_history = HistoryPromo.objects.all()
    context = {
        'user_history': user_history,
        'total_redeemed': total_redeemed,
        'current_time': timezone.now(),  
    }
    return render(request, 'history_promo.html', context)

def delete_history(request, history_id):
    # Ambil riwayat promo yang akan dihapus
    history = get_object_or_404(HistoryPromo, id=history_id)
    history.delete()
    return redirect('promo:history_promo')  # Ganti dengan nama URL yang sesuai

