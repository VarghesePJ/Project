from django.shortcuts import render
from . models import Category, Product

def Store(request,category_id = None):
    categories = Category.objects.all()
    products = Product.objects.all()

    category_id = request.GET.get('category',None)
    if category_id:
        products = products.filter(product_category_id = category_id)

    context = {
        'categories' : categories,
        'products' : products
    }

    return render(request,'Store/shop.html',context)

def viewProduct(request,product_id):
    product = Product.objects.all()[:4]
    detail = Product.objects.get(id = product_id)
    context = {
        'product' : product,
        'detail' : detail
    }

    return render(request,'Store/product.html',context)