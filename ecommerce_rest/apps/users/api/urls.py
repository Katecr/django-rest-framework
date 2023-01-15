from django.urls import path
from apps.users.api.api import UserAPIView, user_api_view, user_detail_view


urlpatterns = [
    path('', UserAPIView.as_view(), name="user"),
    path('user_function/', user_api_view, name="user_function"),
    path('user_function/<int:pk>/', user_detail_view, name="user_detail")
]
