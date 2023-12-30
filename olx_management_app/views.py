from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .models import Signup, Category, Addproduct, LoginRequest, Cart, Notification, SignupRequestNotification, \
    SignupRequest, AdminNotification, OverdueProductNotification, PaymentHistory, Feedback, ChatMessageData, SubCategory
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
import random
import string
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import ProductRequest, ProblemReport, ChatMessage
from django.http import JsonResponse
from django.db.models import Q
from datetime import timedelta
from django.utils import timezone
from django.dispatch import receiver
import datetime
from decimal import Decimal
from datetime import date
from django.db import transaction
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password


# Create your views here.
def index(request):
    generated_password = request.GET.get('generated_password', '')
    generated_password = generate_password()
    ca = Category.objects.all()
    show = Addproduct.objects.filter(is_approved=True)
    return render(request, 'index.html', {'generated_password': generated_password, 'ca': ca, 'sh': show})


# def adminhome(request):


#       notifications = SignupRequestNotification.objects.filter(is_seen=False)
#       unread_count = notifications.count()
#       return render(request, 'adminhome.html', {'unread_count': unread_count, 'notifications': notifications})

def adminhome(request):
    # Get all unread notifications for user signups
    notifications = SignupRequestNotification.objects.filter(user__is_staff=False, is_seen=False)
    unread_count = notifications.count()
    overdue_requests = ProductRequest.objects.filter(status="Overdue")

    # Mark the notifications as seen when they are displayed
    for notification in notifications:
        notification.is_seen = True
        notification.save()
    unapproved_products = Addproduct.objects.filter(is_approved=False)
    return render(request, 'adminhome.html',
                  {'unread_count': unread_count, 'notifications': notifications, 'overdue_requests': overdue_requests, 'unapproved_products': unapproved_products})


#   else:
#      return render(request, 'adminhome.html')


# def adminhome(request):
#     if request.user.is_authenticated and request.user.is_staff:
#         # Get all unread notifications for user signups
#         signup_notifications = SignupRequestNotification.objects.filter(user__is_staff=False, is_seen=False)
#         signup_unread_count = signup_notifications.count()

#         # Get all overdue rentals
#         today = date.today()
#         overdue_rentals =OverdueProductNotification.objects.filter(due_date__lt=today, returned=False)

#         # Create notifications for overdue rentals
#         for rental in overdue_rentals:
#             # Check if a notification already exists for this rental and user
#             existing_notification = OverdueProductNotification.objects.filter(
#                 user=rental.user,
#                 Product_title=rental.Product.title,
#                 due_date=rental.due_date,
#             ).first()

#             if not existing_notification:
#                 # Create a new notification
#                 notification = OverdueProductNotification.objects.create(
#                     user=rental.user,
#                     Product_title=rental.Product.title,
#                     due_date=rental.due_date,
#                 )

#                 # Send an email notification here (use Django's send_mail)

#         overdue_notifications = OverdueProductNotification.objects.filter(is_seen=False)

#         # Mark the notifications as seen when they are displayed
#         for notification in signup_notifications:
#             notification.is_seen = True
#             notification.save()

#         for notification in overdue_notifications:
#             notification.is_seen = True
#             notification.save()

#             # Send an email to the user
#             subject = 'Overdue Product Notification'
#             message = f'Hello {notification.user.username},\n\n' \
#                       f'This is to remind you that the Product "{notification.Product_title}" ' \
#                       f'is overdue. Please return it to the library as soon as possible.\n\n' \
#                       f'Thank you!'
#             from_email = 'reshmithacr311@gmail.com'  # Replace with your email address
#             recipient_list = [notification.user.email]  # Use the user's email address

#             send_mail(subject, message, from_email, recipient_list, fail_silently=False)

#         return render(request, 'adminhome.html', {
#             'signup_unread_count': signup_unread_count,
#             'overdue_unread_count': overdue_notifications.count(),
#             'signup_notifications': signup_notifications,
#             'overdue_notifications': overdue_notifications
#         })

@login_required(login_url='index')
def addcategory(request):
    return render(request, 'addcategory.html')


@login_required(login_url='index')
def addcat(request):
    if request.method == 'POST':
        cat = request.POST['cate']

        catg = Category(cat_name=cat)
        catg.save()
        messages.success(request, 'Category Added Successfully')
        return redirect('addcategory')


@login_required(login_url='index')
def Addproducts(request):
    Products = Category.objects.all()
    return render(request, 'Addproducts.html', {'Product': Products})


@login_required(login_url='index')
def UserAddproducts(request):
    Products = Category.objects.all()
    ca = Category.objects.all()
    current_user=request.user
    user_products = Addproduct.objects.filter(user=current_user,is_approved=True)
    user_chat_messages = ChatMessageData.objects.filter(is_seen=False).exclude(sender=request.user)
    cart_items = Cart.objects.filter(user=request.user).select_related('Product')
    return render(request, 'user_add_product.html', {'cartitems': cart_items,'Product': Products, 'ca': ca, 'user_chat_messages': user_chat_messages})


@login_required(login_url='index')
def addbo(request):
    if request.method == 'POST':
        bk = request.POST['bname']
        sb = request.POST['subcat']
        an = request.POST['aname']
        des = request.POST['desc']
        yop = request.POST['yop']
        lan = request.POST['lan']
        qty = request.POST['qty']
        price = request.POST['price']
        img = request.FILES.get('img')
        sel = request.POST['sel']
        cat = Category.objects.get(id=sel)
        cat.save()
        Product = Addproduct(Product_name=bk, author_name=an, description=des, year=yop, language=lan, qty=qty, price=price,
                          image=img, add=cat, subcategory=sb)
        Product.save()
        messages.success(request, 'Product Added Successfully')
        return redirect('Addproducts')


@login_required(login_url='index')
def useraddbo(request):
    if request.method == 'POST':
        bk = request.POST['bname']
        des = request.POST['desc']
        yop = request.POST['yop']
        sb = request.POST['subcat']
        qty = request.POST['qty']
        price = request.POST['price']
        img = request.FILES.get('img')
        sel = request.POST['sel']
        cat = Category.objects.get(id=sel)
        cat.save()
        Product = Addproduct(user=request.user, Product_name=bk, description=des, year=yop, qty=qty, price=price,
                          image=img, add=cat, subcategory=sb)
        Product.save()
        messages.success(request, 'Product Added Successfully')
        return redirect('UserAddproducts')


# def userdetails(request):
#     details=Signup.objects.all()
#     return render(request,'userdetails.html',{'de':details})

@login_required(login_url='index')
def userdetails(request):
    approved_users = Signup.objects.filter(approval_status='Approved')
    return render(request, 'userdetails.html', {'approved_users': approved_users})


def generate_password(length=6):
    characters = string.digits
    password = ''.join(random.choice(characters) for _ in range(length))
    return password


# def reg(request):
#     if request.method == 'POST':
#         fname = request.POST['fname']
#         lname = request.POST['lname']
#         uname = request.POST['uname']
#         pswd = request.POST['pass']
#         cpswd = request.POST['cpass']
#         email = request.POST['email']
#         addr = request.POST['address']
#         dob = request.POST['dob']
#         cnum = request.POST['contact']
#         img = request.FILES.get('img')


#         if pswd == cpswd:
#             print("Passwords match")
#             if User.objects.filter(username=uname).exists():
#                 messages.info(request, 'This username already exists!!!!!!')
#                 return redirect('index')

#             else:
#                 print("Passwords do not match")
#                 user = User.objects.create_user(
#                     first_name=fname,
#                     last_name=lname,
#                     username=uname,
#                     password=pswd, 
#                     email=email)
#                 user.save()
#                 print("User saved")
#                 u=User.objects.get(id=user.id)
#                 print("User fetched from database")
#                 reg = Signup( Address=addr, contact=cnum, dob=dob, img=img,user=u)
#                 reg.save()
#                 print("Signup data saved")

#                 subject = 'Welcome to CARMEL LIBRARY'
#                 message = f"Thank you for signing up!\nUsername: {uname}\nPassword: {pswd}"
#                 from_email = 'reshmithacr31@gmail.com'  # Replace with your email
#                 recipient_list = [email]
#                 send_mail(subject, message, from_email, recipient_list, fail_silently=False)
#                 messages.success(request, 'Your registration was successful. You can now log in with your username and password.')
#                 return redirect('/')

#         else:
#             messages.info(request, 'Password incorrect')
#             return redirect('/')

#     return render(request, 'index.html')


def reg(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        uname = request.POST['uname']
        pswd = request.POST['pass']
        cpswd = request.POST['cpass']
        email = request.POST['email']
        addr = request.POST['address']
        dob = request.POST['dob']
        cnum = request.POST['contact']
        img = request.FILES.get('img')

        if pswd == cpswd:
            print("Passwords match")
            if User.objects.filter(email=email).exists():
                messages.info(request, 'A user with this email already exists!')
                return redirect('/')
            if User.objects.filter(username=uname).exists():
                messages.info(request, 'This username already exists!')
                return redirect('/')
            else:
                print("Passwords do not match")
                user = User.objects.create_user(
                    first_name=fname,
                    last_name=lname,
                    username=uname,
                    password=pswd,
                    email=email)
                user.save()
                print("User saved")
                u = User.objects.get(id=user.id)
                print("User fetched from database")
                reg = Signup(Address=addr, contact=cnum, dob=dob, img=img, user=u)
                reg.save()
                print("Signup data saved")

                # subject = 'Welcome to OLX'
                # message = f"Thank you for signing up!\nUsername: {uname}\nPassword: {pswd}"
                # recipient_list = email
                # send_mail(subject,message,settings.EMAIL_HOST_USER,[recipient_list])   
                # from django.core.mail import EmailMessage
                from django.template.loader import render_to_string
                from django.utils.html import strip_tags
                from django.core.mail import EmailMultiAlternatives

                # Load the HTML content from the template
                html_content = render_to_string('email_template.html', {'uname': uname, 'pswd': pswd})

                # Create an EmailMessage object
                email = EmailMultiAlternatives(
                    subject='Welcome to OLX',
                    body=strip_tags(html_content),  # Strip HTML tags for the plain text version
                    from_email='sandradhaneesh0789@gmail.com',
                    to=[email],  # Replace with the recipient's email address
                )

                # Attach the HTML content
                email.attach_alternative(html_content, "text/html")

                # Send the email
                email.send()
                messages.success(request, 'Your registration is pending . Waiting for admin approval.')
                signup_notification = SignupRequestNotification(user=user)
                signup_notification.save()

                # signup_notification = SignupRequestNotification(user=user)
                # signup_notification.save()
                # notifications = SignupRequestNotification.objects.filter(is_seen=False)
                # unread_count = notifications.count()
                # return render(request, 'adminhome.html', {'unread_count': unread_count, 'notifications': notifications})

                # signup_notification = SignupRequestNotification(user=user)
                # signup_notification.save()
                # user_signup_signal.send(sender=reg)
                return redirect('/')


        else:
            messages.info(request, 'Password incorrect')
            return redirect('/')

    return render(request, 'index.html')


def adminlogin(request):
    if request.method == 'POST':
        username = request.POST['uname']
        password = request.POST['pass']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            if user.is_staff:
                login(request, user)
                return redirect('adminhome')
            else:
                try:
                    signup = Signup.objects.get(user=user)
                    if signup.approval_status == 'Approved':
                        login(request, user)
                        messages.info(request, 'User login successful.')
                        return redirect('userhome')
                    else:
                        messages.info(request, 'Your login request is not approved yet.')
                        return redirect('index')
                except Signup.DoesNotExist:
                    messages.info(request, 'Your login request is not submitted yet.')
                    return redirect('index')
        else:
            messages.info(request, 'Invalid username & password')
            return redirect('index')
    else:
        return render(request, 'index.html')


def reset_password1(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        new_password = request.POST.get('new_password')

        try:
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            return JsonResponse({'success': True})
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'User not found.'})

    return JsonResponse({'success': False, 'message': 'Invalid request.'})


# def reset_password1(request):
#     return render(request,'reset_password.html')
@login_required(login_url='index')
def userhome(request):
    ca = Category.objects.all()
    current_user=request.user
    user_products = Addproduct.objects.filter(user=current_user,is_approved=True)
    user_chat_messages = ChatMessageData.objects.filter(is_seen=False).exclude(sender=request.user)
    show = Addproduct.objects.filter(is_approved=True).exclude(user=request.user)
    cart_items = Cart.objects.filter(user=request.user).select_related('Product')
    return render(request, 'userhome.html', {'cartitems': cart_items,'ca': ca, 'sh': show,'user_chat_messages':user_chat_messages})


def logout1(request):
    auth.logout(request)
    return redirect('index')


@login_required(login_url='index')
def showProduct(request):
    Products = Category.objects.all()
    bk = Addproduct.objects.all()
    not_approved_chat_count = Addproduct.objects.filter(is_approved=False).count()
    print(not_approved_chat_count)
    return render(request, 'showProduct.html', {'bk': Products, 'buk': bk, 'not_approved_chat_count': not_approved_chat_count})

@login_required(login_url='index')
def payment_history(request):
    Products = Category.objects.all()
    bk = PaymentHistory.objects.all()

    return render(request, 'payment_history.html', {'bk': Products, 'buk': bk})

@login_required(login_url='index')
def admin_feedback(request):
    Products = Category.objects.all()
    bk = PaymentHistory.objects.all()
    all_feedback_data = Feedback.objects.all()

    return render(request, 'admin_feedback.html', {'all_feedback_data': all_feedback_data})

@login_required(login_url='index')
def show_user_products(request):
    Products = Category.objects.all()
    bk = Addproduct.objects.filter(user=request.user)
    ca = Category.objects.all()
    current_user=request.user
    user_products = Addproduct.objects.filter(user=current_user,is_approved=True)
    user_chat_messages = ChatMessageData.objects.filter(is_seen=False).exclude(sender=request.user)
    user_chat = ChatMessage.objects.filter(Product__in=user_products).order_by('-id')
    user_products = Addproduct.objects.filter(user=request.user)
    product_ids = user_products.values_list('id', flat=True)  # Retrieve IDs of user's products
    print(product_ids)
    all_feedback_data = Feedback.objects.filter(product_id__in=product_ids)
    print(all_feedback_data)
    cart_items = Cart.objects.filter(user=request.user).select_related('Product')
    return render(request, 'show_user_products.html', {'cartitems': cart_items,'bk': Products, 'buk': bk, 'ca': ca, 'all_feedback_data': all_feedback_data, 'user_chat': user_chat, 'user_chat_messages': user_chat_messages})

@login_required(login_url='index')
def show_user_payment_history(request):

    ca = Category.objects.all()
    Products = Category.objects.all()
    current_user=request.user
    user_products = Addproduct.objects.filter(user=current_user,is_approved=True)
    user_chat_messages = ChatMessageData.objects.filter(is_seen=False).exclude(sender=request.user)
    bk = PaymentHistory.objects.filter(buyer=request.user)
    cart_items = Cart.objects.filter(user=request.user).select_related('Product')
    return render(request, 'show_user_payments.html', {'cartitems': cart_items,'bk': Products, 'buk': bk, 'ca': ca, 'user_chat_messages': user_chat_messages})


@login_required(login_url='index')
def edit_user(request):
    ca = Category.objects.all()
    current_user=request.user
    user_products = Addproduct.objects.filter(user=current_user,is_approved=True)
    user_chat_messages = ChatMessageData.objects.filter(is_seen=False).exclude(sender=request.user)
    user_profile = Signup.objects.get(user=request.user)
    cart_items = Cart.objects.filter(user=request.user).select_related('Product')
    return render(request, 'edit_user.html', {'cartitems': cart_items,'Product': user_profile, 'ca': ca, 'user_chat_messages':user_chat_messages})


@login_required(login_url='index')
def edit_password_page(request):
    ca = Category.objects.all()
    current_user=request.user
    user_products = Addproduct.objects.filter(user=current_user,is_approved=True)
    user_chat_messages = ChatMessageData.objects.filter(is_seen=False).exclude(sender=request.user)
    user_profile = Signup.objects.get(user=request.user)
    cart_items = Cart.objects.filter(user=request.user).select_related('Product')
    return render(request, 'edit_password_page.html', {'cartitems': cart_items,'Product': user_profile, 'ca': ca, 'user_chat_messages':user_chat_messages })


@login_required(login_url='index')
def edit_details(request, pk):
    if request.method == 'POST':
        Product = Signup.objects.get(user=pk)
        user = User.objects.get(id=pk)
        user.first_name = request.POST['fname']
        user.last_name = request.POST['lname']
        user.username = request.POST['uname']
        user.email = request.POST['email']
        Product.Address = request.POST['address']
        Product.dob = request.POST['dob']
        Product.contact = request.POST['contact']
        if 'img' in request.FILES:
            Product.img = request.FILES.get('img')

        Product.save()
        user.save()

        messages.success(request, 'Details updated successfully.')
        return redirect('edit_user')


@login_required(login_url='index')
def edit_password(request, pk):
    if request.method == 'POST':
        Product = Signup.objects.get(user=pk)
        user = User.objects.get(id=pk)

        if 'current_password' in request.POST and 'new_password' in request.POST and 'confirm_password' in request.POST:
            current_password = request.POST['current_password']
            new_password = request.POST['new_password']
            confirm_password = request.POST['confirm_password']

            # Check if the current password is valid
            if not check_password(current_password, user.password):
                messages.error(request, 'Invalid current password.')
                return redirect('edit_password_page')

            # Check if the new password matches the confirmation
            if new_password != confirm_password:
                messages.error(request, 'New password and confirmation do not match.')
                return redirect('edit_password_page')

            # Set the new password for the user
            user.set_password(new_password)
            user.save()
        messages.success(request, 'Password updated successfully.')
        return redirect('edit_password_page')


@login_required(login_url='index')
def view_profile(request):
    ca = Category.objects.all()
    current_user=request.user
    user_products = Addproduct.objects.filter(user=current_user,is_approved=True)
    user_chat_messages = ChatMessageData.objects.filter(is_seen=False).exclude(sender=request.user)
    current_user = request.user.id
    user1 = Signup.objects.get(user_id=current_user)
    cart_items = Cart.objects.filter(user=request.user).select_related('Product')
    return render(request, 'view_profile.html', {'cartitems': cart_items,'users': user1, 'ca': ca, 'user_chat_messages':user_chat_messages})


@login_required(login_url='index')
def editProduct(request, pk):
    Products = Addproduct.objects.get(id=pk)
    cat = Category.objects.all()
    return render(request, 'editProduct.html', {'bk': Products, 'ca': cat})

@login_required(login_url='index')
def edit_user_product(request, pk):
    Products = Addproduct.objects.get(id=pk)
    cat = Category.objects.all()
    current_user=request.user
    user_products = Addproduct.objects.filter(user=current_user,is_approved=True)
    user_chat_messages = ChatMessageData.objects.filter(is_seen=False).exclude(sender=request.user)
    cart_items = Cart.objects.filter(user=request.user).select_related('Product')
    return render(request, 'user_products_edit.html', {'cartitems': cart_items,'bk': Products, 'ca': cat, 'user_chat_messages':user_chat_messages})

@login_required(login_url='index')
def editProduct_details(request, pk):
    if request.method == 'POST':
        eProduct = Addproduct.objects.get(id=pk)
        eProduct.Product_name = request.POST['Productname']

        eProduct.description = request.POST['description']

        eProduct.year = request.POST['year']
        eProduct.qty = request.POST['qty']
        eProduct.price = request.POST['price']
        cat = request.POST['category']
        cate = Category.objects.get(id=cat)
        cate.save()
        eProduct.add = cate
        if 'img' in request.FILES:
            eProduct.image = request.FILES.get('img')

        eProduct.save()

        messages.info(request, 'Details updated successfully.')

        return redirect('showProduct')

@login_required(login_url='index')
def edit_user_product_details(request, pk):
    if request.method == 'POST':
        eProduct = Addproduct.objects.get(id=pk)
        eProduct.Product_name = request.POST['Productname']

        eProduct.description = request.POST['description']

        eProduct.year = request.POST['year']
        eProduct.qty = request.POST['qty']
        eProduct.price = request.POST['price']
        cat = request.POST['category']
        cate = Category.objects.get(id=cat)
        cate.save()
        eProduct.add = cate
        if 'img' in request.FILES:
            eProduct.image = request.FILES.get('img')

        eProduct.save()

        messages.info(request, 'Details updated successfully.')

        return redirect('show_user_products')


@login_required(login_url='index')
def delete_user(request, pk):
    user = User.objects.filter(id=pk)

    if user is not None:
        user.delete()
        messages.success(request, 'User deleted successfully.')
    else:
        messages.error(request, 'User not found.')

    return redirect('userdetails')


# def delete_Product(request,pk):
#     Product=Addproduct.objects.get(id=pk)
#     if Product is not None:
#         Product.delete()
#         messages.success(request, 'Product deleted successfully.')


def process_payment(request):
    if request.method == "POST":
        totalprice = request.POST.get('totalprice')
        payment_history = PaymentHistory(buyer=request.user, totalprice=totalprice)
        payment_history.save()
        user_cart = Cart.objects.filter(user=request.user)
        user_cart.delete()
        return render(request, 'cart.html')
    return render(request, 'cart.html')


def delete_Product(request, pk):
    try:
        Product = Addproduct.objects.get(id=pk)
        Product.delete()
        messages.success(request, 'Product deleted successfully.')
    except Addproduct.DoesNotExist:
        messages.error(request, 'Product not found.')

    return redirect('showProduct')


def delete_user_product(request, pk):
    try:
        Product = Addproduct.objects.get(id=pk)
        Product.delete()
        messages.success(request, 'Product deleted successfully.')
    except Addproduct.DoesNotExist:
        messages.error(request, 'Product not found.')

    return redirect('show_user_products')

def delete_product_by_admin(request, pk):
    try:
        Product = Addproduct.objects.get(id=pk)
        Product.delete()
        messages.success(request, 'Product deleted successfully.')
    except Addproduct.DoesNotExist:
        messages.error(request, 'Product not found.')

    return redirect('showProduct')


def submit_feedback(request):
    if request.method == 'POST':
        user = request.user  # Assuming user is logged in
        product_id = request.POST.get('product_id')
        feedback_text = request.POST.get('feedback')

        if user.is_authenticated and product_id and feedback_text:
            try:
                product = Addproduct.objects.get(id=product_id)
                # Create feedback object and save it
                feedback = Feedback.objects.create(
                    user=user,
                    product=product,
                    feedback_text=feedback_text
                )
                messages.success(request, 'Feedback submitted successfully!')
            except Addproduct.DoesNotExist:
                messages.error(request, 'Product does not exist.')
            except Exception as e:
                messages.error(request, f'Error: {e}')


    ca = Category.objects.all()
    current_user = request.user
    user_products = Addproduct.objects.filter(user=current_user, is_approved=True)
    user_chat_messages = ChatMessageData.objects.filter(is_seen=False).exclude(sender=request.user)
    show = Addproduct.objects.filter(is_approved=True).exclude(user=request.user)
    return render(request, 'userhome.html', {'ca': ca, 'sh': show, 'user_chat_messages': user_chat_messages})

@login_required(login_url='index')
def categorized_products(request, category_id):
    ca = Category.objects.all()
    current_user=request.user
    user_products = Addproduct.objects.filter(user=current_user,is_approved=True)
    user_chat_messages = ChatMessageData.objects.filter(is_seen=False).exclude(sender=request.user)
    categories = Category.objects.filter(id=category_id)

    if categories.exists():
        category = categories.first()
        # Filter Addproduct items by category and exclude items added by the current user
        Products = Addproduct.objects.filter(add=category, is_approved=True).exclude(user=request.user).exclude(qty=0)
        print(Products)
        cart_items = Cart.objects.filter(user=request.user).select_related('Product')
        return render(request, 'categories.html', {'cartitems': cart_items,'categories': [category], 'Product': Products, 'ca': ca, 'user_chat_messages':user_chat_messages})
    else:

        return render(request, 'userhome.html')

@login_required(login_url='index')
def sub_categorized_products(request, category_name):
    ca = Category.objects.all()
    current_user=request.user
    user_products = Addproduct.objects.filter(user=current_user,is_approved=True)
    user_chat_messages = ChatMessageData.objects.filter(is_seen=False).exclude(sender=request.user)

    # Filter Addproduct items by category and exclude items added by the current user
    Products = Addproduct.objects.filter(subcategory=category_name, is_approved=True).exclude(user=request.user).exclude(qty=0)
    print(Products)
    cart_items = Cart.objects.filter(user=request.user).select_related('Product')
    return render(request, 'categories.html', {'cartitems': cart_items, 'Product': Products, 'ca': ca, 'user_chat_messages':user_chat_messages})


# def search_Products(request):
#     search_query = request.GET.get('q')
#     if search_query:
#         search_results = Addproduct.objects.filter(Product_name__icontains=search_query)
#     else:
#         search_results = []

#     return render(request, 'your_template.html', {'search_results': search_results})


@login_required(login_url='index')
def Productcard(request, pk):
    bk = Addproduct.objects.get(id=pk)
    ca = Category.objects.all()
    current_user = request.user
    try:
        product = Addproduct.objects.get(id=pk)
        # Retrieve feedback for the current product
        product_feedback = Feedback.objects.filter(product=product)
    except Addproduct.DoesNotExist:
        product = None
        product_feedback = None

    # Filter chat messages created by the current user
    user_chat_messages = ChatMessage.objects.filter(Product=bk, created_by=current_user).order_by('-id')
    # Check if there is an existing pending request for the Product by the logged-in user
    # existing_request = ProductRequest.objects.filter(Product=bk, user=request.user, status='Pending').exists()
    #
    # if existing_request:
    #     messages.warning(request, 'You have already requested this Product. Please wait for approval.')

    return render(request, 'Productcard.html', {'bk': bk, 'user_chat_messages': user_chat_messages, 'ca':ca, 'product': product,
        'product_feedback': product_feedback,})


def loginusers(request):
    us = Signup.objects.all()
    return render(request, 'loginusers.html', {'us': us})


# def approve_user(request, signup_id):
#     signup = Signup.objects.get(pk=signup_id)
#     signup.approve_user()

#     # Send a notification to the user using the messaging framework
#     messages.success(request, 'Your account has been approved by the admin. You can now log in.')

#     return redirect('index')

def approve_user(request, signup_id):
    signup = get_object_or_404(Signup, pk=signup_id)

    signup.approval_status = 'Approved'
    signup.save()

    messages.success(request, 'User account has been approved by the admin.')
    # messages.info(request,f'{uname} wants to  signup ')

    return redirect('loginusers')

def approve_product(request, id):
    prd = get_object_or_404(Addproduct, pk=id)

    prd.is_approved = True
    prd.save()

    messages.success(request, 'Product has been approved by the admin.')
    # messages.info(request,f'{uname} wants to  signup ')

    return redirect('showProduct')

def reject_product(request, id):
    prd = get_object_or_404(Addproduct, pk=id)

    prd.is_approved = False
    prd.save()

    messages.success(request, 'Product has been Rejected by the admin.')
    # messages.info(request,f'{uname} wants to  signup ')

    return redirect('showProduct')



# def approve_user(request, signup_id):
#     signup = get_object_or_404(Signup, pk=signup_id)


#     signup.approval_status = 'Approved'
#     signup.save()


#     messages.success(request, 'User account has been approved by the admin.')


#     admin_message = f"User {signup.username} has signed up and been approved."
#     admin_username = "libraryadmin"  
#     admin_user = User.objects.get(username=admin_username)
#     admin_message_notification = Notification.objects.create(
#         user=admin_user,
#         message=admin_message
#     )

#     return redirect('loginusers')

@login_required
def notifications(request):
    user_notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'notifications.html', {'notifications': user_notifications})


# def reject_user(request, signup_id):
#     signup = Signup.objects.get(pk=signup_id)
#     user = signup.user
#     user.delete()

#     signup.reject_user()

#     messages.warning(request, 'User has been rejected.')

#     return redirect('loginusers') 

from django.contrib import messages


def reject_user(request, signup_id):
    signup = Signup.objects.get(pk=signup_id)
    user = signup.user

    # Send an email to the rejected user
    subject = 'Your Account Request has been Rejected'
    message = f"Dear {user.username},\n\nYour account request has been rejected by the admin. If you have any questions, please contact us.\n\nRegards,\nThe OLX Team"
    from_email = 'sandradhaneesh0789@gmail.com'
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)

    # Delete the user
    user.delete()

    signup.reject_user()

    messages.warning(request, 'User has been rejected and an email has been sent to the user.')

    return redirect('loginusers')


# @login_required(login_url='index')
def cart(request):
    ca = Category.objects.all()
    cart_items = Cart.objects.filter(user=request.user).select_related('Product')
    total_price = sum(item.total_price() for item in cart_items)
    return render(request, 'cart.html', {'cartitems': cart_items, 'totalprice': total_price, 'ca': ca})


# def increase_quantity(request, pk):
#     cart_item = Cart.objects.get(Product__id=pk, user=request.user)
#     cart_item.quantity += 1
#     cart_item.save()
#     return redirect('cart')

# def decrease_quantity(request, pk):
#     cart_item = Cart.objects.get(Product__id=pk, user=request.user)
#     if cart_item.quantity > 1:
#         cart_item.quantity -= 1
#         cart_item.save()
#     return redirect('cart')


# @login_required(login_url='index') 
# def cart_details(request, pk):
#     product = Addproduct.objects.get(id=pk)
#     cart_item, created = Cart.objects.get_or_create(user=request.user, Product=product)
#     if not created:
#         cart_item.quantity += 1
#         cart_item.save()
#     messages.success(request,'Product Added to Cart')
#     return redirect('userhome')


@login_required(login_url='index')
def cart_details(request, pk):
    product = Addproduct.objects.get(id=pk)
    cart_item, created = Cart.objects.get_or_create(user=request.user, Product=product)
    if product.qty > 0:
        if not created:
            cart_item.quantity += 1
            cart_item.save()

            # Decrement the quantity from inventory
            with transaction.atomic():
                product.qty -= 1
                product.save()

        messages.success(request, 'Product Added to Cart')
        return redirect('userhome')
    else:
        # Product is out of stock, display a message
        messages.success(request, 'Sorry, this product is currently out of stock.')
        return redirect('userhome')

@login_required(login_url='index')
def increase_quantity(request, pk):
    cart_item = Cart.objects.get(Product__id=pk, user=request.user)
    cart_item.quantity += 1
    cart_item.save()

    # Decrement the quantity from inventory
    with transaction.atomic():
        cart_item.Product.qty -= 1
        cart_item.Product.save()

    return redirect('cart')


@login_required(login_url='index')
def decrease_quantity(request, pk):
    cart_item = Cart.objects.get(Product__id=pk, user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()

        with transaction.atomic():
            cart_item.Product.qty += 1
            cart_item.Product.save()

    return redirect('cart')


@login_required(login_url='index')
def removecart(request, pk):
    product = Addproduct.objects.get(id=pk)
    cart_item = Cart.objects.filter(user=request.user, Product=product).first()

    if cart_item:
        cart_item.delete()
    messages.success(request, 'Product Removed!')
    return redirect('cart')


@login_required(login_url='index')
def proceedpay(request):
    cart_items = Cart.objects.filter(user=request.user).select_related('Product')
    total_price = sum(item.total_price() for item in cart_items)
    with transaction.atomic():
        for cart_item in cart_items:
            product = cart_item.Product
            # Ensure the quantity in the cart is not greater than available stock
            if cart_item.quantity <= product.qty:
                # Reduce the quantity in the Addproduct model
                product.qty -= cart_item.quantity
                product.save()
    return render(request, 'proceedpay.html', {'cartitems': cart_items, 'totalprice': total_price})


# def search_Products1(request):
#     search_query = request.GET.get('q', '')

#     Products = Addproduct.objects.filter(Q(Product_name__icontains=search_query) | Q(author_name__icontains=search_query))


#     context = {
#         'Products': Products,
#         'search_query': search_query
#     }

#     return render(request, 'index.html', context)

# def search_Products1(request):
#     search_query = request.GET.get('q', '')

#     sh = Addproduct.objects.filter(Q(Product_name__icontains=search_query) | Q(author_name__icontains=search_query))


#     context = {
#         'sh': sh,  
#         'search_query': search_query,

#     }

#     return render(request, 'index.html', context)


def search_Products_ajax(request):
    search_query = request.GET.get('q', '')

    sh = Addproduct.objects.filter(
        (Q(Product_name__icontains=search_query) | Q(author_name__icontains=search_query)) &
        Q(is_approved=True)
    )
    # Convert the search results to a JSON format
    results = [{'Product_name': Product.Product_name, 'author_name': Product.author_name} for Product in sh]

    return JsonResponse({'results': results})


@login_required(login_url='index')
# def request_issue(request, pk):
#     try:
#         if request.method == 'POST':
#             Product_id = request.POST.get('Product_id')  # Use get() to avoid raising KeyError
#             Product = Addproduct.objects.get(pk=Product_id)

#             # Check if the Product is in stock
#             if Product.qty <= 0:
#                 messages.error(request, 'This Product is out of stock and cannot be requested for issue.')
#             else:
#                 # Create a Product request with "Pending" status
#                 ProductRequest.objects.create(user=request.user, Product=Product, status="Pending")
#                 messages.success(request, 'Product request sent successfully!')
#         else:
#             messages.error(request, 'Invalid request method.')
#     except Addproduct.DoesNotExist:
#         messages.error(request, 'The requested Product does not exist.')
#     except Exception as e:
#         print(f"Error: {e}")
#         messages.error(request, 'An error occurred while sending the Product request.')

#     return redirect('userhome')
def request_issue(request, pk):
    try:
        if request.method == 'POST':
            Product_id = request.POST.get('Product_id')
            rental_period = request.POST.get('rental_period')

            try:
                rental_period = int(rental_period)
            except ValueError:
                rental_period = 7

            try:
                Product = Addproduct.objects.get(pk=Product_id)

                if Product.qty <= 0:
                    messages.error(request, 'This Product is out of stock and cannot be requested for issue.')
                else:
                    # Debugging: Print values to check if they are set correctly
                    print(f"Product_id: {Product_id}, rental_period: {rental_period}")
                    # Check if there is a pending request for the same user and Product
                    pending_request = ProductRequest.objects.filter(user=request.user, Product=Product,
                                                                 issued=False).exists()
                    if pending_request:
                        messages.error(request,
                                       'You have already requested this Product and it is pending. Cannot request again until it is issued.')
                    else:
                        # Calculate the due date based on the rental period
                        due_date = timezone.now() + timedelta(days=rental_period)

                        # Debugging: Print the calculated due date
                        print(f"Calculated due_date: {due_date}")

                        # Create a Product request with "Pending" status and due date
                        ProductRequest.objects.create(user=request.user, Product=Product, status="Pending",
                                                   rental_period=rental_period, due_date=due_date)
                        messages.success(request, 'Product request sent successfully!')
            except Addproduct.DoesNotExist:
                messages.error(request, 'The requested Product does not exist.')
            except Exception as e:
                print(f"Error: {e}")
                messages.error(request, 'An error occurred while sending the Product request.')

    except Exception as e:
        # Handle any other exceptions that might occur
        print(f"Error: {e}")
        messages.error(request, 'An error occurred while processing the request.')

    return redirect('userhome')


@login_required(login_url='index')
def chat_message_view(request, Product_id):
    if request.method == 'POST':
        Product = get_object_or_404(Addproduct, id=Product_id)
        chat_box = request.POST.get('chat_box')
        user = request.user  # Assuming the user is logged in

        # Create or update ChatMessage
        chat_message = ChatMessage.objects.create(
            Product=Product,
            created_by=user,
            messages=chat_box  # Set messages field to chat_box
        )

        chat_message.save()
        messages.success(request, 'Message request sent successfully!')
        return redirect('userhome')
    #     # Redirect or render as needed
    #     return redirect('success_url')  # Replace 'success_url' with your success URL
    #
    # # Handle GET requests or other cases
    # return render(request, 'your_template.html')


@login_required(login_url='index')
def send_message(request):
    if request.method == 'POST':
        receiver_id = request.POST.get('receiver_id')
        message_text = request.POST.get('message')

        # Get the receiver based on the receiver_id
        receiver = User.objects.get(id=receiver_id)

        # Create a new ChatMessageData object and save it
        message = ChatMessageData.objects.create(
            sender=request.user,
            receiver=receiver,
            message=message_text
        )
        ca = Category.objects.all()
        current_user = request.user
        users = Signup.objects.exclude(user=current_user)
        current_chat_user = Signup.objects.get(user=receiver_id)
        # Retrieve the Addproduct instances associated with the current user
        user_products = Addproduct.objects.filter(user=current_user, is_approved=True)

        # Get the chat messages related to these Addproduct instances
        user_chat_messages = ChatMessageData.objects.filter(is_seen=False).exclude(sender=request.user)

        cart_items = Cart.objects.filter(user=request.user).select_related('Product')
        sender = User.objects.get(pk=receiver_id)
        receiver = User.objects.get(pk=request.user.id)
        sender_to_receiver = Q(sender=sender, receiver=receiver)
        receiver_to_sender = Q(sender=receiver, receiver=sender)

        # Combine conditions using OR operator to get both types of messages
        messages = ChatMessageData.objects.filter(sender_to_receiver | receiver_to_sender).order_by('timestamp')
        context = {
            'cartitems': cart_items,
            'user_chat_messages': user_chat_messages,
            'ca': ca,
            'users': users,
            'sender': sender,
            'receiver': receiver,
            'messages': messages,
            "current_chat_user": current_chat_user

        }
        return render(request, 'show_requestedProduct.html', context)  # Or redirect to a success page

    return HttpResponse('Failed to send message')  # Or redirect to an error page
@login_required(login_url='index')
def chat_with_user(request, user_id):
    ca = Category.objects.all()
    current_user = request.user
    users = Signup.objects.exclude(user=current_user)
    current_chat_user = Signup.objects.get(user=user_id)
    # Retrieve the Addproduct instances associated with the current user
    user_products = Addproduct.objects.filter(user=current_user, is_approved=True)

    # Get the chat messages related to these Addproduct instances
    user_chat_messages = ChatMessageData.objects.filter(is_seen=False).exclude(sender=request.user)

    cart_items = Cart.objects.filter(user=request.user).select_related('Product')
    sender = User.objects.get(pk=user_id)
    receiver = User.objects.get(pk=request.user.id)
    sender_to_receiver = Q(sender=sender, receiver=receiver)
    receiver_to_sender = Q(sender=receiver, receiver=sender)

    # Combine conditions using OR operator to get both types of messages
    messages = ChatMessageData.objects.filter(sender_to_receiver | receiver_to_sender).order_by('timestamp')
    un_read_messages = ChatMessageData.objects.filter(is_seen=False)
    un_read_messages.update(is_seen=True)
    categories = Category.objects.all()
    categories_with_subcategories = {}

    for category in categories:
        subcategories = SubCategory.objects.filter(cat_name=category)
        categories_with_subcategories[category] = subcategories
    print("haiiiiii", categories_with_subcategories)

    for i in messages:
        print(i.message)
    context = {
        'cartitems': cart_items,
        'user_chat_messages': user_chat_messages,
        'ca': ca,
        'users': users,
        'sender': sender,
        'receiver': receiver,
        'messages': messages,
        "current_chat_user":current_chat_user,
        'categories_with_subcategories': categories_with_subcategories
    }
    # print(context)
    return render(request, 'show_requestedProduct.html', context)
@login_required(login_url='index')
def show_requestedProduct(request):
    user = request.user
    ca = Category.objects.all()
    current_user = request.user
    users = Signup.objects.exclude(user=current_user)
    # Retrieve the Addproduct instances associated with the current user
    user_products = Addproduct.objects.filter(user=current_user,is_approved=True)

    # Get the chat messages related to these Addproduct instances
    # user_chat_messages = ChatMessageData.objects.filter(is_seen=False).exclude(sender=request.user)
    user_chat_messages = ChatMessageData.objects.filter(is_seen=False).exclude(sender=request.user)
    cart_items = Cart.objects.filter(user=request.user).select_related('Product')
    return render(request, 'show_requestedProduct.html', {
        'cartitems': cart_items,
        'user_chat_messages': user_chat_messages,
        'ca': ca,
        'users': users

    })


@login_required(login_url='index')
def update_reply(request):
    if request.method == 'POST':
        message_id = request.POST.get('message_id')
        reply_message = request.POST.get('reply_message')
        print(reply_message)

        # Retrieve the ChatMessage instance based on message_id
        chat_message = ChatMessage.objects.get(pk=message_id)
        print(chat_message)
        print(chat_message.messages)
        print(chat_message.reply)
        # Update the 'reply' field with the new reply message
        chat_message.reply = reply_message
        print(chat_message.reply)
        chat_message.save()
        print(chat_message.reply)
        current_user = request.user
        user_products = Addproduct.objects.filter(user=current_user,is_approved=True)
        user_chat_messages = ChatMessageData.objects.filter(is_seen=False).exclude(sender=request.user)
        ca = Category.objects.all()

        context = {
            'user_chat_messages': user_chat_messages,
            'ca': ca,
            # Other context variables if needed
        }
        # Redirect or render as needed
        return render(request, 'show_requestedProduct.html', context)


# def show_requestedProduct(request):
#     ca = Category.objects.all()
#     user = request.user
#     requested_Products = ProductRequest.objects.filter(user=user, issued=False, status__in=['Pending', 'Approved'])
#     context = {
#         'requested_Products': requested_Products,
#         'ca': ca
#     }
#     return render(request, 'show_requestedProduct.html', context)


@login_required(login_url='index')
# def show_issuedProduct(request):
#     user = request.user
#     ca=Category.objects.all()
#     issued_Products = ProductRequest.objects.filter(user=user, issued=True)  # Retrieve issued Products for the logged-in user
#     for issued_Product in issued_Products:
#         # Calculate due date by adding 14 days to the request date
#         issued_Product.due_date = issued_Product.request_date + timedelta(days=14)
#     context = {
#         'issued_Products': issued_Products,
#         'ca':ca
#     }
#     return render(request, 'show_issuedProduct.html', context)

def show_issuedProduct(request):
    user = request.user
    ca = Category.objects.all()
    issued_Products = ProductRequest.objects.filter(user=user, issued=True)

    for issued_Product in issued_Products:
        # Calculate due date based on the rental period
        due_date = issued_Product.request_date + timedelta(days=issued_Product.rental_period)
        issued_Product.due_date = due_date

    context = {
        'issued_Products': issued_Products,
        'ca': ca
    }

    return render(request, 'show_issuedProduct.html', context)


@login_required(login_url='index')
def requestedProduct(request):
    requested_Products = ProductRequest.objects.all()
    # Calculate and update overdue amount for each request
    today = date.today()
    for Product_request in requested_Products:
        if Product_request.due_date < today:
            days_overdue = (today - Product_request.due_date).days
            overdue_charge_per_day = 50  # Change this to your desired overdue charge
            overdue_amount = days_overdue * overdue_charge_per_day

            # Update the ProductRequest object with the calculated overdue amount
            Product_request.overdue_amount = overdue_amount
            Product_request.save()  # Save the updated object
    return render(request, 'requestedProduct.html', {'requested_Products': requested_Products[::-1]})


# @login_required(login_url='index')
# def issue_Product_request(request, request_id):
#     Product_request = get_object_or_404(ProductRequest, id=request_id)

#     print(f"Product request status: {Product_request.status}")
#     print(f"Is Issued: {Product_request.issued}")
#     print(f"Product quantity: {Product_request.Product.qty}")

#     if Product_request.status == "Approved" and not Product_request.issued:
#         try:
#             Product_request.issued = True
#             Product_request.save()

#             Product_request.Product.qty -= 1
#             Product_request.Product.save()

#             messages.success(request, 'Product issued successfully!')
#         except Exception as e:
#             messages.error(request, 'An error occurred while issuing the Product.')
#             print(f"Error: {e}")
#     else:
#         messages.error(request, 'Product request cannot be issued.')

#     print(f"Issued status after update: {Product_request.issued}")
#     print(f"Product quantity after update: {Product_request.Product.qty}")

#     return redirect('requestedProduct')

@login_required(login_url='index')
def issue_Product_request(request, request_id):
    Product_request = get_object_or_404(ProductRequest, id=request_id)

    print(f"Product request status: {Product_request.status}")
    print(f"Is Issued: {Product_request.issued}")
    print(f"Product quantity: {Product_request.Product.qty}")

    if Product_request.status == "Approved" and not Product_request.issued:
        try:
            Product_request.issued = True
            Product_request.save()

            Product_request.Product.qty -= 1
            Product_request.Product.save()

            messages.success(request, 'Product issued successfully!')
        except Exception as e:
            messages.error(request, 'An error occurred while issuing the Product.')
            print(f"Error: {e}")
    else:
        messages.error(request, 'Product request cannot be issued.')

    print(f"Issued status after update: {Product_request.issued}")
    print(f"Product quantity after update: {Product_request.Product.qty}")

    return redirect('requestedProduct')


@login_required(login_url='index')
def issued_Products(request):
    issued_Products = ProductRequest.objects.filter(status="Approved", issued_Products__gt=0)
    return render(request, 'issued_Products.html', {'issued_Products': issued_Products})


@login_required(login_url='index')
def approve_Product_request(request, request_id):
    Product_request = get_object_or_404(ProductRequest, id=request_id)
    if Product_request.status == "Pending":
        Product_request.status = "Approved"
        Product_request.save()
        messages.success(request, 'Product request approved successfully!')
    else:
        messages.error(request, 'Product request cannot be approved.')

    return redirect('requestedProduct')


@login_required(login_url='index')
# def show_returnedProduct(request): #1st workin
#     returned_Products = ProductRequest.objects.filter(issued=False)
#     for returned_Product in returned_Products:
#         returned_Product.due_date = returned_Product.request_date + timedelta(days=14)
#     context = {'returned_Products': returned_Products}
#     return render(request, 'show_returnedProduct.html', context)

# def show_returnedProduct(request):#2nd workin
#     user = request.user 
#     ca = Category.objects.all() 
#     returned_Products = ProductRequest.objects.filter(issued=False)

#     for returned_Product in returned_Products:
#         # Calculate due date based on the rental period
#         due_date = returned_Product.request_date + timedelta(days=returned_Product.rental_period)
#         returned_Product.due_date = due_date

#     context = {
#         'returned_Products': returned_Products,
#         'ca': ca  
#     }

#     return render(request, 'show_returnedProduct.html', context)

def show_returnedProduct(request):
    user = request.user
    ca = Category.objects.all()
    returned_Products = ProductRequest.objects.filter(issued=False)

    for returned_Product in returned_Products:
        # Calculate due date based on the rental period
        due_date = returned_Product.request_date + timedelta(days=returned_Product.rental_period)
        returned_Product.due_date = due_date

    issue_reports = ProblemReport.objects.filter(issued_Product__in=returned_Products)

    context = {
        'returned_Products': returned_Products,
        'ca': ca,
        'issue_reports': issue_reports
    }

    return render(request, 'show_returnedProduct.html', context)


# @login_required(login_url='index')
# def finepayment(request, Product_request_id):
#     Product_request = get_object_or_404(ProductRequest, id=Product_request_id)

#     if request.method == 'POST':
#         penalty = request.POST.get('penalty')
#         status = request.POST.get('status')

#         Product_request.penalty = penalty
#         Product_request.status = status
#         Product_request.save()

#         # Redirect back to the same page or a relevant page
#         return redirect('show_returnedProduct')  

#     return render(request, 'userhome.html', {'Product_request': Product_request})

@login_required(login_url='index')
def user_penalty_details(request):
    problem_reports = ProblemReport.objects.filter(user=request.user).exclude(problem_type="no_issue")

    return render(request, 'user_penalty_details.html', {'problem_reports': problem_reports})


# @login_required(login_url='index')
# def return_Product(request, issued_Product_id):
#     issued_Product = get_object_or_404(ProductRequest, id=issued_Product_id)
#     if issued_Product.issued and request.method == 'POST':
#         print('Product issued')
#         penalty = request.POST.get('penalty')
#         status = request.POST.get('status')

#         issued_Product.penalty = penalty
#         issued_Product.status = status

#         issued_Product.issued = False
#         issued_Product.return_date = timezone.now()
#         issued_Product.save()

#         returned_Product = issued_Product.Product
#         returned_Product.qty += 1
#         returned_Product.save()

#         messages.success(request, 'The Product has been successfully returned. Penalty Amount: {} Reason: {}'.format(penalty, status))

#         return redirect('show_issuedProduct')

#     return render(request, 'userhome.html')

def return_Product(request, issued_Product_id):
    issued_Product = get_object_or_404(ProductRequest, id=issued_Product_id)
    if issued_Product.issued and request.method == 'POST':
        print('Product issued')
        penalty = request.POST.get('penalty')
        if not penalty:
            penalty = 0
        status = request.POST.get('status')

        issued_Product.penalty = penalty
        issued_Product.status = status

        issued_Product.issued = False
        issued_Product.return_date = timezone.now()
        issued_Product.save()

        returned_Product = issued_Product.Product
        returned_Product.qty += 1
        returned_Product.save()

        messages.success(request,
                         'The Product has been successfully returned. Penalty Amount: {} Reason: {}'.format(penalty,
                                                                                                         status))

        return redirect('show_issuedProduct')

    return render(request, 'userhome.html')


# def return_Product(request, issued_Product_id):
#     issued_Product = get_object_or_404(ProductRequest, id=issued_Product_id)
#     if issued_Product.issued and request.method == 'POST':
#         print('Product issued')
#         penalty = request.POST.get('penalty')
#         status = request.POST.get('status')

#         issued_Product.penalty = penalty
#         issued_Product.status = status

#         issued_Product.issued = False
#         issued_Product.return_date = timezone.now()
#         issued_Product.save()

#         returned_Product = issued_Product.Product
#         returned_Product.qty += 1
#         returned_Product.save()

#         messages.success(request, 'The Product has been successfully returned. Penalty Amount: {} Reason: {}'.format(penalty, status))

#         return redirect('show_issuedProduct')

#     return render(request, 'userhome.html')


# def return_Product(request, issued_Product_id):
#     issued_Product = get_object_or_404(ProductRequest, id=issued_Product_id)

#     if issued_Product.issued and request.method == 'POST':
#         # Calculate overdue_days
#         due_date = issued_Product.due_date  # Replace with the actual due date field name
#         return_date = timezone.now()
#         overdue_days = (return_date - due_date).days

#         penalty_rate = 1  # Replace with your actual penalty rate per day

#         # Calculate penalty based on overdue days and penalty rate
#         penalty = overdue_days * penalty_rate

#         status = request.POST.get('status')

#         issued_Product.penalty = penalty
#         issued_Product.status = status

#         issued_Product.issued = False
#         issued_Product.return_date = return_date
#         issued_Product.save()

#         returned_Product = issued_Product.Product
#         returned_Product.qty += 1
#         returned_Product.save()

#         messages.success(request, f'The Product has been successfully returned. Penalty Amount: {} Reason: {}')

#         return redirect('show_issuedProduct')

#     return render(request, 'userhome.html')


@login_required(login_url='index')
def confirm_order(request):
    if request.method == 'POST':
        user = request.user

        # Send email
        subject = 'Order Confirmation'
        message = 'Your order has been confirmed. Thank you for your purchase!'
        from_email = 'sandradhaneesh0789@gmail.com'
        recipient_list = [user.email]

        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        print(f"Email sent to {recipient_list}")

        messages.success(request, 'Order placed.Please do the payment')

        return render(request, 'cart_pay.html')

    return render(request, 'cart.html')


def about(request):
    return render(request, 'about.html')


def penaltypayment(request):
    ca = Category.objects.all()
    return render(request, 'penaltypayment.html', {'ca': ca})


# def report_problem(request, issued_Product_id):
#     try:
#         issued_Product = ProductRequest.objects.get(id=issued_Product_id)
#     except ProductRequest.DoesNotExist:
#         messages.error(request, 'Issued Product not found.')
#         return redirect('your_rented_Products_page')  # Replace with the URL name for the rented Products page

#     # Get problem type and description from the form submission
#     problem_type = request.POST.get('problem_type')
#     problem_description = request.POST.get('problem_description')

#     # Calculate fine amount based on problem type and additional charges (if any)
#     fine_amount = calculate_fine(issued_Product, problem_type)

#     # Create a problem report entry
#     problem_report = ProblemReport(
#         user=request.user,
#         issued_Product=issued_Product,
#         problem_type=problem_type,
#         problem_description=problem_description,
#         fine_amount=fine_amount
#     )
#     problem_report.save()


#     return redirect('show_issuedProduct')
def report_problem(request, issued_Product_id):
    try:
        issued_Product = ProductRequest.objects.get(id=issued_Product_id)
    except ProductRequest.DoesNotExist:
        messages.error(request, 'Issued Product not found.')
        return redirect('show_issuedProduct')

    if request.method == 'POST':
        # Get problem type and description from the form submission
        print('Product issued')
        problem_type = request.POST.get('problem_type')
        problem_description = request.POST.get('problem_description')

        # Calculate fine amount based on problem type and additional charges
        fine_amount = calculate_fine(issued_Product, problem_type)

        # Create a problem report entry
        problem_report = ProblemReport(
            user=request.user,
            issued_Product=issued_Product,
            problem_type=problem_type,
            problem_description=problem_description,
            fine_amount=fine_amount
        )
        problem_report.save()

        status = request.POST.get('status')

        issued_Product.status = status
        issued_Product.fine_amount = fine_amount
        issued_Product.issued = False
        issued_Product.return_date = timezone.now()
        issued_Product.save()

        returned_Product = issued_Product.Product
        returned_Product.qty += 1
        returned_Product.save()
        problem_description = request.POST.get('problem_description')
        messages.success(request,
                         'The Product has been successfully returned. Penalty Amount: {} Reason: {}'.format(fine_amount,
                                                                                                         problem_description))

        return redirect('show_issuedProduct')

    return redirect('show_issuedProduct')


# def calculate_fine(issued_Product, problem_type):
#     if problem_type == 'lost':
#         # Calculate the fine for a lost Product as the Product's original price plus any additional charges
#         fine_amount = issued_Product.Product.price + issued_Product.additional_charges
#     else:


#         # For other problem types (damage, overdue), use the predefined rates
#         fine_rates = {
#             'damage': 20,    # Fine amount for a damaged Product
#             'overdue': 10,   # Fine amount for overdue return


#         }
#         fine_rate = fine_rates.get(problem_type, 0)  
#         fine_amount = issued_Product.Product.price + fine_rate

#     return fine_amount


# def calculate_fine(issued_Product, problem_type):
#     if problem_type == 'lost':
#         # Calculate the fine amount for a lost Product (e.g., original price + additional charges)
#         original_price = issued_Product.Product.price
#         additional_charges = Decimal('10.00')  # You can customize this value
#         fine_amount = original_price + additional_charges
#     elif problem_type == 'damage':
#         # Calculate the fine amount for a damaged Product (e.g., based on the extent of damage)
#         damage_charge_per_page = Decimal('2.00')  # You can customize this value
#         damaged_pages = 10  # You can get this information from the user or other sources
#         fine_amount = damage_charge_per_page * damaged_pages
#     else:
#         # Handle other issue types if needed
#         fine_amount = Decimal('0.00')  # Default to no fine

#     return fine_amount


def calculate_fine(issued_Product, problem_type):
    if problem_type == 'lost':
        # Calculate the fine amount for a lost Product 
        original_price = issued_Product.Product.price
        additional_charges = Decimal('10.00')
        fine_amount = original_price + additional_charges
    elif problem_type == 'damage':
        # Calculate the fine amount for a damaged Product (
        damage_charge_per_page = Decimal('2.00')
        damaged_pages = 10
        fine_amount = damage_charge_per_page * damaged_pages
    elif problem_type == 'no_issue':
        fine_amount = Decimal('0.00')
    elif problem_type == 'overdue':
        due_date = issued_Product.due_date  # Remove .date()
        today = date.today()  # Get the current date without time
        if today > due_date:
            # Calculate fine based on the number of days overdue
            days_overdue = (today - due_date).days
            overdue_charge_per_day = Decimal('10.00')
            fine_amount = days_overdue * overdue_charge_per_day
        else:
            fine_amount = Decimal('0.00')

    return fine_amount


def problem_history(request):
    # Retrieve the user's problem reports from the database
    problem_reports = ProblemReport.objects.filter(user=request.user).exclude(problem_type="no_issue")

    return render(request, 'problem_history.html', {'problem_reports': problem_reports})


def update_pay(request, report_id):
    if request.method == 'POST':
        problem_report = ProblemReport.objects.get(id=report_id)
        problem_report.is_paid = True
        problem_report.save()
        problem_reports = ProblemReport.objects.filter(user=request.user).exclude(problem_type="no_issue")

    return render(request, 'user_penalty_details.html', {'problem_reports': problem_reports})


def mark_issue_as_paid(request, issue_id):
    try:
        issue_report = ProblemReport.objects.get(id=issue_id)
        # Mark the issue as paid in the database
        issue_report.is_paid = True
        issue_report.save()
        return JsonResponse({'status': 'success'})
    except ProblemReport.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Issue report not found'})


def check_overdue_Products(request):
    # Get the current date and time
    current_datetime = timezone.now()

    # Identify overdue Products
    overdue_Products = ProblemReport.objects.filter(due_date__lt=current_datetime)

    notifications = []

    for Product_request in overdue_Products:
        # Calculate fine amount 
        fine_amount = calculate_fine1(Product_request.due_date, current_datetime)

        # Create a ProblemReport instance for the overdue Product
        overdue = ProductRequest(
            user=Product_request.user,
            issued_Product=Product_request,
            problem_type='Overdue',
            problem_description='The Product is overdue',
            fine_amount=fine_amount
        )
        overdue.save()

        # Create a notification message with username and Product name
        notification_message = f"{Product_request.user.username} and {Product_request.Product.Product_name}, Product is overdue, please return it on time to avoid a penalty"
        notifications.append(notification_message)

    return render(request, 'adminhome.html', {'overdue_Products': overdue_Products, 'notifications': notifications})


def calculate_fine1(due_date, current_date):
    # Convert date strings to date objects if needed
    due_date = date.fromisoformat(due_date)
    current_date = date.fromisoformat(current_date)

    # Calculate the number of days overdue
    days_overdue = (current_date - due_date).days

    # Check if the Product is overdue
    if days_overdue > 0:
        overdue_charge_per_day = Decimal('1.00')
        fine_amount = days_overdue * overdue_charge_per_day
        return fine_amount
    else:
        return Decimal('0.00')


def send_overdue_notifications(overdue_requests):
    """
    Send overdue Product notifications to users.
    """
    for request in overdue_requests:

        if not request.user.email:
            continue

        subject = "Overdue Product Notification"
        message = f"Dear {request.user.username},\n\nYour Product request for '{request.Product.Product_name}' is overdue. Please return it as soon as possible to avoid penalties."
        from_email = "reshmitha31@gmail.com"
        recipient_list = [request.user.email]

        send_mail(subject, message, from_email, recipient_list)
