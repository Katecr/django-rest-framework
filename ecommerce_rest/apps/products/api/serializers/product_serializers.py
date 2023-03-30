from rest_framework import serializers

from apps.products.models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ('state','created_date','modified_date','delete_date')

    def to_representation(self, intance):
        return {
            'id': intance.id,
            'name': intance.name,
            'description': intance.description,
            'image': intance.image if intance.image else None,
            'measure_unit': intance.measure_unit.description if intance.measure_unit is not None else '',
            'category_product': intance.category_product.description if intance.category_product is not None else ''
        }