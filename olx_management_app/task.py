from celery import shared_task
from .models import ProductRequest, ProblemReport
from django.core.mail import send_mail
from decimal import Decimal
from datetime import datetime, date
from django.utils import timezone
from django.shortcuts import render




@shared_task
def check_overdue_Products(request):
    # Get the current date and time
    current_date = timezone.now().date()

    # Identify overdue Products
    overdue_Products = ProductRequest.objects.filter(due_date__lt=current_date, status='Borrowed')

    notifications = []

    for Product_request in overdue_Products:
        # Calculate fine amount (customize this logic based on your requirements)
        fine_amount = calculate_fine1(Product_request.due_date, current_date)

        # Create a ProblemReport instance for the overdue Product
        problem_report = ProblemReport(
            user=Product_request.user,
            issued_Product=Product_request,
            problem_type='Overdue',
            problem_description='The Product is overdue',
            fine_amount=fine_amount
        )
        problem_report.save()

        # Create a notification message with username and Product name
        notification_message = f"{Product_request.user.username} and {Product_request.Product.Product_name}, Product is overdue, please return it on time to avoid a penalty"
        notifications.append(notification_message)

  

    return render(request, 'adminhome.html', {'overdue_Products': overdue_Products, 'notifications': notifications})

def send_user_notification(problem_report):
    # Send an email notification to the user
    # You can customize the email content and template
    send_mail(
        'Overdue Product Notification',
        f'The Product you borrowed is overdue. Please return it.',
        
        [problem_report.user.email],
        fail_silently=False,
    )
def calculate_fine1(due_date, current_date):
    # Convert date strings to date objects if needed
    due_date = date.fromisoformat(due_date)
    current_date = date.fromisoformat(current_date)

    # Calculate the number of days overdue
    days_overdue = (current_date - due_date).days

    # Check if the Product is overdue
    if days_overdue > 0:
        overdue_charge_per_day = Decimal('1.00')  # Customize this value as needed
        fine_amount = days_overdue * overdue_charge_per_day
        return fine_amount
    else:
        return Decimal('0.00')
    