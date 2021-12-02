from django.shortcuts import render
from django.http import JsonResponse

from offer.models import Coupon, RedeemedCoupon
from django.contrib.humanize.templatetags.humanize import intcomma
from django.utils import timezone

# Create your views here.


def apply_coupon(request):
    # This function validate the entered coupon code is valid or not   

    if request.method == 'POST':
        coupon_code = request.POST.get('coupon-code')

        try:
            if coupon_code == request.session['coupon_code']:  # Checking the entered coupon code already in the session
                return JsonResponse({'error': 'already applied'})
        except KeyError:
            pass

        # Fetching the coupon code instance
        try:
            coupon = Coupon.objects.get(coupon_code=coupon_code)
        except Coupon.DoesNotExist:
            return JsonResponse({'error': 'invalid coupon'})

        try:
            if RedeemedCoupon.objects.get(user=request.user, coupon_id=coupon.id):
                return JsonResponse({'error': 'This coupon code is already used'})
        except RedeemedCoupon.DoesNotExist:
            pass

        cart_summery(request)  # Update the cart summery with the coupon discount

        # Checking current status of the entered coupon code
        if coupon.is_active:
            if coupon.limit > coupon.used and coupon.valid_to >= timezone.now().date():
                """ Coupon code is valid, so the coupon code is saving to the  current user session """
                request.session['coupon_code'] = coupon_code
                discount = (request.session['total_price'] * coupon.discount) / 100
                request.session['discount'] = discount
                request.session['total_price'] -= discount
                request.session['grand_total'] = request.session['total_price'] + request.session['tax']
                context = {
                    'message': 'success',
                    'discount': discount,
                    'total_price': intcomma(request.session['total_price']),
                    'grand_total': intcomma(request.session['grand_total'])
                }
                return JsonResponse(context)
            else:
                return JsonResponse({'error': 'coupon code was expired'})

        return JsonResponse({'error': 'coupon code was expired'})

        
