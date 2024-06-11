from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from common.views import CreateUserView, ObtainTokenView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path('api/auth/registration/', CreateUserView.as_view(), name='registration'),
    path('api/auth/token/', ObtainTokenView.as_view(), name='token'),

    path('api/', include('books.urls')),
    path('api/', include('orders.urls')),
]
