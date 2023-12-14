from django.db import models
import uuid

from .validators import is_valid_url, is_valid_rating, is_valid_price

class Product(models.Model):
    id = models.CharField(primary_key=True, default=uuid.uuid4, max_length=36)
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=1000, validators=[is_valid_url])
    total_review_count = models.IntegerField()
    rating = models.DecimalField(decimal_places=1, max_digits=2, validators=[is_valid_rating])
    price = models.IntegerField(validators=[is_valid_price])
    category = models.CharField(max_length=100)
    company = models.ForeignKey('Company', on_delete=models.CASCADE)

    def __str__(self):
        return self.title+" "+self.company.name

class Company(models.Model):
    id = models.CharField(primary_key=True, default=uuid.uuid4, max_length=36)
    name = models.CharField(max_length=30, unique=True)
    website = models.CharField(max_length=100, validators=[is_valid_url])
    image = models.CharField(max_length=1000)

    def __str__(self):
        return self.name

