from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.cache import never_cache
from .models import Item
from users.decorators import approved_user_required
from .forms import ItemForm


def public_item_list(request):
    """Public item listing - viewable by anyone."""
    items = Item.approved.all()
    
    # Exclude current user's items if authenticated
    if request.user.is_authenticated:
        items = items.exclude(owner=request.user)
    
    # Search functionality
    search_query = request.GET.get('search', '').strip()
    if search_query:
        items = items.filter(name__icontains=search_query)
    
    return render(request, 'items/public_list.html', {'items': items, 'search_query': search_query})


@approved_user_required
def add_item(request):
    """Add a new item for donation - requires approved user."""
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.owner = request.user
            item.available_quantity = item.total_quantity
            item.save()
            return redirect('my_items_list')
    else:
        form = ItemForm()

    return render(request, 'items/add_item.html', {'form': form})


@login_required
@never_cache
def my_items_list(request):
    """List items owned by the current user (excluding zero quantity items)."""
    my_items = Item.objects.filter(
        owner=request.user,
        available_quantity__gt=0
    ).order_by('-created_at')

    context = {
        'my_items': my_items
    }
    return render(request, 'items/my_item_list.html', context)


@login_required
@require_POST
def unlist_item(request, pk):
    """Remove an item completely from the system."""
    item = get_object_or_404(Item, pk=pk, owner=request.user)
    item.delete()
    return redirect('my_items_list')
