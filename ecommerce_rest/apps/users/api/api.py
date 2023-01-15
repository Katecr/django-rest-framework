from rest_framework.response import Response
from rest_framework.views import APIView
from apps.users.api.serializers import User
from apps.users.api.serializers import UserSerializer

#Decorador @APIVIEW
from rest_framework.decorators import api_view

# para manejar estados http
from rest_framework import status

class UserAPIView(APIView):
    
    def get(self, request):
        users = User.objects.all()
        users_serializer = UserSerializer(users, many = True)
        return Response(users_serializer.data, status= status.HTTP_200_OK)

@api_view(['GET','POST'])
def user_api_view(request):
    #list
    if request.method == 'GET':
        #queryset
        users = User.objects.all()
        users_serializer = UserSerializer(users, many = True)
        return Response(users_serializer.data, status= status.HTTP_200_OK)
    #create
    elif request.method == 'POST':
        user_serializer = UserSerializer(data = request.data)
        #validation
        if user_serializer.is_valid():
            user_serializer.save()
            return Response({'message': 'user created'}, status= status.HTTP_201_CREATED)

        return Response(user_serializer.errors, status= status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT', 'DELETE'])
def user_detail_view(request, pk =None):
    #queryset
    user = User.objects.filter(id=pk).first()
    #validation
    if user:
        if request.method == 'GET':
            if pk is not None:
                user_serializer = UserSerializer(user)
                return Response(user_serializer.data, status= status.HTTP_200_OK)
        # update    
        elif request.method == 'PUT':
            user_serializer = UserSerializer(user, data = request.data)
            if user_serializer.is_valid():
                user_serializer.save()
                return Response(user_serializer.data, status= status.HTTP_200_OK)
            return Response(user_serializer.errors, status= status.HTTP_400_BAD_REQUEST)
        #delete
        elif request.method == 'DELETE':
            user.delete()
            return Response({'message': 'user deleted correct'}, status= status.HTTP_200_OK)
    else:
        return Response({'message':'user not found'}, status= status.HTTP_400_BAD_REQUEST)