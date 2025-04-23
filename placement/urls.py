from django.contrib import admin
from django.urls import path, include
from placeapp import views as placeapp_views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', placeapp_views.home_view, name='home'),  # Default route to home view
    path('accounts/', include('placeapp.urls')),       # For signup, login, etc.
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)