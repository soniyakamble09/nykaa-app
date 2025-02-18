from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Categories(models.Model):
    cat = models.CharField(max_length=100, verbose_name='Category Name')
    cimage=models.ImageField(upload_to='image')

class Product(models.Model):
    CAT=((1,'Lipsticks'), (2,'Foundations'), (3,'Compacts'), (4,'Eye-Makeup'), (5,'Nails'), (6,'Makeup'), (7,'Lotions'))
    name=models.CharField(max_length=50, verbose_name='Product Name')
    price=models.FloatField()
    pdetails=models.CharField(max_length=200, verbose_name='Product Details')
    cat=models.IntegerField(verbose_name='Categories', choices=CAT)
    # ForeignKey to Categories
    #cat = models.ForeignKey(Categories, on_delete=models.CASCADE, verbose_name='Category')
    # Dynamically generated choices
    # def get_category_choices():
    #     return [(category.id, category.cat) for category in Categories.objects.all()]
    is_active=models.BooleanField(default=True, verbose_name='Available')
    pimage=models.ImageField(upload_to='image')

    # def __str__(self):
    #     return self.name

class Cart(models.Model):
    uid=models.ForeignKey(User, on_delete=models.CASCADE,db_column="uid")
    pid=models.ForeignKey(Product, on_delete=models.CASCADE,db_column="pid")
    qty=models.IntegerField(default=1)

class Order(models.Model):
    order_id=models.CharField(max_length=50)
    uid=models.ForeignKey(User, on_delete=models.CASCADE,db_column="uid")
    pid=models.ForeignKey(Product, on_delete=models.CASCADE,db_column="pid")
    qty=models.IntegerField(default=1)
    is_deleted=models.BooleanField(default=False, verbose_name='Available')