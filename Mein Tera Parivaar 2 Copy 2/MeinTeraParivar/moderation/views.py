from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.utils import timezone
from datetime import timedelta
from moderation.models import Request
from items.models import Item

# Cooldown period in days after a request is accepted
COOLDOWN_DAYS = 2


@login_required
def my_requests(request):
    active_requests = Request.objects.filter(
        receiver=request.user,
        status__in=['pending', 'accepted']
    ).order_by('-created_at')

    past_requests = Request.objects.filter(
        receiver=request.user,
        status__in=['rejected', 'completed']
    ).order_by('-created_at')

    context = {
        'active_requests': active_requests,
        'past_requests': past_requests,
    }
    return render(request, 'moderations/my_request.html', context)


@login_required
def incoming_requests(request):
    """Show pending requests for donor's items."""
    pending_requests = Request.objects.filter(
        item__owner=request.user,
        status='pending'
    ).order_by('-created_at')

    context = {
        'pending_requests': pending_requests,
    }
    return render(request, 'moderations/incoming_request.html', context)


@login_required
def accepted_requests(request):
    """Show accepted requests for donor's items - here donor can see receiver contact."""
    accepted = Request.objects.filter(
        item__owner=request.user,
        status='accepted'
    ).order_by('-accepted_at')

    context = {
        'accepted_requests': accepted,
    }
    return render(request, 'moderations/accepted_requests.html', context)


@login_required
@require_POST
def accept_request(request, pk):
    req = get_object_or_404(Request, pk=pk)

    # SECURITY: Only item owner can accept
    if req.item.owner != request.user:
        return HttpResponseForbidden("You are not allowed to accept this request.")

    # Only pending requests can be accepted
    if req.status != 'pending':
        return redirect('incoming_requests')

    item = req.item

    # Quantity check
    if item.available_quantity < req.requested_quantity:
        return redirect('incoming_requests')

    # ACCEPT LOGIC
    req.status = 'accepted'
    req.approved_quantity = req.requested_quantity
    req.accepted_at = timezone.now()
    req.save()

    # Reduce item quantity
    item.available_quantity -= req.approved_quantity
    item.save()

    # Set cooldown for receiver
    receiver = req.receiver
    receiver.cooldown_until = timezone.now() + timedelta(days=COOLDOWN_DAYS)
    receiver.save()

    return redirect('incoming_requests')


@login_required
@require_POST
def reject_request(request, pk):
    req = get_object_or_404(Request, pk=pk)

    # SECURITY: Only item owner can reject
    if req.item.owner != request.user:
        return HttpResponseForbidden("You are not allowed to reject this request.")

    # Only pending requests can be rejected
    if req.status != 'pending':
        return redirect('incoming_requests')

    # Reject logic
    req.status = 'rejected'
    req.save()

    return redirect('incoming_requests')


def item_detail(request, pk):
    """Item detail page - viewable by anyone, but only eligible users can request."""
    item = get_object_or_404(Item.approved, pk=pk)

    user = request.user
    can_request = False
    ineligibility_reason = None
    cooldown_remaining = None
    approved_items_count = 0

    # ---------- CAN REQUEST LOGIC (only for authenticated users) ----------
    if user.is_authenticated:
        approved_items_count = Item.objects.filter(
            owner=user,
            approval_status='approved',
            is_active=True
        ).count()

        # Check cooldown
        is_in_cooldown = (
            user.cooldown_until and 
            user.cooldown_until > timezone.now()
        )
        
        if is_in_cooldown:
            cooldown_remaining = user.cooldown_until

        # Determine eligibility
        if not user.is_active:
            ineligibility_reason = "Your account is not active yet."
        elif approved_items_count < 2:
            ineligibility_reason = f"You need to donate at least 2 items first. Currently: {approved_items_count}"
        elif item.owner == user:
            ineligibility_reason = "You cannot request your own item."
        elif item.available_quantity <= 0:
            ineligibility_reason = "This item is no longer available."
        elif is_in_cooldown:
            ineligibility_reason = f"You are in cooldown period until {cooldown_remaining.strftime('%b %d, %Y')}."
        else:
            can_request = True

    # ---------- POST : CREATE REQUEST ----------
    if request.method == 'POST':
        # Must be authenticated
        if not user.is_authenticated:
            return redirect('login')

        # Re-verify all conditions in backend
        if not can_request:
            return HttpResponseForbidden("You are not allowed to request this item.")

        quantity = int(request.POST.get('quantity', 0))

        # Quantity validation
        if quantity <= 0 or quantity > item.available_quantity:
            return redirect('item_detail', pk=item.pk)

        # Same item max 2 active requests
        active_request_count = Request.objects.filter(
            receiver=user,
            item=item,
            status__in=['pending', 'accepted']
        ).count()

        if active_request_count >= 2:
            return redirect('item_detail', pk=item.pk)

        # User max 5 active requests total
        total_active_requests = Request.objects.filter(
            receiver=user,
            status__in=['pending', 'accepted']
        ).count()

        if total_active_requests >= 5:
            return redirect('item_detail', pk=item.pk)

        # CREATE REQUEST
        Request.objects.create(
            item=item,
            receiver=user,
            requested_quantity=quantity,
            status='pending'
        )

        return redirect('my_requests')

    # ---------- GET ----------
    context = {
        'item': item,
        'can_request': can_request,
        'ineligibility_reason': ineligibility_reason,
        'approved_items_count': approved_items_count,
    }
    return render(request, 'items/item_details.html', context)

