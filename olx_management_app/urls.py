from django.urls import path
from .import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('',views.index,name='index'),
    path('adminhome',views.adminhome,name='adminhome'),
    path('addcategory',views.addcategory,name='addcategory'),
    path('addcat',views.addcat,name='addcat'),
    path('Addproducts',views.Addproducts,name='Addproducts'),
    path('UserAddproducts',views.UserAddproducts,name='UserAddproducts'),
    path('addbo',views.addbo,name='addbo'),
    path('useraddbo',views.useraddbo,name='useraddbo'),
    path('showbook',views.showbook,name='showbook'),
    path('show_user_products',views.show_user_products,name='show_user_products'),
    path('update_reply',views.update_reply,name='update_reply'),
    # path('demo',views.demo,name='demo')
    path('userdetails',views.userdetails,name='userdetails'),
    path('reg',views.reg,name='reg'),
    path('adminlogin',views.adminlogin,name='adminlogin'),
    path('userhome',views.userhome,name='userhome'),
    path('reset_password1',views.reset_password1,name='reset_password1'),
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('logout1',views.logout1,name='logout1'),
    path('edit_user',views.edit_user,name='edit_user'),
    path('edit_password_page',views.edit_password_page,name='edit_password_page'),
    path('edit_details/<int:pk>',views.edit_details,name='edit_details'),
    path('view_profile',views.view_profile,name='view_profile'),
    path('edit_password/<int:pk>',views.edit_password,name='edit_password'),
    path('editbook/<int:pk>',views.editbook,name='editbook'),
    path('edit_user_product/<int:pk>',views.edit_user_product,name='edit_user_product'),
    path('editbook_details/<int:pk>',views.editbook_details,name='editbook_details'),
    path('edit_user_product_details/<int:pk>',views.edit_user_product_details,name='edit_user_product_details'),
    path('delete_user/<int:pk>',views.delete_user,name='delete_user'),
    path('delete_book/<int:pk>',views.delete_book,name='delete_book'),
    path('delete_user_product/<int:pk>',views.delete_user_product,name='delete_user_product'),
    path('categorized_products/<int:category_id>/', views.categorized_products, name='categorized_products'),
    path('bookcard/<int:pk>',views.bookcard,name='bookcard'),
    path('request_issue/<int:pk>', views.request_issue, name='request_issue'),
    path('chat_message_view/<int:book_id>', views.chat_message_view, name='chat_message_view'),
    path('requestedbook/', views.requestedbook, name='requestedbook'),
    path('loginusers',views.loginusers,name='loginusers'),
    path('approve_user/<int:signup_id>/', views.approve_user, name='approve_user'),
     path('notifications/', views.notifications, name='notifications'),
    path('reject_user/<int:signup_id>/', views.reject_user, name='reject_user'),
    path('cart',views.cart,name='cart'),
    path('cart_details/<int:pk>',views.cart_details,name='cart_details'),
    path('removecart<int:pk>',views.removecart,name='removecart'),
    path('proceedpay',views.proceedpay,name='proceedpay'),
    path('process_payment',views.process_payment,name='process_payment'),
    path('update_pay/<int:report_id>/',views.update_pay,name='update_pay'),
     
     path('show_requestedbook',views.show_requestedbook,name='show_requestedbook'),
    path('show_issuedbook',views.show_issuedbook,name='show_issuedbook'),
    path('issue_book_request/<int:request_id>/', views.issue_book_request, name='issue_book_request'),
    path('issued_books',views.issued_books,name='issued_books'),
     path('approve_book_request/<int:request_id>/', views.approve_book_request, name='approve_book_request'),
     path('return_book/<int:issued_book_id>',views.return_book,name='return_book'),
     path('show_returnedbook',views.show_returnedbook,name='show_returnedbook'),
    path('about',views.about,name='about'),
    # path('finepayment/<int:book_request_id>/', views.finepayment, name='finepayment'),
    path('user_penalty_details/', views.user_penalty_details, name='user_penalty_details'),

    path('confirm_order',views.confirm_order,name='confirm_order'),
    path('increase_quantity/<int:pk>/', views.increase_quantity, name='increase_quantity'),
    path('decrease_quantity/<int:pk>/', views.decrease_quantity, name='decrease_quantity'),
    #  path('check_signup_requests/', views.check_signup_requests, name='check_signup_requests'),
    #  path('penaltypayment',views.penaltypayment,name='penaltypayment'),
    #   path('get_unread_notification_count/', views.get_unread_notification_count, name='get_unread_notification_count'),
    # path('admin_notifications',views.admin_notifications,name='admin_notifications'),
    path('search_books_ajax/', views.search_books_ajax, name='search_books_ajax'),
    #  path('report_issue1/', views.report_issue1, name='report_issue1'),
    # path('report_issue/<int:issued_book_id>/', views.report_issue, name='report_issue'),

    path('report_problem/<int:issued_book_id>',views.report_problem,name='report_problem'),
     path('problem-history/', views.problem_history, name='problem_history'),
   path('mark_issue_as_paid/<int:issue_id>/', views.mark_issue_as_paid, name='mark_issue_as_paid'),
  #  path('check_overdue_books',views.check_overdue_books,name='check_overdue_books')

 



    


]