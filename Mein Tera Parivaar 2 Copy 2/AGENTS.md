# AGENTS.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

**Mein Tera Parivaar** is a Django-based donation/barter platform where users exchange items without money. It implements a "give-to-get" model: users must donate items before they can request items from others.

## Development Commands

```bash
# Activate virtual environment
source MeinTeraParivar_Venv/bin/activate

# Run development server
cd MeinTeraParivar && python manage.py runserver

# Run migrations
cd MeinTeraParivar && python manage.py makemigrations && python manage.py migrate

# Create superuser
cd MeinTeraParivar && python manage.py createsuperuser

# Install dependencies
pip install -r MeinTeraParivar/requirements.txt
```

## Architecture

### Django Apps

- **`users/`** - Custom User model with phone-based authentication, signup/login views, dashboard
- **`items/`** - Item model for donations, public listing, item management
- **`moderation/`** - Request model and request handling (accept/reject flow)
- **`requests/`** - Empty app (Request model is in moderation)

### Key Models

**User** (`users/models.py`):
- Custom auth model using phone number as username
- Fields: `name`, `phone`, `email`, `city`, `caste`, `cooldown_until`

**Item** (`items/models.py`):
- Categories: clothes, education, furniture, electronics, others
- Approval workflow: `pending` → `approved`/`rejected`
- Education items auto-approve and require `board_type` + `dice_code`
- Two managers: `objects` (all) and `approved` (public)

**Request** (`moderation/models.py`):
- Status flow: `pending` → `accepted`/`rejected` → `completed`
- Links receiver (User) to Item
- Tracks `requested_quantity` and `approved_quantity`

### Business Rules

1. **Give-to-Get**: Users must have ≥2 approved active items to request
2. **Request Limits**: Max 5 active requests per user, max 2 per same item
3. **Cooldown**: 7-day cooldown after a request is accepted
4. **Quantity**: Reduces only when donor accepts (not on request creation)
5. **Auto-reject**: Pending requests auto-reject when item quantity hits 0

### URL Structure

- `/accounts/login/` - Login
- `/signup/` - Registration
- `/dashboard/` - User dashboard
- `/<pk>/` - Item detail + request creation
- `/add/` - Add new item
- `/myitemslist/` - User's donated items
- `/my-requests/` - Receiver's requests
- `/incoming-requests/` - Donor's pending requests
- `/accepted-requests/` - Donor's accepted requests
- `/admin/` - Django admin

### Templates

Located in `MeinTeraParivar/templates/`:
- `registration/` - login, signup
- `users/` - dashboard
- `items/` - add_item, public_list, item_details, my_item_list
- `moderations/` - my_request, incoming_request, accepted_requests

### Environment

Copy `.env.example` to `.env` in the `MeinTeraParivar/` directory.

Database: SQLite (`db.sqlite3`)
