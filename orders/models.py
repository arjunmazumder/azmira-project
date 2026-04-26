from django.db import models
from django.db import models
from django.conf import settings
from projects.models import Property  # Assuming Property is in the same app
from cloudinary.models import CloudinaryField


#---------------Booking Model--------------------------------
class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    property = models.OneToOneField(Property, on_delete=models.CASCADE, related_name='booking_details')
    
    # Financials based on contract
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    token_money = models.DecimalField(max_digits=12, decimal_places=2, help_text="Initial advance [cite: 237]")
    down_payment = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    # Installment Logic [cite: 233, 239]
    installment_duration_months = models.PositiveIntegerField(default=10)
    monthly_installment_amount = models.DecimalField(max_digits=12, decimal_places=2)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    booking_date = models.DateTimeField(auto_now_add=True)
    
    # Automation tracking 
    token_expiration_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Auto-calculate installment if not set [cite: 53]
        if not self.monthly_installment_amount:
            remaining = self.total_amount - self.token_money - self.down_payment
            self.monthly_installment_amount = remaining / self.installment_duration_months
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking: {self.property.title} by {self.user.email}"
    
#----------------------Installment---------------------------------------
class Installment(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='installments')
    due_date = models.DateField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    payment_date = models.DateField(null=True, blank=True)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Installment for {self.booking.property.unit_number} - Due: {self.due_date}"
