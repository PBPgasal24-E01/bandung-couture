from django.shortcuts import render, redirect
from forum.models import Forum
from django.http import HttpResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags
import json
from django.http import JsonResponse
from forum.forms import ForumEntryForm
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.utils.timezone import now


# Create your views here.
@login_required(login_url='/account/login')
def show_forum_page(request):
    return render(request, "forum_page.html", {"id_not_found": False})

@login_required(login_url='/account/login')
def show_forum_page_id(request,id):
    try :
        forum_data = Forum.objects.get(pk=id)
    except : 
        return render(request, "forum_page.html", {"id_not_found": True})
    
    context = {
        'pk': id
    }
    return render(request, "forum_page_id.html", context)

# show all
def show_json(request):
    data = Forum.objects.all().order_by("-time")
    current_user = request.user
    forum_entries = []
    
    for forum_data in data:
        if( forum_data.parent == None) :
            parent = "None"
        else :
            parent = forum_data.parent.id
        entry = {
            'pk':forum_data.pk,
            'fields':{
                'id': forum_data.user.id,
                'title': forum_data.title,
                'details': forum_data.details,
                'time': time_since(forum_data.time),  
                'username': forum_data.user.username,  
                'parent': parent,
                'is_author': (current_user.id == forum_data.user.id),
            }
        }
        
        forum_entries.append(entry)

    # Return the data as JSON
    return JsonResponse(forum_entries, safe=False, status=200)

def show_json_raw(request) :
    data = Forum.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")


# only show the id's data
def show_json_by_id(request,id) :
    try :
        forum_data = Forum.objects.get(pk=id)
    except : 
        return HttpResponse("NOT FOUND", status=404)
    current_user = request.user
    
    entry = {
        'pk':forum_data.pk,
        'fields':{
            'id': forum_data.user.id,
            'title': forum_data.title,
            'details': forum_data.details,
            'time': time_since(forum_data.time),  
            'username': forum_data.user.username,  
            'parent': "None",
            'is_author': (current_user.id == forum_data.user.id),
        }
    }

    return JsonResponse(entry, safe=False, status=200)

# only show the id's childs
def show_json_childs_by_id(request,id) :
    data = Forum.objects.filter(parent=id)
    current_user = request.user
    forum_entries = []
    
    for forum_data in data:
        
        entry = {
            'pk':forum_data.pk,
            'fields':{
                'id': forum_data.user.id,
                'title': forum_data.title,
                'details': forum_data.details,
                'time': time_since(forum_data.time),  
                'username': forum_data.user.username,  
                'is_author': (current_user.id == forum_data.user.id),
            }
        }
        
        forum_entries.append(entry)

    return JsonResponse(forum_entries, safe=False, status=200)

# only show root
def show_root_json(request) :
    data = Forum.objects.filter(parent__isnull=True).order_by("-time")
    current_user = request.user
    forum_entries = []
    
    for forum_data in data:
        
        entry = {
            'pk':forum_data.pk,
            'fields':{
                'id': forum_data.user.id,
                'title': forum_data.title,
                'details': forum_data.details,
                'time': time_since(forum_data.time),  
                'username': forum_data.user.username,  
                'is_author': (current_user.id == forum_data.user.id),
            }
        }
        
        forum_entries.append(entry)

    return JsonResponse(forum_entries, safe=False, status=200)

# filtered for the user logged in
def show_root_json_filter_user(request) :
    data = Forum.objects.filter(parent__isnull=True, user=request.user).order_by("-time")
    current_user = request.user
    forum_entries = []
    
    for forum_data in data:
        
        entry = {
            'pk':forum_data.pk,
            'fields':{
                'id': forum_data.user.id,
                'title': forum_data.title,
                'details': forum_data.details,
                'time': time_since(forum_data.time),  
                'username': forum_data.user.username,  
                'is_author': (current_user.id == forum_data.user.id),
            }
        }
        
        forum_entries.append(entry)

    return JsonResponse(forum_entries, safe=False, status=200)

@require_POST
@login_required(login_url='/account/login')
def add_forum_entry_ajax(request):
    title = strip_tags(request.POST.get("title"))
    details = strip_tags(request.POST.get("details")) 

    parentpk = request.POST.get("parent")
     
    user = request.user
    
    if(parentpk != None) :
        try :
            parent = Forum.objects.get(pk=parentpk)
        except : 
            return HttpResponse(b"NOT FOUND", status=404)
        new_forum = Forum(
            title=title, details=details,
            user=user,
            parent=parent
        )
        new_forum.save()
    else : 
        new_forum = Forum(
            title=title, details=details,
            user=user,
        )
        new_forum.save()
    return HttpResponse(b"CREATED", status=201)

@csrf_exempt
def add_flutter(request):
    if request.method == 'POST':

        data = json.loads(request.body)
        
        if data["parent"] == None :
            parent = None
        else :
            parent = Forum.objects.get(pk=data["parent"])
        new_data = Forum.objects.create(
            user=request.user,
            title=data["title"],
            details=data["details"],
            parent=parent
        )

        new_data.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)

@require_POST
@login_required(login_url='/account/login')
def edit_forum(request):
    try :
        forum = Forum.objects.get(pk=request.POST.get("pk"))
    except :
        return HttpResponse(b"NOT FOUND", status=404)
    form = ForumEntryForm(request.POST or None, instance=forum)

    if(request.user != forum.user) :
        return HttpResponse(b"Failed, unauthorized", status=401)
    
    form.save()
    return HttpResponse(b"EDITED", status=201)

@csrf_exempt
def edit_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        try : 
            forum = Forum.objects.get(pk = data['pk'])
        except : 
            return JsonResponse({"status": "error"}, status=404)
        
        if(request.user != forum.user) :
            return HttpResponse(b"Failed, unauthorized", status=401)
        
        form = ForumEntryForm(data or None, instance=forum)
        form.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)
        

@require_POST
@login_required(login_url='/account/login')
def delete_forum(request):
    try :
        forum = Forum.objects.get(pk = request.POST.get("pk"))
    except :
        return HttpResponse(b"NOT FOUND", status=404)
    
    
    if(request.user != forum.user) :
        return HttpResponse(b"Failed, unauthorized", status=401)
    
    forum.delete()
    return HttpResponse(b"DELETED", status=201) 

@csrf_exempt 
def delete_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        try : 
            forum = Forum.objects.get(pk = data['pk'])
        except : 
            return JsonResponse({"status": "error"}, status=404)
        
        if(request.user != forum.user) :
            return HttpResponse(b"Failed, unauthorized", status=401)
        
        forum.delete()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)
        


def time_since(time):
    delta = now() - time

    if delta < timedelta(hours=1):
        return "recent"
    elif delta < timedelta(days=1):
        hours = delta.seconds // 3600
        return f"{hours}h ago"
    else:
        days = delta.days
        return f"{days}d ago"
    
    
