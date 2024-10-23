from django.urls import path
from forum.views import show_forum_page, show_root_json, add_forum_entry_ajax, edit_forum, delete_forum, show_forum_page_id, show_json_by_id, show_json_childs_by_id, show_json
from django.shortcuts import redirect

app_name = 'forum'

urlpatterns = [
    path('', lambda request: redirect('forum:show'), name='default'),
    path('show/', show_forum_page, name='show'),
    path('show/<uuid:id>/', show_forum_page_id, name='show_id'),
    path('show_root_json/', show_root_json, name='show_root_json'),
    path('show_json/', show_json, name='show_json'),
    path('show_json_by_id/<uuid:id>/', show_json_by_id, name='show_json_by_id'),
    path('show_json_childs_by_id/<uuid:id>/', show_json_childs_by_id, name='show_json_childs_by_id'),
    path('add_forum_entry_ajax/', add_forum_entry_ajax, name='add_forum_entry_ajax'),
    path('edit_forum/', edit_forum, name="edit_forum"),
    path('delete_forum/', delete_forum, name="delete_forum"),
]
