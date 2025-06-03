from django.db import models
from django.contrib.auth.models import \
    AbstractUser
from django.core.validators import RegexValidator


class User(AbstractUser):
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('staff', 'Staff'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    image = models.ImageField(upload_to='users_image',blank=True,
                              null=True)
    
    phone = models.CharField(
        max_length=20,
        validators=[RegexValidator(
            regex=r'^\+375 \(?(25|29|33|44)\)? \d{3}-\d{2}-\d{2}$',
            message="Phone number must be in the format: +375 (29) 123-45-67"
        )],
        blank=True
    )

    birth_date = models.DateField(null=True, blank=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    
    
    class Meta:
        db_table = 'user'
    
    
    def __str__(self):
        return self.username

