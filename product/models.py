from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.forms import ModelForm
from django.urls import reverse
from django.utils.safestring import mark_safe
from ckeditor_uploader.fields import RichTextUploadingField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Category(MPTTModel):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    title = models.CharField(max_length=100)
    keywords = models.CharField(blank=True, max_length=255)
    description = models.CharField(blank=True, max_length=255)
    image = models.ImageField(blank=True, upload_to='images/')
    status = models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField(null=False, unique=True)
    parent = TreeForeignKey('self',blank=True,null=True,related_name='children',on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by = ['title']


    def __str__(self):
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' / '.join(full_path[::-1])




    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'


    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})




class Product(models.Model):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE) #relation with Category table
    title = models.CharField(max_length=150)
    keywords = models.CharField(blank=True, max_length=255)
    description = models.CharField(blank=True, max_length=255)
    image = models.ImageField(blank=True, upload_to='images/')
    price = models.FloatField()
    amount = models.IntegerField()
    detail = RichTextUploadingField()
    slug = models.SlugField(null=False, unique=True)
    status = models.CharField(max_length=10, choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})


class Images(models.Model):
        product = models.ForeignKey(Product, on_delete=models.CASCADE)
        title = models.CharField(max_length=50,blank=True)
        image = models.ImageField(blank=True, upload_to='images/')
        def __str__(self):
            return self.title

        def image_tag(self):
            return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
        image_tag.short_description = 'Image'


class Comment(models.Model):
    STATUS = (
        ('New', 'Yeni'),
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    comment = models.CharField(max_length=200, blank=True)
    rate = models.IntegerField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=20)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject



class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['subject', 'comment', 'rate']



class Reservation(models.Model):
    STATUS = (
        ('New', 'Yeni'),
        ('Accepted', 'Onaylandı'),
        ('Canceled', 'Reddedildi'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(blank=True, max_length=25)
    email = models.CharField(blank=True, max_length=50)
    phone = models.CharField(blank=True, max_length=20)
    address = models.CharField(blank=True, max_length=200)
    location = models.CharField(blank=True, max_length=70)
    days = models.IntegerField()
    checkin = models.DateField(null=True)
    checkout = models.DateField(null=True)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=25)
    message = models.CharField(blank=True, max_length=255)
    note = models.CharField(blank=True, max_length=100)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.product.title

    @property
    def total(self):
        return self.days * self.product.price

    @property
    def price(self):
        return self.product.price


class ReservationForm(ModelForm):
    class Meta:
        model = Reservation
        fields = ['name', 'email', 'phone', 'address', 'location', 'checkin', 'checkout', 'days']