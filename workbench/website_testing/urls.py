from django.urls import path
from . import views

app_name = 'website_testing'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('create/', views.create_test, name='create'),
    path('test/<int:pk>/', views.test_detail, name='detail'),
    path('test/<int:pk>/status/', views.test_status, name='status'),
    path('test/<int:pk>/rerun/', views.rerun_test, name='rerun'),
    path('test/<int:pk>/delete/', views.delete_test, name='delete'),
    path('compare/', views.compare_tests, name='compare'),
    path('report/<int:pk>/', views.public_report, name='public_report'),
]