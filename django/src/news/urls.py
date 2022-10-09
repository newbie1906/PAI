from django.urls import path, include
from .views import index, add, get, update

urlpatterns = [
    path('', index, name="view_news"),
    path('add/', add, name="add"),
    path('<int:id>/', get, name='get'),
    path('<int:id>/update', update, name='update'),
]
