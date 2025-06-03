from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit
from imagekit.processors import Transpose  # Auto-rotate based on EXIF

def validate_image_size(value):
    """Validate that image size doesn't exceed 3MB"""
    limit = 3 * 1024 * 1024  
    if value.size > limit:
        raise ValidationError('Image too large. Maximum size is 3MB.')

class CustomUser(AbstractUser):
    pass

class ClockType(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = ProcessedImageField(
        upload_to='clock_images/',
        blank=True,
        null=True,
        validators=[validate_image_size],
        processors=[
            Transpose(),  # Auto-rotate based on EXIF data
            ResizeToFit(1200, 1200)  # Resize to fit within 1200x1200
        ],
        format='JPEG',
        options={'quality': 80},  # Optimized quality/size ratio
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Stock(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    clock_type = models.ForeignKey(ClockType, on_delete=models.CASCADE)
    quantity_received = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    defective_quantity = models.PositiveIntegerField(default=0)
    date_received = models.DateTimeField(auto_now_add=True)
    
    def clean(self):
        if self.defective_quantity > self.quantity_received:
            raise ValidationError("Defective quantity cannot exceed received quantity")
    
    def good_quantity(self):
        return self.quantity_received - self.defective_quantity
    
    def __str__(self):
        return f"{self.clock_type.name} - {self.quantity_received} units"

class Sale(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    clock_type = models.ForeignKey(ClockType, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    sale_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.quantity} {self.clock_type.name} sold on {self.sale_date}"

class Return(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    clock_type = models.ForeignKey(ClockType, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    return_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.quantity} {self.clock_type.name} returned on {self.return_date}"