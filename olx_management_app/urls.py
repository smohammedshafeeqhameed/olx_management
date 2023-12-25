from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('adminhome', views.adminhome, name='adminhome'),
    path('addcategory', views.addcategory, name='addcategory'),
    path('addcat', views.addcat, name='addcat'),
    path('Addproducts', views.Addproducts, name='Addproducts'),
    path('UserAddproducts', views.UserAddproducts, name='UserAddproducts'),
    path('addbo', views.addbo, name='addbo'),
    path('useraddbo', views.useraddbo, name='useraddbo'),
    path('showProduct', views.showProduct, name='showProduct'),
    path('payment_history', views.payment_history, name='payment_history'),
    path('admin_feedback', views.admin_feedback, name='admin_feedback'),
    path('show_user_products', views.show_user_products, name='show_user_products'),
    path('show_user_payment_history', views.show_user_payment_history, name='show_user_payment_history'),
    path('submit_feedback/', views.submit_feedback, name='submit_feedback'),
    path('update_reply', views.update_reply, name='update_reply'),
    # path('demo',views.demo,name='demo')
    path('userdetails', views.userdetails, name='userdetails'),
    path('reg', views.reg, name='reg'),
    path('adminlogin', views.adminlogin, name='adminlogin'),
    path('userhome', views.userhome, name='userhome'),
    path('reset_password1', views.reset_password1, name='reset_password1'),
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('logout1', views.logout1, name='logout1'),
    path('edit_user', views.edit_user, name='edit_user'),
    path('edit_password_page', views.edit_password_page, name='edit_password_page'),
    path('edit_details/<int:pk>', views.edit_details, name='edit_details'),
    path('view_profile', views.view_profile, name='view_profile'),
    path('edit_password/<int:pk>', views.edit_password, name='edit_password'),
    path('editProduct/<int:pk>', views.editProduct, name='editProduct'),
    path('edit_user_product/<int:pk>', views.edit_user_product, name='edit_user_product'),
    path('editProduct_details/<int:pk>', views.editProduct_details, name='editProduct_details'),
    path('edit_user_product_details/<int:pk>', views.edit_user_product_details, name='edit_user_product_details'),
    path('delete_user/<int:pk>', views.delete_user, name='delete_user'),
    path('delete_Product/<int:pk>', views.delete_Product, name='delete_Product'),
    path('delete_user_product/<int:pk>', views.delete_user_product, name='delete_user_product'),
    path('delete_product_by_admin/<int:pk>', views.delete_product_by_admin, name='delete_product_by_admin'),
    path('categorized_products/<int:category_id>/', views.categorized_products, name='categorized_products'),
    path('Productcard/<int:pk>', views.Productcard, name='Productcard'),
    path('request_issue/<int:pk>', views.request_issue, name='request_issue'),
    path('chat_message_view/<int:Product_id>', views.chat_message_view, name='chat_message_view'),
    path('requestedProduct/', views.requestedProduct, name='requestedProduct'),
    path('loginusers', views.loginusers, name='loginusers'),
    path('approve_user/<int:signup_id>/', views.approve_user, name='approve_user'),
    path('approve_product/<int:id>/', views.approve_product, name='approve_product'),
    path('reject_product/<int:id>/', views.reject_product, name='reject_product'),
    path('notifications/', views.notifications, name='notifications'),
    path('reject_user/<int:signup_id>/', views.reject_user, name='reject_user'),
    path('cart', views.cart, name='cart'),
    path('cart_details/<int:pk>', views.cart_details, name='cart_details'),
    path('removecart<int:pk>', views.removecart, name='removecart'),
    path('proceedpay', views.proceedpay, name='proceedpay'),
    path('process_payment', views.process_payment, name='process_payment'),
    path('update_pay/<int:report_id>/', views.update_pay, name='update_pay'),

    path('show_requestedProduct', views.show_requestedProduct, name='show_requestedProduct'),
    path('show_issuedProduct', views.show_issuedProduct, name='show_issuedProduct'),
    path('issue_Product_request/<int:request_id>/', views.issue_Product_request, name='issue_Product_request'),
    path('issued_Products', views.issued_Products, name='issued_Products'),
    path('approve_Product_request/<int:request_id>/', views.approve_Product_request, name='approve_Product_request'),

    path('return_Product/<int:issued_Product_id>', views.return_Product, name='return_Product'),
    path('show_returnedProduct', views.show_returnedProduct, name='show_returnedProduct'),
    path('about', views.about, name='about'),
    # path('finepayment/<int:Product_request_id>/', views.finepayment, name='finepayment'),
    path('user_penalty_details/', views.user_penalty_details, name='user_penalty_details'),

    path('confirm_order', views.confirm_order, name='confirm_order'),
    path('increase_quantity/<int:pk>/', views.increase_quantity, name='increase_quantity'),
    path('decrease_quantity/<int:pk>/', views.decrease_quantity, name='decrease_quantity'),
    #  path('check_signup_requests/', views.check_signup_requests, name='check_signup_requests'),
    #  path('penaltypayment',views.penaltypayment,name='penaltypayment'),
    #   path('get_unread_notification_count/', views.get_unread_notification_count, name='get_unread_notification_count'),
    # path('admin_notifications',views.admin_notifications,name='admin_notifications'),
    path('search_Products_ajax/', views.search_Products_ajax, name='search_Products_ajax'),
    #  path('report_issue1/', views.report_issue1, name='report_issue1'),
    # path('report_issue/<int:issued_Product_id>/', views.report_issue, name='report_issue'),

    path('report_problem/<int:issued_Product_id>', views.report_problem, name='report_problem'),
    path('problem-history/', views.problem_history, name='problem_history'),
    path('mark_issue_as_paid/<int:issue_id>/', views.mark_issue_as_paid, name='mark_issue_as_paid'),
    #  path('check_overdue_Products',views.check_overdue_Products,name='check_overdue_Products')

]
