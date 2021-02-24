from django.db import models
from PIL import Image
from django.contrib.auth.models import User


class Product(models.Model):
    PHONE = 'phone'
    LAPTOP = 'laptop'
    PC = 'pc'
    ACC = 'acc'

    CHOICE_GROUP = {
        (PHONE, 'Phone'),
        (LAPTOP, 'Laptop'),
        (PC, 'PersonalComputer'),
        (ACC, 'Accessory'),
    }

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()
    availability = models.BooleanField(default=True)
    group = models.CharField(max_length=20, choices=CHOICE_GROUP, default=PHONE)
    image = models.ImageField(default='no_image.jpg', upload_to='product_image')

    def __str__(self):
        return f'{self.name}'


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True)
    ordering = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ('ordering',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return '/%s/' % {self.slug}


class ConfirmationCode(models.Model):
    code = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    valid_until = models.DateTimeField()

    def __str__(self):
        return self.code