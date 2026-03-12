from django.urls import path
from . import views

urlpatterns = [
    # ================= AUTH =================
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
    # ================= STATIC =================
    path("about/", views.about_view, name="about"),
    # ================= SHOP =================
    path("shop/<slug:slug>/", views.category_products, name="category_products"),
    # ================= WISHLIST =================
    path("wishlist/", views.wishlist_page, name="wishlist"),
    path(
        "wishlist/toggle/<int:product_id>/",
        views.toggle_wishlist,
        name="toggle_wishlist",
    ),
    path("offers/", views.offers_page, name="offers"),
    path("contact/", views.contact_page, name="contact"),
    # urls.py
    path("product/<slug:slug>/", views.product_detail, name="product_detail"),
    path("cart/add/", views.add_to_cart, name="add_to_cart"),
    path("cart/", views.cart_page, name="cart_page"),
    path(
        "cart/update/<int:item_id>/<str:action>/",
        views.update_cart_qty,
        name="update_cart_qty",
    ),
    path("", views.home, name="home"),
    path("cart/remove/<int:item_id>/", views.remove_cart_item, name="remove_cart_item"),
    path("checkout/", views.checkout_page, name="checkout_page"),
    path("checkout/", views.checkout_page, name="checkout_page"),
    path("order-confirmed/", views.order_confirmed, name="order_confirmed"),
    path("track-order/", views.track_order, name="track_order"),
    path("payment-success/", views.payment_success, name="payment_success"),
]
