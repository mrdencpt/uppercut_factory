from django.shortcuts import get_object_or_404, render
from store.models import Product, ReviewRating
# from accounts.models import UserProfile

def home(request):
    # userprofile = get_object_or_404(UserProfile, user=request.user)
    products = Product.objects.all().filter(is_available=True).order_by('created_date')

    # Get the reviews
    # for product in products:
    #     reviews = ReviewRating.objects.filter(product_id=product.id, status=True)

    context = {
        'products': products,
        # 'userprofile':userprofile
        # 'reviews': reviews,
    }

    return render(request, 'home.html', context)
