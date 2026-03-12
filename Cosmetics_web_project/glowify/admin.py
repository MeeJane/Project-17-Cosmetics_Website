from django.contrib import admin
from .models import (
    Category,
    Brand,
    Product,
    ProductImage,
    ProductVariant,
    ProductTab,
    Review,
    DiscountTag,
    ProductDiscount,
    HeroBanner,
    IngredientHighlight,
    PromoSection,
    PromoBanner,
    Testimonial,
    FAQ,
    NewsletterSubscriber,
    Offer,
    FeaturedOffer,
    Wishlist,
    WishlistItem,
    Cart,
    CartItem,
    ShippingAddress,
    ShippingMethod,
    Order,
    OrderItem,
    Payment,
    OrderTrackingEvent,
)


# =========================
# CATEGORY
# =========================
from django.contrib import admin
from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = ("name", "display_order", "is_active")

    prepopulated_fields = {"slug": ("name",)}


# =========================
# BRAND
# =========================
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ["name", "is_active"]
    list_editable = ["is_active"]
    search_fields = ["name"]


# =========================
# PRODUCT INLINES
# =========================
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 0


class ProductTabInline(admin.TabularInline):
    model = ProductTab
    extra = 0


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    readonly_fields = ["user", "rating", "comment", "created_at"]


# =========================
# PRODUCT
# =========================
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "category",
        "brand",
        "price",
        "compare_price",
        "stock",
        "is_featured",
        "is_active",
        "created_at",
    ]
    list_filter = ["is_active", "is_featured", "category", "brand"]
    search_fields = ["name", "description"]
    list_editable = ["price", "stock", "is_featured", "is_active"]
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductImageInline, ProductVariantInline, ProductTabInline, ReviewInline]


# =========================
# DISCOUNTS
# =========================
@admin.register(DiscountTag)
class DiscountTagAdmin(admin.ModelAdmin):
    list_display = ["name", "type", "is_active"]
    list_filter = ["type", "is_active"]


@admin.register(ProductDiscount)
class ProductDiscountAdmin(admin.ModelAdmin):
    list_display = ["product", "discount"]
    list_filter = ["discount"]


# =========================
# HOMEPAGE CMS
# =========================
@admin.register(HeroBanner)
class HeroBannerAdmin(admin.ModelAdmin):
    list_display = ["title", "page", "order", "is_active"]
    list_filter = ["page", "is_active"]
    ordering = ["order"]


@admin.register(IngredientHighlight)
class IngredientHighlightAdmin(admin.ModelAdmin):
    list_display = ["title", "order"]
    ordering = ["order"]


@admin.register(PromoSection)
class PromoSectionAdmin(admin.ModelAdmin):
    list_display = ["title"]


@admin.register(PromoBanner)
class PromoBannerAdmin(admin.ModelAdmin):
    list_display = ["title"]


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ["name", "place", "rating", "is_active"]
    list_filter = ["rating", "is_active"]


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ["question", "order", "is_active"]
    list_filter = ["is_active"]
    ordering = ["order"]


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ["email", "subscribed_at"]
    search_fields = ["email"]


# =========================
# OFFERS
# =========================
@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ["title", "product", "offer_price", "original_price", "is_active"]
    list_filter = ["is_active"]


@admin.register(FeaturedOffer)
class FeaturedOfferAdmin(admin.ModelAdmin):
    list_display = ["title", "product", "offer_price", "original_price"]


# =========================
# WISHLIST
# =========================
class WishlistItemInline(admin.TabularInline):
    model = WishlistItem
    extra = 0


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ["user", "created_at"]
    inlines = [WishlistItemInline]


@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ["wishlist", "product", "added_at"]


# =========================
# CART
# =========================
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ["user", "created_at"]
    inlines = [CartItemInline]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ["cart", "product", "variant", "quantity"]


# =========================
# SHIPPING
# =========================
@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ["user", "first_name", "last_name", "city", "state", "pincode"]


@admin.register(ShippingMethod)
class ShippingMethodAdmin(admin.ModelAdmin):
    list_display = ["name", "delivery_time", "price"]


# =========================
# ORDER INLINES
# =========================
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


class OrderTrackingInline(admin.TabularInline):
    model = OrderTrackingEvent
    extra = 0
    readonly_fields = ["status", "message", "timestamp"]


# =========================
# ORDERS
# =========================
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["order_number", "user", "total", "status", "created_at"]
    list_filter = ["status", "created_at"]
    search_fields = ["order_number", "user__username"]
    inlines = [OrderItemInline, OrderTrackingInline]
    readonly_fields = ["order_number", "created_at"]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["order", "product", "variant", "quantity", "price"]


# =========================
# PAYMENTS
# =========================
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ["order", "method", "is_paid", "paid_at"]
    list_filter = ["method", "is_paid"]


# =========================
# ORDER TRACKING
# =========================
@admin.register(OrderTrackingEvent)
class OrderTrackingEventAdmin(admin.ModelAdmin):
    list_display = ["order", "status", "timestamp"]
    list_filter = ["status"]
