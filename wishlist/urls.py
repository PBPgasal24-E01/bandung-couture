from django.urls import path
from wishlist.views import add_to_wishlist,remove_from_wishlist,wishlist_view,filter_by_category,recommened_wishlist,wishlist_view_mobile,recommended_wishlist_mobile,is_in_wishlist,remove_mobile

app_name = 'wishlist'

urlpatterns = [
    path('', wishlist_view, name='view'),
    path('view_Mob/', wishlist_view_mobile, name='view_Mob' ),
    path('add/<int:store_id>/', add_to_wishlist, name='add'),
    path('remove/<int:store_id>/', remove_from_wishlist, name='remove'),
    path("remove_mob/<int:pk>/", remove_mobile, name="remove_mob"),
    path('filter/<str:category_id>/', filter_by_category, name='filter'),
    path('recommended_wishlist/', recommened_wishlist, name='recommended_wishlist'),
    path('recommended_Mob/', recommended_wishlist_mobile, name='recommended_Mob'),
    path('check/<int:store_id>/', is_in_wishlist, name='is_in_wishlist')
]