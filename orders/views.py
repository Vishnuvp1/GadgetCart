from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
import weasyprint
from accounts.models import Account
from accounts.views import phone_number
from carts.models import CartItem
from offer.models import Coupon, RedeemedCoupon
from offer.utils import use_coupon
from store.models import Product
from .models import Order, OrderProduct, Payment
from .forms import OrderForm
import datetime
import json
from .send_sms import send_sms
import razorpay
from django.conf import settings
from django.views.decorators.cache import never_cache

# Create your views here.


def payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(
        user=request.user, is_ordered=False, order_number=body["orderID"]
    )
    use_coupon(request)
    total = 0

    # Store transaction details inside Payment model
    payment = Payment(
        user=request.user,
        payment_id=body["transID"],
        payment_method=body["payment_method"],
        amound_paid=order.order_total,
        status=body["status"],
    )
    payment.save()

    order.payment = payment
    order.is_ordered = True
    order.save()

    if "product_id" in request.session:
        product_id = request.session["product_id"]
        product = Product.objects.get(id=product_id)

        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = product_id
        orderproduct.quantity = 1
        orderproduct.product_price = product.price
        # orderproduct.discount=request.session['coupon_discount'],
        orderproduct.ordered = True
        orderproduct.save()

        # product_variation = product.variations.all()
        # orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        # orderproduct.variations.set(product_variation)
        # orderproduct.save()

        # Reduce the quality of the sold products
        product = Product.objects.get(id=product_id)
        product.stock -= 1
        product.save()
    else:

        # Move to the cart items to Order Product table
        cart_items = CartItem.objects.filter(user=request.user)

        for item in cart_items:
            orderproduct = OrderProduct()
            orderproduct.order_id = order.id
            orderproduct.payment = payment
            orderproduct.user_id = request.user.id
            orderproduct.product_id = item.product_id
            orderproduct.quantity = item.quantity
            orderproduct.product_price = item.product.price
            # orderproduct.discount=request.session['coupon_discount'],
            orderproduct.ordered = True
            orderproduct.save()

            cart_item = CartItem.objects.get(id=item.id)
            product_variation = cart_item.variations.all()
            orderproduct = OrderProduct.objects.get(id=orderproduct.id)
            orderproduct.variations.set(product_variation)
            orderproduct.save()

            # Reduce the quality of the sold products
            product = Product.objects.get(id=item.product_id)
            product.stock -= item.quantity
            product.save()

    if "product_id" in request.session:
        del request.session["product_id"]
    else:
        # Clear cart
        CartItem.objects.filter(user=request.user).delete()

    # Send order recieved sms to customer

    phone = request.user.phone_number
    print(phone)

    # Send order number and transaction id back to senddata method via json response
    data = {"order_number": order.order_number, "transID": payment.payment_id}
    return JsonResponse(data)


@never_cache
def place_order(request, total=0, quantity=0):
    current_user = request.user

    if request.session.has_key("couponid"):
        coupon_redeem = RedeemedCoupon()
        coupon_id = request.session["couponid"]
        coupon = Coupon.objects.get(id=coupon_id)
        if coupon.is_active == True:
            coupon_redeem.user = current_user
            coupon_redeem.coupon = coupon
            coupon_redeem.save()
    grand_total = 0
    tax = 0
    g_total = 0
    product = None
    cart_items = None
    if "product_id" in request.session:
        product_id = request.session["product_id"]
        product = Product.objects.get(id=product_id)
        offerprice = product.get_price()
        quantity = 1
        total += offerprice["price"] * quantity

    else:
        # if the cart is less than or equal to 0, then redirect back to shop
        cart_items = CartItem.objects.filter(user=current_user)
        cart_count = cart_items.count()
        if cart_count <= 0:
            return redirect("store")

        for cart_item in cart_items:
            offerprice = cart_item.product.get_price()
            total += offerprice["price"] * cart_item.quantity
            quantity += cart_item.quantity
    tax = (2 * total) / 100
    g_total = total + tax
    coupon_discount_price = 0
    coupon_discount = 0
    if request.session.has_key("grand_total"):
        if request.session.has_key("coupon_discount"):
            coupon_discount = request.session["coupon_discount"]
            del request.session["coupon_discount"]
            if request.session.has_key("coupon_discount_price"):
                coupon_discount_price = request.session["coupon_discount_price"]
                del request.session["coupon_discount_price"]
            else:
                coupon_discount_price = 0

        g_total = total + tax - (coupon_discount_price)
        grand_total = round(g_total / 70)
    else:
        grand_total = round(g_total / 70)

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            # Store all the billing information inside Order table
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data["first_name"]
            data.last_name = form.cleaned_data["last_name"]
            data.phone = form.cleaned_data["phone"]
            data.email = form.cleaned_data["email"]
            data.address_line_1 = form.cleaned_data["address_line_1"]
            data.address_line_2 = form.cleaned_data["address_line_2"]
            data.country = form.cleaned_data["country"]
            data.state = form.cleaned_data["state"]
            data.city = form.cleaned_data["city"]
            data.order_note = form.cleaned_data["order_note"]
            data.order_total = g_total
            data.tax = tax
            data.ip = request.META.get("REMOTE_ADDR")
            data.save()
            # Generate order number
            yr = int(datetime.date.today().strftime("%Y"))
            dt = int(datetime.date.today().strftime("%d"))
            mt = int(datetime.date.today().strftime("%m"))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d")  # 20210305
            order_number = current_date + str(data.id)
            request.session["order_number"] = order_number
            data.order_number = order_number
            data.save()

            request.session["order_number"] = order_number
            request.session["grand_total"] = grand_total
            order_amount = g_total * 100
            razorpay_grand_total = round(order_amount)
            order_currency = "INR"
            razorpay_order = client.order.create(
                dict(
                    amount=int(order_amount),
                    currency=order_currency,
                    payment_capture="0",
                )
            )
            payment_order_id = razorpay_order["id"]

            order = Order.objects.get(
                user=current_user, is_ordered=False, order_number=order_number
            )
            context = {
                "order": order,
                "cart_items": cart_items,
                "total": total,
                "tax": tax,
                "razorpay_grand_total": razorpay_grand_total,
                "grand_total": grand_total,
                "g_total": g_total,
                "amount": order_amount,
                "payment_order_id": payment_order_id,
                "coupon_discount_price": coupon_discount_price,
                "coupon_discount": coupon_discount,
                "razorpay_merchant_key": settings.RAZOR_KEY_ID,
                "razorpay_amount": order_amount,
                "currency": order_currency,
                "product": product,
            }
            return render(request, "user/payments.html", context)
        else:
            print(form.errors)
    else:
        return redirect("checkout")

    return redirect("checkout")


def order_complete(request):
    order_number = request.session["order_number"]
    transID = request.GET.get("payment_id")

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=False)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)
        order.is_ordered = True
        order.save()
        tax = 0
        g_total = 0
        subtotal = 0
        for i in ordered_products:
            offerprice = i.product.get_price()
            subtotal += offerprice["price"] * i.quantity
        tax = (2 * subtotal) / 100
        g_total = subtotal + tax

        context = {
            "order": order,
            "ordered_products": ordered_products,
            "order_number": order.order_number,
            "subtotal": subtotal,
            "tax": tax,
            "g_total": g_total,
        }
        return render(request, "user/order_complete.html", context)

    except:

        try:
            order = Order.objects.get(order_number=order_number, is_ordered=True)
            ordered_products = OrderProduct.objects.filter(order_id=order.id)
            tax = 0
            g_total = 0
            subtotal = 0
            for i in ordered_products:
                offerprice = i.product.get_price()
                subtotal += offerprice["price"] * i.quantity
            tax = (2 * subtotal) / 100
            g_total = subtotal + tax

            payment = Payment.objects.get(payment_id=transID)

            context = {
                "order": order,
                "ordered_products": ordered_products,
                "order_number": order.order_number,
                "transID": payment.payment_id,
                "payment": payment,
                "subtotal": subtotal,
                "tax": tax,
                "g_total": g_total,
            }
            return render(request, "user/order_complete.html", context)

        except:
            try:
                order = Order.objects.get(order_number=order_number, is_ordered=True)
                ordered_products = OrderProduct.objects.filter(order_id=order.id)
                tax = 0
                g_total = 0
                subtotal = 0
                for i in ordered_products:
                    subtotal += i.product_price
                tax = (2 * subtotal) / 100
                g_total = subtotal + tax
                razorpay_order_id = request.session["razorpay_order_id"]

                payment = Payment.objects.get(payment_id=razorpay_order_id)

                context = {
                    "order": order,
                    "ordered_products": ordered_products,
                    "order_number": order.order_number,
                    "order_id": payment.payment_id,
                    "payment": payment,
                    "subtotal": subtotal,
                    "tax": tax,
                    "g_total": g_total,
                }
                return render(request, "user/order_complete.html", context)
            except (Order.DoesNotExist):
                return redirect("homepage")


def cash_on_delivery(request):
    # Move the cart items to Order Product table
    order_number = request.session["order_number"]
    order = Order.objects.get(
        user=request.user, is_ordered=False, order_number=order_number
    )

    if "product_id" in request.session:
        product_id = request.session["product_id"]
        product = Product.objects.get(id=product_id)

        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.user_id = request.user.id
        orderproduct.product_id = product_id
        orderproduct.quantity = 1
        orderproduct.product_price = product.price
        orderproduct.ordered = True
        orderproduct.save()

        # product_variation = product.variations.all()
        # orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        # orderproduct.variations.set(product_variation)
        # orderproduct.save()

        # Reduce the quality of the sold products
        product = Product.objects.get(id=product_id)
        product.stock -= 1
        product.save()
    else:
        cart_items = CartItem.objects.filter(user=request.user)
        for item in cart_items:
            orderproduct = OrderProduct()
            orderproduct.order_id = order.id
            orderproduct.user_id = request.user.id
            orderproduct.product_id = item.product_id
            orderproduct.quantity = item.quantity
            orderproduct.product_price = item.product.price
            orderproduct.ordered = True
            orderproduct.save()

            cart_item = CartItem.objects.get(id=item.id)
            product_variation = cart_item.variations.all()
            orderproduct = OrderProduct.objects.get(id=orderproduct.id)
            orderproduct.variations.set(product_variation)
            orderproduct.save()

            # Reduce the quantity of the sold products
            product = Product.objects.get(id=item.product_id)
            product.stock -= item.quantity
            product.save()

    if "product_id" in request.session:
        del request.session["product_id"]
    else:
        # Clear cart
        CartItem.objects.filter(user=request.user).delete()
    return redirect("order_complete")


client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


def razorpay_payment_verification(request):
    order_number = request.session["order_number"]
    order = Order.objects.get(
        user=request.user, is_ordered=False, order_number=order_number
    )
    if request.method == "POST":

        razorpay_payment_id = request.POST.get("razorpay_payment_id")
        razorpay_order_id = request.POST.get("razorpay_order_id")
        razorpay_signature = request.POST.get("razorpay_signature")
        print(razorpay_payment_id)
        print(razorpay_order_id)
        print(razorpay_signature)

        params_dict = {
            "razorpay_order_id": razorpay_order_id,
            "razorpay_payment_id": razorpay_payment_id,
            "razorpay_signature": razorpay_signature,
        }

        request.session["razorpay_order_id"] = razorpay_order_id
        try:
            client.utility.verify_payment_signature(params_dict)
        except:
            return JsonResponse({"messages": "error"})
        # Store transaction details inside Payment model
        payment = Payment(
            user=request.user,
            payment_id=razorpay_order_id,
            payment_method="razorpay",
            amound_paid=order.order_total,
            status="Completed",
        )
        payment.save()

        order.payment = payment
        order.is_ordered = True
        order.save()

    if "product_id" in request.session:
        product_id = request.session["product_id"]
        product = Product.objects.get(id=product_id)

        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = product_id
        orderproduct.quantity = 1
        orderproduct.product_price = product.price
        orderproduct.ordered = True
        orderproduct.save()

        # product_variation = product.variations.all()
        # orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        # orderproduct.variations.set(product_variation)
        # orderproduct.save()

        # Reduce the quality of the sold products
        product = Product.objects.get(id=product_id)
        product.stock -= 1
        product.save()
    else:

        # Move the cart items to Order Product table
        cart_items = CartItem.objects.filter(user=request.user)

        for item in cart_items:
            orderproduct = OrderProduct()
            orderproduct.order_id = order.id
            orderproduct.payment = payment
            orderproduct.user_id = request.user.id
            orderproduct.product_id = item.product_id
            orderproduct.quantity = item.quantity
            orderproduct.product_price = item.product.price
            orderproduct.ordered = True
            orderproduct.save()

            cart_item = CartItem.objects.get(id=item.id)
            product_variation = cart_item.variations.all()
            orderproduct = OrderProduct.objects.get(id=orderproduct.id)
            orderproduct.variations.set(product_variation)
            orderproduct.save()

            # Reduce the quantity of the sold products
            product = Product.objects.get(id=item.product_id)
            product.stock -= item.quantity
            product.save()

    if "product_id" in request.session:
        del request.session["product_id"]
    else:
        # Clear cart
        CartItem.objects.filter(user=request.user).delete()
    return JsonResponse({"message": "success"})


def payment_failed(request):
    return render(request, "user/payment_failed.html")


def order_pdf(request):
    order_number = request.session["order_number"]
    print(order_number)
    order = Order.objects.get(order_number=order_number, is_ordered=True)
    ordered_products = OrderProduct.objects.filter(order_id=order.id)
    tax = 0
    g_total = 0
    subtotal = 0
    for i in ordered_products:
        offerprice = i.product.get_price()
        subtotal += offerprice["price"] * i.quantity
    tax = (2 * subtotal) / 100
    g_total = subtotal + tax

    html = render_to_string(
        "user/order_pdf.html",
        {
            "ordered_products": ordered_products,
            "tax": tax,
            "g_total": g_total,
            "subtotal": subtotal,
        },
    )
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "filename=Invoice.pdf"
    weasyprint.HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(
        response
    )
    return response
