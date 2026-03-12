from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from decimal import Decimal
from .models import Category, Product
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Category, Product, Wishlist, WishlistItem
from .models import HeroBanner, Offer, FeaturedOffer
from .models import (
    Product,
    ProductVariant,
    Cart,
    CartItem,
    IngredientHighlight,
    Testimonial,
)


def home(request):

    hero_banners = HeroBanner.objects.filter(page="home", is_active=True).order_by(
        "order"
    )

    ingredients = IngredientHighlight.objects.all()

    featured_products = Product.objects.filter(is_featured=True, is_active=True)[:6]

    categories = Category.objects.filter(is_active=True).order_by("display_order")

    testimonials = Testimonial.objects.filter(is_active=True)

    wishlisted_ids = []

    if request.user.is_authenticated:
        wishlisted_ids = WishlistItem.objects.filter(
            wishlist=request.user.wishlist
        ).values_list("product_id", flat=True)

    context = {
        "hero_banners": hero_banners,
        "ingredients": ingredients,
        "featured_products": featured_products,
        "categories": categories,
        "testimonials": testimonials,
        "wishlisted_ids": wishlisted_ids,
    }

    return render(request, "glowify/home.html", context)


def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, is_active=True)

    wishlisted_ids = []
    if request.user.is_authenticated:
        wishlisted_ids = WishlistItem.objects.filter(
            wishlist=request.user.wishlist
        ).values_list("product_id", flat=True)

    return render(
        request,
        "glowify/category_products.html",
        {"category": category, "products": products, "wishlisted_ids": wishlisted_ids},
    )
    return render(
        request,
        "glowify/category_products.html",
        {"category": category, "products": products},
    )


def login_view(request):
    return render(request, "auth/login.html")


def register_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # prevent duplicate users
        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already registered")
            return redirect("register")

        # create user
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=name,
        )

        # auto login after register
        login(request, user)

        # 🔥 REDIRECT AFTER SUCCESS
        return redirect("home")  # or redirect("/")

    return render(request, "auth/register.html")


def logout_view(request):
    logout(request)
    return redirect("/")


def about_view(request):
    return render(request, "glowify/about.html")


def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug, is_active=True)
    products = Product.objects.filter(category=category, is_active=True)

    context = {
        "category": category,
        "products": products,
    }
    return render(request, "glowify/category_products.html", context)


from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


# wishlist
@login_required
def wishlist_view(request):
    wishlist = request.user.wishlist
    return render(
        request,
        "glowify/wishlist.html",
        {"items": wishlist.items.select_related("product")},
    )


@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist = request.user.wishlist

    WishlistItem.objects.get_or_create(wishlist=wishlist, product=product)

    return JsonResponse({"status": "added"})


from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Product, Wishlist, WishlistItem
from django.contrib.auth.decorators import login_required


@login_required
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # ✅ Safe wishlist getter (no crash)
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)

    item, created = WishlistItem.objects.get_or_create(
        wishlist=wishlist, product=product
    )

    if not created:
        item.delete()
        return JsonResponse({"status": "removed"})

    return JsonResponse({"status": "added"})


@login_required
def wishlist_page(request):
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    items = wishlist.items.select_related("product")
    return render(request, "glowify/wishlist.html", {"items": items})


# offers page
def offers_page(request):
    heroes = HeroBanner.objects.filter(page="offers", is_active=True).order_by("order")

    bogo_offers = Offer.objects.filter(is_active=True)

    featured = FeaturedOffer.objects.first()

    save_percent = None
    if featured and featured.original_price > 0:
        save_percent = int(
            ((featured.original_price - featured.offer_price) / featured.original_price)
            * 100
        )

    context = {
        "heroes": heroes,  # hero slider
        "bogo_offers": bogo_offers,
        "featured": featured,
        "save_percent": save_percent,
    }

    return render(request, "glowify/offers.html", context)


from .models import FAQ


def contact_page(request):
    faqs = FAQ.objects.filter(is_active=True)

    return render(
        request,
        "glowify/contact.html",
        {
            "faqs": faqs,
        },
    )


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    variants = product.variants.all()  # 👈 REQUIRED

    related_products = Product.objects.filter(
        category=product.category, is_active=True
    ).exclude(id=product.id)[:4]

    print("RELATED:", related_products)  # ✅ DEBUG LINE

    return render(
        request,
        "glowify/product_detail.html",
        {
            "product": product,
            "variants": variants,
            "related_products": related_products,
        },
    )


from django.contrib.auth.decorators import login_required


@login_required
def add_to_cart(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        variant_id = request.POST.get("variant_id")
        qty = int(request.POST.get("quantity", 1))

        cart, _ = Cart.objects.get_or_create(user=request.user)
        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product_id=product_id,
            variant_id=variant_id if variant_id else None,
        )

        if not created:
            item.quantity += qty
        else:
            item.quantity = qty

        item.save()

    return redirect("cart_page")  # create cart page later


from decimal import Decimal
from django.contrib.auth.decorators import login_required


@login_required
def cart_page(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related("product", "variant")

    subtotal = sum(item.total_price for item in items)
    shipping = Decimal("50.00") if items else Decimal("0.00")
    gst = Decimal("50.00") if items else Decimal("0.00")
    total = subtotal + shipping + gst

    context = {
        "items": items,
        "subtotal": subtotal,
        "shipping": shipping,
        "gst": gst,
        "total": total,
    }
    return render(request, "glowify/cart.html", context)


from django.shortcuts import redirect


@login_required
def update_cart_qty(request, item_id, action):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    if action == "inc":
        item.quantity += 1
    elif action == "dec":
        item.quantity -= 1
        if item.quantity < 1:
            item.quantity = 1

    item.save()
    return redirect("cart_page")


@login_required
def remove_cart_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    return redirect("cart_page")


def checkout_page(request):
    return render(request, "glowify/checkout.html")


from decimal import Decimal
from .models import Cart


def checkout_page(request):
    if not request.user.is_authenticated:
        return redirect("login")

    cart = Cart.objects.filter(user=request.user).first()
    items = cart.items.select_related("product", "variant") if cart else []

    subtotal = sum(item.total_price for item in items)
    shipping = Decimal("50.00")
    gst = Decimal("50.00")
    total = subtotal + shipping + gst

    return render(
        request,
        "glowify/checkout.html",
        {
            "items": items,
            "subtotal": subtotal,
            "shipping": shipping,
            "gst": gst,
            "total": total,
        },
    )


from django.contrib.auth.decorators import login_required


@login_required
def order_confirmed(request):

    cart = Cart.objects.get(user=request.user)
    items = cart.items.select_related("product", "variant")

    subtotal = sum(i.total_price for i in items)
    shipping = 100
    gst = 100
    total = subtotal + shipping + gst

    context = {
        "items": items,
        "subtotal": subtotal,
        "shipping": shipping,
        "gst": gst,
        "total": total,
    }

    return render(request, "glowify/order_confirmed.html", context)


from django.contrib.auth.decorators import login_required


@login_required
def track_order(request):

    cart = Cart.objects.get(user=request.user)
    items = cart.items.select_related("product", "variant")

    orders = []

    for i, item in enumerate(items):
        orders.append(
            {
                "product": item.product,
                "variant": item.variant,
                "order_no": f"#0987278{i+8}",
                "status": 3 if i == 0 else 2,
            }
        )

    return render(request, "glowify/track_order.html", {"orders": orders})


import razorpay
from django.conf import settings


def checkout_page(request):

    cart = Cart.objects.get(user=request.user)
    items = cart.items.all()

    subtotal = sum(i.product.price * i.quantity for i in items)
    shipping = 50
    gst = subtotal * Decimal("0.18")

    total = subtotal + shipping + gst

    client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )

    payment = client.order.create(
        {"amount": int(total * 100), "currency": "INR", "payment_capture": 1}  # paise
    )

    context = {
        "items": items,
        "subtotal": subtotal,
        "shipping": shipping,
        "gst": gst,
        "total": total,
        "razorpay_order_id": payment["id"],
        "razorpay_key": settings.RAZORPAY_KEY_ID,
    }

    return render(request, "glowify/checkout.html", context)


from django.http import JsonResponse
import json


def payment_success(request):

    data = json.loads(request.body)

    razorpay_payment_id = data["razorpay_payment_id"]
    razorpay_order_id = data["razorpay_order_id"]
    razorpay_signature = data["razorpay_signature"]

    # mark payment success
    # create order record if needed

    return JsonResponse({"status": "ok"})
