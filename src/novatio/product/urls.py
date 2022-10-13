from django.urls import path
from django.conf.urls import handler404
from . import views

app_name = "product"
urlpatterns = [
    path('<int:pk>/items/', views.index, name='product'),
]
