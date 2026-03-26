from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout, login as auth_login, authenticate
from django.views.decorators.cache import never_cache
from django.contrib import messages
from .forms import SignupForm
from items.models import Item
from django.contrib.auth import get_user_model

from moderation.models import Request

User = get_user_model()

def home(request):
    return render(request, 'home.html')

def custom_login(request):
    """Custom login view with phone and password authentication."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        
        user = authenticate(request, username=phone, password=password)
        
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Logout successful!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid phone number or password.')
    
    return render(request, 'registration/login.html')


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.first_name = form.cleaned_data['name']
            user.is_active = True
            user.save()
            messages.success(request, 'Account created successfully! Please login.')
            return redirect('login')
    else:
        form = SignupForm()

    return render(request, 'registration/signup.html', {'form': form})


def custom_logout(request):
    """Custom logout that clears session and prevents back button access."""
    auth_logout(request)
    request.session.flush()  # Completely clear the session
    response = redirect('login')
    # Prevent caching of the response
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response


@login_required
@never_cache
def dashboard(request):
    user = request.user
    my_items_count = Item.objects.filter(owner=user).count()

    approved_active_items_count = Item.objects.filter(
        owner=user,
        approval_status='approved',
        is_active=True
    ).count()

    can_receive = approved_active_items_count >= 2

    # Count user's active requests (as receiver)
    my_requests_count = Request.objects.filter(
        receiver=user,
        status__in=['pending', 'accepted']
    ).count()

    # Count incoming requests for user's items (as donor)
    incoming_requests_count = Request.objects.filter(
        item__owner=user,
        status='pending'
    ).count()

    # Count accepted requests for user's items (as donor)
    accepted_requests_count = Request.objects.filter(
        item__owner=user,
        status='accepted'
    ).count()

    context = {
        'my_items_count': my_items_count,
        'can_receive': can_receive,
        'my_requests_count': my_requests_count,
        'incoming_requests_count': incoming_requests_count,
        'accepted_requests_count': accepted_requests_count,
    }

    return render(request, 'users/dashboard.html', context)
