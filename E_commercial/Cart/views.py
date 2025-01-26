from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . models import Cart, CartItem
from Store.models import Product

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id = product_id)

    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request,f"{product.name} has addded to your cart")

    return redirect ('product', product_id = product.id)



@login_required
def update_quantity(request,product_id,type):

    cart = Cart.objects.get(user=request.user)
    cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
    
    if type == "plus":
        cart_item.quantity += 1
        cart_item.save()
        return redirect ('cart')
    elif type == "minus":
        if cart_item.quantity == 1:
            cart_item.delete()
        else:
            cart_item.quantity -= 1
            cart_item.save()
        return redirect('cart')
    

@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.total_price() for item in cart_items)

    context = {
        "cart_items" : cart_items,
        "total_price" : total_price,
    }

    return render(request,'Cart/cart.html', context)

@login_required
def remove_cart(request, product_id):
    cart = Cart.objects.get(user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
    cart_item.delete()

    messages.success(request, f"{cart_item.product.name} has been removed from your cart!")

    return redirect('cart')

