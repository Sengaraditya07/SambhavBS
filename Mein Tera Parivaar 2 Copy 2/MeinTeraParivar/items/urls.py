from django.urls import path
from .views import public_item_list, add_item, my_items_list, unlist_item
from moderation.views import item_detail

urlpatterns = [
    path('', public_item_list, name='public_items'),
    path('add/', add_item, name='add_item'),
    path('<int:pk>/', item_detail, name='item_detail'),
    path('myitemslist/', my_items_list, name='my_items_list'),
    path('unlist/<int:pk>/', unlist_item, name='unlist_item'),
]
