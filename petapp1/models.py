#from tkinter import CASCADE
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.contrib.auth.models import AbstractUser

# Create your models here.
class PetUser(AbstractUser):
    fname = models.CharField(max_length=30)
    lname = models.CharField(max_length=30)
    email1 = models.CharField(max_length=50)
    phone1 = models.CharField(max_length=14)
    address1 = models.CharField(max_length=100)

    def __str__(self):
        return self.username


class PetManager(models.Manager):
    def search(self, query):
        if query: 
            return self.get_queryset().filter(models.Q(name__exact=query)|models.Q(breed__exact=query))


class Pet(models.Model):
    name = models.CharField(max_length=20, validators=[RegexValidator(regex=r'^[a-zA-Z\s]+$', message=("Name can contain only alphabets and spaces"), code="invalid_name")])
    breed = models.CharField(max_length=30,)
    age = models.IntegerField(validators=[MinValueValidator(1, message=("The minimun age value for pet is 1 years")), MaxValueValidator(15, message=("The maximum age for pet is 15 years."))])
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(10000, message=("The minimum priced pet should be 10000 rupees."))])
    type = models.CharField(max_length=10)
    description = models.CharField(max_length=100)
    image = models.ImageField(upload_to='pet_images/', blank=True, null=True)

    objects = PetManager()

    # adding certain permission 
    class Meta:
        permissions = [
            ('can_add_pet', 'Can add a pet'), 
            ('can_update_pet', 'Can update a pet')
        ]

class Product(models.Model):
    product_name = models.CharField(max_length=20, validators=[RegexValidator(regex=r'^[a-zA-Z\s]+$', message=("Product Name can contain only alphabets and spaces"), code="invalid_product_name")])
    category = models.CharField(max_length=15)
    price = models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(1000, message=("The minimum priced pet product should be 1000 rupees."))] )
    quantity_in_stock = models.IntegerField()
    description = models.CharField(max_length=100)
    image = models.ImageField(upload_to='product_images/')

class Order(models.Model):
    user_id = models.ForeignKey(PetUser, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    PAYMENT_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]
    payment_status = models.CharField(
        max_length=10, choices=PAYMENT_STATUS_CHOICES, default='PENDING'
    )
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)

class OrderItem(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    pet_id = models.ForeignKey(Pet, on_delete=models.CASCADE, blank=True, null=True)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Cart(models.Model):
    customer_id = models.ForeignKey(PetUser, on_delete=models.CASCADE)
    pet_id = models.ForeignKey(Pet, on_delete=models.CASCADE, null=True, blank=True)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField()
    date_added = models.DateTimeField()

class Payments(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_date = models.DateTimeField()
    payment_method = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"