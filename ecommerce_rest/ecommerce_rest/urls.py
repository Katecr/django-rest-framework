from django.contrib import admin
from django.urls import path, include

from apps.users.views import Login, Logout, UserToken

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('refresh_token/', UserToken.as_view(), name='refresh_token'),
    path('user/', include('apps.users.api.urls')),
    path('products/', include('apps.products.api.routers')),
]
