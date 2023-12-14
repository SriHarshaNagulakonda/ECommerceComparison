import random
import re
from collections import defaultdict

from rest_framework import generics

from .constants import products
from .models import Product, Company
from .serializers import ProductSerializer, CompanySerializer, SearchProductSerializer, GroupedProductSerializer
from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class NewProduct(generics.CreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class ProductDetailsView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    lookup_field = 'id'


class ProductsView(generics.ListAPIView):
    serializer_class = GroupedProductSerializer
    queryset = Product.objects.all()
    pagination_class = CustomPagination

    def get_queryset(self):
        search_query = self.request.query_params.get('search', None)
        sort_key = self.request.query_params.get('sort', None)
        companies = self.request.query_params.get('company')

        if not companies or len(companies) == 0:
            companies = list(Company.objects.all().values_list('name', flat=True))
        else:
            companies = companies.split(',')
        base_queryset = Product.objects.select_related('company').all()

        if search_query:
            search_words = search_query.split()

            grouped_products = defaultdict(list)
            for product in base_queryset:
                for word in search_words:
                    if (product.company.name in companies) and len(word)>1 and (
                            (word.lower() in product.title.lower()) or (word.lower() in product.category.lower())):
                        grouped_products[product.title].append({
                            "id": product.id,
                            "title": product.title,
                            "url": product.url,
                            "total_review_count": product.total_review_count,
                            "rating": str(product.rating),
                            "price": product.price,
                            "category": product.category,
                            "company": str(product.company.name),
                            "company_image": str(product.company.image)
                        })

            results = [{"title": title, "products": products} for title, products in grouped_products.items()]
            if sort_key:
                for each_row in results:
                    products = each_row["products"]
                    if (sort_key == "highest_price"):
                        products.sort(key=lambda group: group["price"], reverse=True)
                    elif sort_key == "lowest_price":
                        products.sort(key=lambda group: group["price"])
                    elif sort_key == "highest_rating":
                        products.sort(key=lambda group: float(group["rating"]), reverse=True)

            if (sort_key == "highest_price"):
                results.sort(key=lambda group: group["products"][0]["price"], reverse=True)
            elif sort_key == "lowest_price":
                results.sort(key=lambda group: group["products"][0]["price"])
            elif sort_key == "highest_rating":
                results.sort(key=lambda group: float(group["products"][0]["rating"]), reverse=True)
            return results

        return []


class NewCompany(generics.CreateAPIView):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()


class CompanyDetailsView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()
    lookup_field = 'id'


class CompanyView(generics.ListAPIView):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()


class GenerateData(generics.ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):
        companies = list(Company.objects.all().values_list('id', flat=True))

        total_created = 0
        for count in range(100):
            category = random.choice(list(products.keys()))
            company = Company.objects.get(id=random.choice(companies))

            title = random.choice(products[category])
            url = company.website + "-".join(title.lower().split()) + "/"
            url = re.sub(r'-{2,}', '-', url)
            random_digit = random.randint(3, 6)
            total_review_count = random.randint(10 ** random_digit, 10 ** (random_digit + 1))
            rating = random.randint(total_review_count * 1, total_review_count * 5) / total_review_count
            price = random.randint(len(url) * 100, len(url) * 500)

            if (Product.objects.filter(url=url, company__id=company.id).count() > 0):
                continue

            product = Product(category=category, title=title, company=company, price=price, url=url, rating=rating,
                              total_review_count=total_review_count)
            product.save()
            total_created += 1
        return super().get(request, *args, **kwargs)
