from django.shortcuts import render
from forum.models import Forum
from django.http import HttpResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags
from django.http import JsonResponse
from forum.forms import ForumEntryForm


# Create your views here.
def show_forum_page(request):
    return render(request, "forum_page.html", {})

def show_root_json(request) :
    data = Forum.objects.filter(parent__isnull=True)
    current_user = request.user
    forum_entries = []
    
    for forum_data in data:
        
        entry = {
            'pk':forum_data.pk,
            'fields':{
                'id': forum_data.user.id,
                'title': forum_data.title,
                'details': forum_data.details,
                'time': forum_data.time,  
                'username': forum_data.user.username,  
                'is_author': (current_user.id == forum_data.user.id),
            }
        }
        
        
            
        forum_entries.append(entry)

    # Return the data as JSON
    return JsonResponse(forum_entries, safe=False)

@csrf_exempt
@require_POST
def add_forum_entry_ajax(request):
    title = strip_tags(request.POST.get("title"))
    details = strip_tags(request.POST.get("details")) 
    parent = request.POST.get("parent")
    user = request.user
    new_forum = Forum(
        title=title, details=details,
        user=user,
    )
    new_forum.save()

    return HttpResponse(b"CREATED", status=201)

@csrf_exempt
@require_POST
def edit_forum(request): 
    forum = Forum.objects.get(pk=request.POST.get("pk"))
    print("successfully get forum")
    
    form = ForumEntryForm(request.POST or None, instance=forum)
    print("successfully get form")

    if form.is_valid() and request.method == "POST":
        
        if(request.user != forum.user) :
            return HttpResponse(b"Failed, unauthorized", status=401)
        
        form.save()
        return HttpResponse(b"EDITED", status=201)
    
    return HttpResponse(b"Failed", status=400)

@csrf_exempt
@require_POST
def delete_forum(request):
    forum = Forum.objects.get(pk = request.POST.get("pk"))
    # Hapus forum
    
    print (request.user, forum.user)
    if(request.user != forum.user) :
        return HttpResponse(b"Failed, unauthorized", status=401)
    
    forum.delete()
    return HttpResponse(b"DELETED", status=201) 