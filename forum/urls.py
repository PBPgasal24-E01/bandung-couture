from django.urls import path
from forum.views import show_forum_page, show_root_json, add_forum_entry_ajax
from django.shortcuts import redirect

app_name = 'forum'

urlpatterns = [
    path('', lambda request: redirect('forum:show'), name='default'),
    path('show', show_forum_page, name='show'),
    path('show_root_json', show_root_json, name='show_root_json'),
    path('add_forum_entry_ajax', add_forum_entry_ajax, name='add_forum_entry_ajax'),
]
