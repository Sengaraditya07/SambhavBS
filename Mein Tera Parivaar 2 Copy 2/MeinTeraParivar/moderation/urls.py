from django.urls import path
from . import views

urlpatterns = [
    path('my-requests/', views.my_requests, name='my_requests'),
    path('incoming-requests/', views.incoming_requests, name='incoming_requests'),
    path('accepted-requests/', views.accepted_requests, name='accepted_requests'),
    path('accept-request/<int:pk>/', views.accept_request, name='accept_request'),
    path('reject-request/<int:pk>/', views.reject_request, name='reject_request'),
]
