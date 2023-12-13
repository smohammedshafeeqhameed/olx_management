from .models import Signup

def counter(request):
    count = 0
    user = request.user  # Assuming you want to access the current user

    # Count the number of objects that meet your criteria
    var = Signup.objects.filter(role='user', status=0)
    count = var.count()

    # You can also count var1 if it's defined and meets certain criteria
    # var1 = YourModel.objects.filter(...)  # Replace YourModel and filter criteria
    # count += var1.count()

    return {'count': count}
