from django.urls import path
from .views import BlogEntryListView, CategoryListView

urlpatterns = [
    path("", BlogEntryListView.as_view()),
    
]
