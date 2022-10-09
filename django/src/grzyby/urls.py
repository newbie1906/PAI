from django.urls import path, include
from grzyby.views import index, update, add, delete

urlpatterns = [
    path('', index, name="grzyby_index"),
    path('add/', add, name="grzyby_add"),
    path('<int:id>/update/', update, name="grzyby_update"),
    path('<int:id>/delete/', delete, name="grzyby_delete"),

    ]