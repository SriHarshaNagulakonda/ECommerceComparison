from django.urls import path

from .views import ProductsView, NewProduct, ProductDetailsView, CompanyDetailsView, NewCompany, CompanyView, \
    GenerateData

urlpatterns = [
    path('products/', ProductsView.as_view()),
    path("products/create/", NewProduct.as_view(), name="index"),
    path('products/<str:id>>/', ProductDetailsView.as_view(), name=""),
    path('company/', CompanyView.as_view(), name=""),
    path('company/create/', NewCompany.as_view()),
    path('company/<str:id>/', CompanyDetailsView.as_view()),
    path('generate_data/', GenerateData.as_view()),
]
