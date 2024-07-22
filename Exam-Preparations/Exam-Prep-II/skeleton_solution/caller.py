import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Order, Profile
from django.db.models import Q, F

# Create queries within functions
def get_profiles(search_string=None) -> str:
    if search_string is None:
        return ""
        
    profiles = Profile.objects.filter(
        Q(full_name__icontains=search_string)
            |
        Q(email__icontains=search_string)
            |
        Q(phone_number__icontains=search_string)
    ).order_by("full_name")
    
    if not profiles.exists():
        return ""
    
    return "\n".join(
        f"Profile: {p.full_name}, email: {p.email}, phone number: {p.phone_number}, orders: {p.orders.count()}"
        for p in profiles
    )
    

def get_loyal_profiles() -> str:
    profiles = Profile.objects.get_regular_customers()
    
    if not profiles.exists():
        return ""
        
    return "\n".join(
        f"Profile: {p.full_name}, orders: {p.orders_count}"
        for p in profiles
    )
    

def get_last_sold_products() -> str:
    last_order = Order.objects.prefetch_related("products").last()
    
    if last_order is None or not last_order.products.exists():
        return ""
        
    products = ", ".join(last_order.products.order_by("name").values_list("name", flat=True))
    
    return f"Last sold products: {products}"