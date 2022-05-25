# local Django
from .models import Coupon, RedeemedCoupon


def use_coupon(request):
    if "coupon_code" in request.session:
        coupon = Coupon.objects.get(coupon_code=request.session["coupon_code"])
        RedeemedCoupon.objects.create(user=request.user, coupon=coupon)
        coupon.used += 1
        coupon.save()
    else:
        request.session["discount"] = 0
