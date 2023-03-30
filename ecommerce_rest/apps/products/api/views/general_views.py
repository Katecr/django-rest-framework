from rest_framework.viewsets import ModelViewSet

from apps.products.api.serializers.general_serializer import MeasureUnitSerializer,IndicatorSerializer, CategoryProductSerializer


class MeasureUnitViewSet(ModelViewSet):
    serializer_class = MeasureUnitSerializer
    queryset = MeasureUnitSerializer.Meta.model.objects.filter(state = True)
    

class IndicatorViewSet(ModelViewSet):
    serializer_class = IndicatorSerializer
    queryset = IndicatorSerializer.Meta.model.objects.filter(state = True)
    

class CategoryProductViewSet(ModelViewSet):
    serializer_class = CategoryProductSerializer
    queryset = CategoryProductSerializer.Meta.model.objects.filter(state = True)

    
    