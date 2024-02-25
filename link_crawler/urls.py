from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'links', views.LinkViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('add-links', views.add_links, name='add_links'),
    path('api/', include(router.urls)),
    path('download-excel-template/', views.download_excel_template, name='download_excel_template'),
]
