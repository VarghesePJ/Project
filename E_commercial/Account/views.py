from django.shortcuts import render, redirect
from django.contrib import messages
from . models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from Payment.models import Payment


def Registration(request):
    if request.method == 'POST':
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('confirm_password')

        if password != cpassword:
            messages.error(request,"Password and comfirm password are mismatch")
            return redirect ('register')
        
        if User.objects.filter(email=email).exists():
            messages.error(request,'Email ID already existed.')
            return redirect ('register')
        
        # if len(password) < 8:
        #     messages.error(request, "Password must be at least 8 characters long")
        #     return redirect('register')
        
        # if not any(char.isupper() for char in password):
        #     messages.error(request, "Password must contain at least one uppercase letter")
        #     return redirect('register')
        
        try:
            user = User.objects.create_user(
                first_name = fname,
                last_name = lname,
                email = email,
                username=username,
                password=password
            )
            messages.success(request,'Registration successfull')
            user.generate_verification_code()
            return redirect('otp')
        except Exception as e:
            print('error')
            messages.error(request,f"Error creating account: {e}")
            return redirect('register')

    return render(request,"Account/registration.html")


def otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)

            if user.otp == otp:
                user.is_verified = True
                user.is_active = True
                user.save()
                messages.success(request,'Your account is verified.' )
                return redirect('login')
            else:
                messages.error(request,"Invaild input.")
        except ObjectDoesNotExist:
            messages.error(request,'Email not found')

    return render(request,"Account/otp.html")
 
 
def loginUser(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, email=email, password=password)

        if user is not None:
            if user.is_blocked:
                messages.error(request, 'Your account has been blocked.')
                return redirect('/')

            login(request, user)
            messages.success(request, 'Signed In')
            return redirect('home')
        else:
            messages.error(request, 'Invalid Inputs')
            return redirect('/')

    return render(request, "Account/login.html")

def logoutUser(request):
    logout(request)
    return redirect('home')

@login_required
def profile(request):
    user = request.user

    if request.method == "POST":
        action = request.POST.get('action')

        if action == 'update_profile':
            user.first_name = request.POST.get('first_name',user.first_name)
            user.last_name = request.POST.get('last_name',user.last_name)
            user.username = request.POST.get('username',user.username)
            user.email = request.POST.get('email',user.email)

            user.save()
            messages.success(request,"Profile updated")
            return redirect ('profile')
        
        elif action == 'change_password':
            current_password = request.POST.get('current_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            print(current_password,new_password,confirm_password)

            if not check_password(current_password, request.user.password):
                messages.error(request,"Your cuurent password is incorrrect.")
                return redirect('profile')
            
            if new_password != confirm_password:
                messages.error(request,"Password mismatch")
                return redirect ('profile')
            
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request,request.user)

            messages.success(request,"Your password has been successfully changed")
            return redirect('profile')

    payments = Payment.objects.filter(user=user)

    context = {"user" : user,"payments" : payments}
    
    return render(request,"Account/profile.html", context)

