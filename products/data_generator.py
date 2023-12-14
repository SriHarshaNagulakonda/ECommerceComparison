from .models import Product, Company


companies = Company.objects.all()
print(companies)