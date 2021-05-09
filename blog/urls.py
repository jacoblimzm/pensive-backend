from django.urls import path
from .views import BlogEntryListView, BlogEntryDetailView, CategoryListView, CategoryDetailView

urlpatterns = [
    path("", BlogEntryListView.as_view()),
    path("categories", CategoryListView.as_view()),
    path("categories/<category_name>", CategoryDetailView.as_view()),
    path("<slug>", BlogEntryDetailView.as_view()),
]
