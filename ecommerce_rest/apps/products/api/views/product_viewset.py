from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.products.api.serializers.product_serializers import ProductSerializer
from apps.users.authentication_mixins import Authentication

class ProductViewSet(Authentication, ModelViewSet):
    serializer_class = ProductSerializer
    queryset = ProductSerializer.Meta.model.objects.filter(state = True)

    def get_queryset(self,pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(state = True)
        else:
            return self.get_serializer().Meta.model.objects.filter(id = pk, state = True).first()
    
    def list(self, request):
        product_serializer = self.get_serializer(self.get_queryset(), many = True)
        return Response(product_serializer.data, status = status.HTTP_200_OK)
    
    def create(self, request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Product created successfully!'},status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def destroy(self,request,pk=None):
        product = self.get_queryset().filter(id = pk).first()
        if product:
            product.state = False
            product.save()
            return Response({'message':'Product deleted successfully!'}, status = status.HTTP_200_OK)
        return Response({'error':'Product does not exist'}, status = status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, pk= None):
        product = self.get_queryset().filter(id=pk).first()
        if product:
            product_serializer = self.serializer_class(product)
            return Response(product_serializer.data, status = status.HTTP_200_OK)
        return Response({'error':'Product does not exist'}, status = status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk= None):
        if self.get_queryset(pk):
            product_serializer = self.serializer_class(self.get_queryset(pk), data = request.data)
            if product_serializer.is_valid():
                product_serializer.save()
                return Response(product_serializer.data, status = status.HTTP_200_OK)
            return Response(product_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        return Response({'error':'Product does not exist'}, status = status.HTTP_400_BAD_REQUEST)

