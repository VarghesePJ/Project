from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Order, Payment
from Cart.models import CartItem

import razorpay
from django.conf import settings



def bill_detail(request):
    user = request.user

    try:
        cart_item = CartItem.objects.filter(cart__user=user).first()
        if not cart_item:
            messages.error(request, "No items in the cart!")
            return redirect('cart')
    except CartItem.DoesNotExist:
        messages.error(request, "Cart item not found!")
        return redirect('cart')

    order = Order.objects.filter(user=user, cart_item=cart_item).first()

    if request.method == 'POST':
        name = request.POST.get('name')
        state = request.POST.get('state')
        address = request.POST.get('address')
        city = request.POST.get('city')
        postcode = request.POST.get('postcode')
        phone = request.POST.get('phone')
        email = request.POST.get('email')

        if order:
            order.name = name
            order.state = state
            order.address = address
            order.city = city
            order.postcode = postcode
            order.phone = phone
            order.email = email
            order.save()
            messages.success(request, "Order updated successfully!")
        else:
            Order.objects.create(
                user=user,
                cart_item=cart_item,
                name=name,
                state=state,
                address=address,
                city=city,
                postcode=postcode,
                phone=phone,
                email=email,
            )
            messages.success(request, "Order created successfully!")

        return redirect('checkout')

    return render(request, "Payment/bill_detail.html", {'order': order, 'cart_item': cart_item})


def checkout(request):
    user = request.user
    
    cart_items = CartItem.objects.filter(cart__user=user)

    total_amount = int(sum(item.total_price() for item in cart_items) * 100)
    
    orders = Order.objects.filter(user=user, cart_item__in=cart_items)

    client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

    data = { "amount": total_amount , "currency": "INR", "payment_capture" : 1 }
    payment = client.order.create(data=data)

    for order in orders:
        order.order_id = payment['id']
        order.save()

    print('************')
    print(payment)
    print('************')
    
    context = {
        'cart_items': cart_items,
        'orders': orders,
        'payment' : payment
    }

    return render(request, "Payment/checkout.html", context)

def success(request):
    user = request.user
    cart_items = CartItem.objects.filter(cart__user=user)
    orders = Order.objects.filter(user=user, cart_item__in=cart_items)
    orders.update(status="SUCCESS")

    for order in Order.objects.filter(user=user):
        payment = Payment.objects.create(
            user=order.user,
            order_id=order.order_id,
            name=order.name,
            status=order.status,
            )
    print(payment)
    
    order.delete()
    cart_items.delete()

    return render(request, 'Payment/success.html', context={"payment": payment})

