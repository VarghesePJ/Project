from django.shortcuts import render, redirect
from Account.models import User
from Store.models import Category, Product
from Payment.models import Payment

def admin(request):
    user_list = User.objects.all()

    context = {
        'user': user_list
    }

    return render(request, "Admin/admin.html", context)

# def blocking(request,user_id):
#     user = User.objects.get(id=user_id)
#     user.is_blocked = not user.is_blocked
#     user.save()
#     return redirect('admin')


def blocking (request, user_id):
    user = User.objects.get(id = user_id)
    if user.is_blocked:
        user.is_blocked = False
    else:
        user.is_blocked = True

    user.save()
    return redirect('admin')


def user_view(request,user_id):
    user = User.objects.get(id=user_id)

    context = {
        "user" : user
    }

    return render(request,"Admin/user_detail.html", context)

def category(request):
    category = Category.objects.all()
    
    context = {
        "category" : category
    }

    return render(request,"Admin/Category/category.html",context)

def category_create(request):
    if request.method == "POST":
        category = Category(
            name = request.POST.get('name'),
            description = request.POST.get('description'),
            image = request.FILES['image']
        )

        category.save()
        return redirect('category')
    
    return render(request,'Admin/Category/category_create.html')


def category_view(request,category_id):
    category = Category.objects.get(id=category_id)

    return render(request,"Admin/Category/category_view.html", context = {"category" : category})

def category_update(request,category_id):
    category = Category.objects.get(id=category_id)

    if request.method == "POST":
        category.name = request.POST.get('name',category.name)
        category.description = request.POST.get('description',category.description)

        if 'image' in request.FILES:
            category.image = request.FILES['image']

        category.save()
        return redirect ('category')

    return render(request,"Admin/Category/category_update.html", context = {"category" : category })

def category_delete(request,category_id):
    category = Category.objects.get(id=category_id)
    if request.method == 'POST':
        category.delete()
        return redirect ('category')

    return render(request,"Admin/Category/category_delete.html", context = {"category" : category})

def product(request):
    product = Product.objects.all()
    
    context = {
        "product" : product
    }

    return render(request,"Admin/Product/product.html",context)

def product_create(request):
    categories = Category.objects.all()
    if request.method == "POST":
        product = Product(
            name = request.POST.get('name'),
            product_category = Category.objects.get(id=request.POST.get('product_category')),
            description = request.POST.get('description'),
            image = request.FILES['image'],
            price = request.POST.get('price'),
            stock = request.POST.get('stock'),
            is_available = request.POST.get('is_available') == "1"
        )

        product.save()
        return redirect('product')
    
    return render(request,'Admin/Product/product_create.html',context={"categories" : categories})

def Product_view(request,product_id):
    product = Product.objects.get(id=product_id)

    return render(request,"Admin/Product/product_view.html", context = {"product" : product})

def product_update(request,product_id):
    category = Category.objects.all()
    product = Product.objects.get(id=product_id)

    if request.method == "POST":
        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        product.product_category = Category.objects.get(id=request.POST.get('product_category'))
        product.price = request.POST.get('price')
        product.stock = request.POST.get('stock')
        product.is_available = request.POST.get('is_available') == '1'

        if 'image' in request.FILES:
            product.image = request.FILES['image']

        product.save()
        return redirect ('product')
    
    context = {
        "product" : product,
        'category' : category
    }

    return render(request,"Admin/Product/product_update.html", context)

def product_delete(request,product_id):
    product = Product.objects.get(id=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect ('product')

    return render(request,"Admin/Product/product_delete.html", context = {"product" : product})

def order(request):
    payments = Payment.objects.all()

    context = {
        "payments" : payments
    }

    return render(request,"Admin/order.html",context)