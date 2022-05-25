from django.contrib import admin

from offer.models import BrandOffer, CategoryOffer, Coupon, ProductOffer, RedeemedCoupon

# Register your models here.


class BrandOfferAdmin(admin.ModelAdmin):
    list_display = ("brand", "discount_offer", "is_active")


class CategoryOfferAdmin(admin.ModelAdmin):
    list_display = ("category", "discount_offer", "is_active")


class ProductOfferAdmin(admin.ModelAdmin):
    list_display = ("product", "discount_offer", "is_active")


admin.site.register(BrandOffer, BrandOfferAdmin)
admin.site.register(CategoryOffer, CategoryOfferAdmin)
admin.site.register(ProductOffer, ProductOfferAdmin)
admin.site.register(Coupon)
admin.site.register(RedeemedCoupon)
