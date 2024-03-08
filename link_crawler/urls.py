from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from django.contrib.auth.views import LogoutView


# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'links', views.LinkViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('add-links', views.add_links, name='add_links'),
    path('api/', include(router.urls)),
    path('download_report/', views.download_report, name='download_report'),
    path('download-excel-template/', views.download_excel_template, name='download_excel_template'),
    path('handle-actions/', views.handle_actions, name='handle_actions'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
]
