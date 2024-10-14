from django.shortcuts import render, redirect, reverse
from .models import Promo
from .forms import PromoEntryForm
from django.http import HttpResponseRedirect

def show_promo(request):
    promos = Promo.objects.all() 
    return render(request, 'show_promo.html', {'promos': promos})

def create_promo(request):
    if request.method == 'POST':
        form = PromoEntryForm(request.POST)
        if form.is_valid():
            form.save()
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
    promos = Promo.objects.get(pk=id)  #
    promos.delete()
    return HttpResponseRedirect(reverse('promo:show_promo'))
