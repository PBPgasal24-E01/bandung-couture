from django.urls import path
from wishlist.views import add_to_wishlist,remove_from_wishlist,wishlist_view,filter_by_category

app_name = 'wishlist'

urlpatterns = [
    path('', wishlist_view, name='view'),
    path('add/<int:store_id>/', add_to_wishlist, name='add'),
    path('remove/<int:store_id>/', remove_from_wishlist, name='remove'),
    path('filter/<str:category_id>/', filter_by_category, name='filter')
]
