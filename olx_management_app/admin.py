from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Signup)
admin.site.register(Addproduct)
admin.site.register(BookRequest)
admin.site.register(LoginRequest)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(Notification)
admin.site.register(SignupRequest)
admin.site.register(SignupRequestNotification)
admin.site.register(UserNotification)
admin.site.register(ProblemReport)
admin.site.register(AdminNotification)
admin.site.register(OverdueBookNotification)
admin.site.register(ChatMessage)

