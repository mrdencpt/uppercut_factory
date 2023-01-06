from django.shortcuts import get_object_or_404, redirect, render

from category.models import Category
from .models import Product, ProductGallery, ReviewRating, SizeColorStock
from carts.models import CartItem
from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .forms import ReviewForm
from django.contrib import messages
from orders.models import OrderProduct
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required


def store(request, category_slug=None):
    categories = None
    products = None
    numstock = 0
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(
            category=categories, is_available=True)

        if products:
            for pro in products:
                try:
                    sizestocks = SizeColorStock.objects.filter(
                        product_id=pro.id)
                    print(sizestocks)
                    if sizestocks:
                        for item in sizestocks:
                            numstock = numstock + item.stock
                except:
                    sizestocks = None
        paginator = Paginator(products, 1)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
        datastock = numstock
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        sizestocks = SizeColorStock.objects.filter(product_id=products.id)
        if sizestocks:
            for item in sizestocks:
                numstock = numstock + item.stock

        print(sizestocks)
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
        datastock = numstock
    context = {
        # 'products': products,
        'products': paged_products,
        'product_count': product_count,
        'datastock': datastock,
    }
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(
            category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request),
                                          product=single_product).exists()
    except Exception as e:
        raise e

    if request.user.is_authenticated:
        try:  # ค้นหาว่า ผู้ใช้นี้ซื้อสินค้านี้ รึยัง? ก่อนให้ รีวิวสินค้านี้
            orderproduct = OrderProduct.objects.filter(
                user=request.user, product_id=single_product.id).exists()
        except OrderProduct.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None

    # Get the Reviews
    reviews = ReviewRating.objects.filter(
        product_id=single_product.id, status=True)

    # Get the product gallery
    product_gallery = ProductGallery.objects.filter(
        product_id=single_product.id)

    context = {
        'single_product': single_product,
        'in_cart': in_cart,
        'orderproduct': orderproduct,
        'reviews': reviews,
        'product_gallery': product_gallery,
    }
    return render(request, 'store/product_detail.html', context)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(
                Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()
    context = {
        'products': products,
        'product_count': product_count,
        'keyword': keyword,
    }
    return render(request, 'store/store.html', context)


def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        try:  # เรียกหา รีวิวของ user คนนี้ update รีวิวเดิม
            reviews = ReviewRating.objects.get(
                user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'ขอบคุณ! รีวิวของคุณได้อัพเดทแล้ว')
            return redirect(url)
        except ReviewRating.DoesNotExist:  # เพิ่ม รีวิว
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(
                    request, 'ขอบคุณ! รีวิวของคุณได้ถูกบันทึกแล้ว')
                return redirect(url)
