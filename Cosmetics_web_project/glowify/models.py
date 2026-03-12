from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
import uuid


# =========================
# Hero banner
# =========================


class HeroBanner(models.Model):

    image = models.ImageField(upload_to="hero_banners/")
    link = models.URLField(blank=True, null=True)

    order = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"Hero Banner {self.id}"


# =========================
# CATALOG
# =========================
class Category(models.Model):

    name = models.CharField(max_length=100)

    slug = models.SlugField(unique=True)

    image = models.ImageField(upload_to="categories/", blank=True, null=True)

    display_order = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["display_order"]

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to="brands/", blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    brand = models.ForeignKey(
        Brand, on_delete=models.SET_NULL, null=True, blank=True, related_name="products"
    )

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()

    price = models.DecimalField(max_digits=10, decimal_places=2)
    compare_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    # ⭐ Rating summary (for product card)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    review_count = models.PositiveIntegerField(default=0)

    image = models.ImageField(upload_to="products/")
    stock = models.PositiveIntegerField(default=0)

    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def brand_name(self):
        return self.brand.name if self.brand else ""

    @property
    def has_discount(self):
        return self.compare_price and self.compare_price > self.price

    @property
    def discount_percent(self):
        if self.compare_price and self.compare_price > self.price:
            return int(((self.compare_price - self.price) / self.compare_price) * 100)
        return 0

    @property
    def in_stock(self):
        return self.stock > 0


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="gallery"
    )
    image = models.ImageField(upload_to="products/gallery/")

    def __str__(self):
        return f"Image of {self.product.name}"


# =========================
# PRODUCT VARIANTS (Shades)
# =========================
class ProductVariant(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="variants"
    )
    shade_name = models.CharField(max_length=100)
    shade_hex = models.CharField(max_length=7, blank=True)  # color dot
    price_override = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    stock = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = [["product", "shade_name"]]

    def __str__(self):
        return f"{self.product.name} - {self.shade_name}"


class ProductTab(models.Model):
    TAB_CHOICES = [
        ("desc", "Description"),
        ("how", "How To Use"),
        ("benefits", "Benefits"),
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="tabs")
    tab_type = models.CharField(max_length=20, choices=TAB_CHOICES)
    content = models.TextField()


class Review(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


# =========================
# DISCOUNTS / OFFERS ENGINE
# =========================
class DiscountTag(models.Model):
    TYPE_CHOICES = [
        ("percent", "Percentage"),
        ("bogo", "Buy One Get One"),
        ("flat", "Flat Amount"),
    ]

    name = models.CharField(max_length=100)  # "10-20%", "Buy 1 Get 1"
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    min_percent = models.PositiveIntegerField(null=True, blank=True)
    max_percent = models.PositiveIntegerField(null=True, blank=True)
    flat_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ProductDiscount(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="discounts"
    )
    discount = models.ForeignKey(
        DiscountTag, on_delete=models.CASCADE, related_name="products"
    )

    class Meta:
        unique_together = [["product", "discount"]]

    def __str__(self):
        return f"{self.product.name} - {self.discount.name}"


# =========================
# HOMEPAGE CMS
# =========================
class HeroBanner(models.Model):
    PAGE_CHOICES = [("home", "Home"), ("offers", "Offers")]
    page = models.CharField(max_length=20, choices=PAGE_CHOICES)
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    image = models.ImageField(upload_to="hero/")
    button_text = models.CharField(max_length=50, blank=True)
    button_link = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]


class IngredientHighlight(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="ingredients/")
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]


class PromoSection(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="promos/")
    description = models.TextField(blank=True)


class PromoBanner(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    image = models.ImageField(upload_to="banners/")
    button_text = models.CharField(max_length=50, blank=True)
    button_link = models.URLField(blank=True)


class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    place = models.CharField(max_length=100, blank=True)
    profile_pic = models.ImageField(upload_to="testimonials/")
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    remark = models.TextField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-id"]


class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)


# =========================
# OFFERS PAGE
# =========================
class Offer(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, blank=True, related_name="offers"
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="offers/")
    offer_price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.title


class FeaturedOffer(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, blank=True
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="offers/featured/")
    offer_price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    button_text = models.CharField(max_length=50, default="Claim Offer")

    def __str__(self):
        return self.title


# =========================
# WISHLIST
# =========================
class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Wishlist - {self.user.username}"


class WishlistItem(models.Model):
    wishlist = models.ForeignKey(
        Wishlist, on_delete=models.CASCADE, related_name="items"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [["wishlist", "product"]]


# =========================
# CART
# =========================
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart - {self.user.username}"


# =========================
# CART ITEM (replace full CartItem model)
# =========================
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(
        ProductVariant, on_delete=models.SET_NULL, null=True, blank=True
    )
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = [["cart", "product", "variant"]]

    @property
    def unit_price(self):
        if self.variant and self.variant.price_override:
            return self.variant.price_override
        return self.product.price

    @property
    def total_price(self):
        return self.unit_price * self.quantity


# =========================
# ORDERS
# =========================
class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)


class ShippingMethod(models.Model):
    name = models.CharField(max_length=100)
    delivery_time = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Order(models.Model):
    STATUS_CHOICES = [
        ("ordered", "Ordered"),
        ("processing", "Processing"),
        ("shipped", "Shipped"),
        ("out", "Out for Delivery"),
        ("delivered", "Delivered"),
    ]

    order_number = models.CharField(max_length=20, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.PROTECT)
    shipping_method = models.ForeignKey(ShippingMethod, on_delete=models.PROTECT)

    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ordered")
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    variant = models.ForeignKey(
        ProductVariant, on_delete=models.SET_NULL, null=True, blank=True
    )
    variant_name = models.CharField(max_length=100, blank=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Payment(models.Model):
    METHOD_CHOICES = [("card", "Card"), ("netbanking", "NetBanking"), ("upi", "UPI")]
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    is_paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(null=True, blank=True)


class OrderTrackingEvent(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="tracking")
    status = models.CharField(max_length=100)
    message = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)


class IngredientHighlight(models.Model):

    title = models.CharField(max_length=200)

    description = models.TextField()

    image = models.ImageField(upload_to="ingredients")

    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
