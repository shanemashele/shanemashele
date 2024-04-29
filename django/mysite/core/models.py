from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver






class Category(models.Model):
    name = models.CharField(max_length=255)
  

    def __str__(self):
        return self.name


class Cloth(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=225,default='', blank=True, null='')
    image = models.ImageField(upload_to='uploads/product/')
    is_active = models.BooleanField(default=True) 
    quantity = models.PositiveIntegerField(default=1)
    
        
    def __str__(self):
        return self.name



class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    address =models.CharField(max_length=300,blank=True, null=True)
    country =models.CharField(max_length=255,blank=True, null=True)
    city=models.CharField(max_length=255,blank=True, null=True)
    zipcode=models.CharField(max_length=15,blank=True, null=True)
    phone =models.CharField(max_length=16,blank=True, null=True)
    
    def register(self): 
        self.save() 
  
    
@receiver(post_save, sender=User)
def create_or_update_customer(sender, instance, created, **kwargs):
    """
    Signal handler to create or update a Customer instance whenever a User instance is saved.
    """
    if created:
        Customer.objects.create(user=instance)
    else:
        try:
            instance.customer.save()
        except Customer.DoesNotExist:
            # Log the exception or handle it gracefully
            pass
        
        
ADDRESS_TYPE = (
    ("ship","shipping"),
    ("bill","billing"),
)

class CustomerAddress(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.PROTECT)
    address_type = models.CharField(max_length=10, choices=ADDRESS_TYPE, default="ship")
    street_address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.PositiveIntegerField(null=True, blank=True)
    country = models.CharField(max_length=200, default='South Africa')
    default = models.BooleanField(default=False)
    is_active = models.BooleanField(blank=True)

    def __str__(self):
        return f"{self.postal_code} {self.country}"


class Cart(models.Model):
      cloth= models.ForeignKey(Cloth,on_delete=models.CASCADE)
      image = models.ImageField(null=True,blank=True)
      quantity= models.PositiveIntegerField(default=1)
      price =models.IntegerField(default=0) 
      
      def clear_cart(self):
        # Delete all items associated with the cart
        self.delete()

      
      
class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    crown = models.CharField(max_length=100, blank=True)
    shoulder = models.CharField(max_length=100, blank=True)
    chest = models.CharField(max_length=100, blank=True)
    waist = models.CharField(max_length=100, blank=True)
    hips = models.CharField(max_length=100, blank=True)
    inseam = models.CharField(max_length=100, blank=True)
    floor = models.CharField(max_length=100, blank=True)
      
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cloth = models.ForeignKey(Cloth, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    image = models.ImageField(upload_to='uploads/')

    def __str__(self):
        return f"{self.quantity} of {self.cloth.name} in {self.user.username}'s cart"
    




class Measurement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crown = models.FloatField(help_text="In cm")
    shoulder = models.FloatField(help_text="In cm")
    chest = models.FloatField(help_text="In cm")
    waist = models.FloatField(help_text="In cm")
    hips = models.FloatField(help_text="In cm")
    inseam = models.FloatField(help_text="In cm")
    floor = models.FloatField(help_text="In cm")
    icon = models.ImageField(upload_to='measurement_icons/', null=True, blank=True)

    def __str__(self):
        return f"Measurement by {self.user.username} - Crown: {self.crown}cm, Shoulder: {self.shoulder}cm, Chest: {self.chest}cm, Waist: {self.waist}cm, Hips: {self.hips}cm, Inseam: {self.inseam}cm, Floor: {self.floor}cm"



class UploadedImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/')
 
class Order(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=25)
    cloth = models.ManyToManyField(Cloth)
    quantities = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    checkout = models.BooleanField(default=False)
    payment_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.order_number}"
class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    cloth = models.ForeignKey(Cloth, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.quantity} x {self.cloth.name} in Order {self.order.order_number}"
from django.utils import timezone  
class Shipping(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    tracking_number = models.CharField(max_length=100)
    shipping_method = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)
    
    # Add more fields as needed (e.g., shipping address, shipping date, etc.)

    def __str__(self):
        return f"Shipping for Order {self.order_id}"
