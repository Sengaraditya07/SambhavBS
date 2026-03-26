from django.urls import path
from .views import signup, dashboard, custom_logout, custom_login, home

urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup, name='signup'),
    path('dashboard/', dashboard, name='dashboard'),
    path('logout/', custom_logout, name='logout'),
    path('accounts/login/', custom_login, name='login'),
]
