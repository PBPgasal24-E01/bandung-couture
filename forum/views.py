from django.shortcuts import render
from forum.models import Forum
from django.http import HttpResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags


# Create your views here.
def show_forum_page(request):
    return render(request, "forum_page.html", {})

def show_root_json(request) :
    data = Forum.objects.filter(parent__isnull=True)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@csrf_exempt
@require_POST
def add_forum_entry_ajax(request):
    title = strip_tags(request.POST.get("title")) # strip HTML tags!
    details = strip_tags(request.POST.get("details")) # strip HTML tags!
    parent = request.POST.get("parent")
    user = request.user
    new_forum = Forum(
        title=title, details=details,
        user=user
    )
    new_forum.save()

    return HttpResponse(b"CREATED", status=201)