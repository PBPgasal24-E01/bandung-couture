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
    if id is not None: 
        promo = get_object_or_404(Promo, pk=id)
        return render(request, 'show_promo.html', {'promo': promo})

    user_role = request.user.role if request.user.is_authenticated else None 

    if user_role == 1: 
        promos = Promo.objects.all()
    elif user_role == 2:  
        promos = Promo.objects.filter(created_by=request.user)
    else:
        promos = Promo.objects.none()
        
    return render(request, 'show_promo.html', {
        'promos': promos,
        'user_role': user_role,
   
    })

@login_required(login_url='/account/login')
def filter_promos(request):
    filter_type = request.GET.get('filter', '')
    promos = Promo.objects.all()  

    if filter_type == 'highest-discount':
        promos = promos.order_by('-discount_percentage') 
    elif filter_type == 'nearest-end':
        promos = promos.order_by('end_date')  

    promo_list = [{
        'id': promo.id,
        'title': promo.title,
        'description': promo.description,
        'discount_percentage': promo.discount_percentage,
        'promo_code': promo.promo_code,
        'start_date': promo.start_date.strftime('%Y-%m-%d'),         
        'end_date': promo.end_date.strftime('%Y-%m-%d'),  
    } for promo in promos]

    return JsonResponse({'promos': promo_list})

@login_required(login_url='/account/login')
@require_POST 
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
   
@login_required(login_url='/account/login')
@require_POST
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

@login_required(login_url='/account/login')
def get_promo(request, id):
    if request.method == 'GET':
        promo = get_object_or_404(Promo, pk=id)  


        start_date = promo.start_date.strftime('%Y-%m-%dT%H:%M')
        end_date = promo.end_date.strftime('%Y-%m-%dT%H:%M')

        data = {
            'id': promo.id,
            'title': promo.title,
            'description': promo.description,
            'discount_percentage': promo.discount_percentage,
            'promo_code': promo.promo_code,
            'start_date': start_date, 
            'end_date': end_date,     

        }
        return JsonResponse(data)

@login_required(login_url='/account/login')
def delete_promo(request, id):
    promo = get_object_or_404(Promo, pk=id)
    promo.delete()
    request.session['success_message'] = 'Promo deleted successfully!' 
    return JsonResponse({'success': True})
