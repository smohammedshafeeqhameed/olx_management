from django.db import models
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from decimal import Decimal
from datetime import date
# Create your models here.

class Signup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    Address = models.CharField(max_length=255)
    contact = models.CharField(max_length=10)
    dob = models.DateField()
    img = models.ImageField(upload_to='images/')


    STATUS_CHOICES = (
        ('Pending Approval', 'Pending Approval'),
        ('Approved', 'Approved'),
    )
    approval_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending Approval')
    
    def save(self, *args, **kwargs):
        if self.pk is None:  
            self.approval_status = 'Pending Approval'
        super(Signup, self).save(*args, **kwargs)
    
    def approve_user(self):
        self.approval_status = 'Approved'
        self.save()
    def reject_user(self):
        self.approved = False
        self.save()

    def reject_user(self):
        self.delete()  
     
class LoginRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    request_date = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False) 

    def __str__(self):
        return f"Login request for {self.user}"



class Category(models.Model):
    cat_name=models.CharField(max_length=255)
   
class Addproduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    add=models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    Product_name=models.CharField(max_length=255)
    description=models.CharField(max_length=255) 
    year=models.IntegerField(null=True)
    qty=models.IntegerField(null=True, blank=True)
    price=models.IntegerField(null=True)
    image=models.ImageField(upload_to="images/",null=True)
    is_approved = models.BooleanField(default=False)


class PaymentHistory(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    totalprice = models.IntegerField(null=True)
    update_date = models.DateTimeField(auto_now=True)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    Product = models.ForeignKey(Addproduct, on_delete=models.CASCADE,null=True)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
            return self.quantity * self.Product.price 
   

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    is_seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)



class SignupRequest(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class SignupRequestNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='signup_notifications')
    is_seen = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

class UserNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class ProductRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Product = models.ForeignKey(Addproduct, on_delete=models.CASCADE)
    request_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[("Pending", "Pending"), ("Approved", "Approved"), ("Rejected", "Rejected")])
    issued = models.BooleanField(default=False)
    penalty = models.DecimalField(max_digits=10, decimal_places=2, default=0) 
    rental_period = models.PositiveIntegerField() 
    due_date = models.DateField()  # Automatically calculated due date
    overdue = models.CharField(max_length=20)  
    fine_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    overdue_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text="Overdue amount in currency",
    )

    def save(self, *args, **kwargs):
        if not self.request_date:
            self.request_date = timezone.now().date()

        if not self.rental_period:
            self.rental_period = 1  # Use a default value if rental_period is not set

        # Calculate due date based on request date and rental period
        self.due_date = self.request_date + timezone.timedelta(days=self.rental_period)

        # Extract the date part of the due date and current date
        due_date = self.due_date
        today = date.today()  # Get the current date without time

        if today > due_date:
            days_overdue = (today - due_date).days
            overdue_charge_per_day = Decimal('10.00')  # Change this to your desired overdue charge
            overdue_amount = days_overdue * overdue_charge_per_day
            self.status = "Overdue"
            self.overdue = "Overdue"
            self.overdue_amount = overdue_amount
        else:
            self.overdue_amount = Decimal('0.00')

        if today > due_date:
            # Calculate fine based on the number of days overdue
            days_overdue = (today - due_date).days
            overdue_charge_per_day = Decimal('10.00')  
            fine_amount = days_overdue * overdue_charge_per_day
            self.status = "Overdue" 
            self.overdue = "Overdue"  
        else:
            fine_amount = Decimal('0.00')
            #self.status = "Approved"  # Change the status  "Approved"
            self.overdue = "Not Overdue"  # Set 'overdue' to "Not Overdue" when not overdue

        self.fine_amount = fine_amount 

        super(ProductRequest, self).save(*args, **kwargs)
class ProblemReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    issued_Product = models.ForeignKey(ProductRequest, on_delete=models.CASCADE)
    problem_type = models.CharField(max_length=20)
    problem_description = models.TextField()
    fine_amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False) 

    def __str__(self):
        return f"{self.user.username} - {self.problem_type}"
    


class AdminNotification(models.Model):
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)


class OverdueProductNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    Product_title = models.CharField(max_length=255)  
    due_date = models.DateField() 
    is_seen = models.BooleanField(default=False)  

    def __str__(self):
        return f"{self.user.username}'s overdue Product notification"

class ChatMessage(models.Model):
    Product = models.ForeignKey(Addproduct, on_delete=models.CASCADE)
    messages = models.TextField(null=True, blank=True)
    reply = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
