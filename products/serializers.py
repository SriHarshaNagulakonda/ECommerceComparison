from rest_framework import serializers

from .models import Product, Company


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

class SearchProductSerializer(serializers.ModelSerializer):
    company = serializers.CharField()
    company_image = serializers.CharField()
    class Meta:
        model = Product
        fields = "__all__"

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"

class GroupedProductSerializer(serializers.Serializer):
    title = serializers.CharField()
    products = SearchProductSerializer(many=True)
