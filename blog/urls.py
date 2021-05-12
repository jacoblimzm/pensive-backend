from django.urls import path
from .views import BlogEntryListView, BlogEntryDetailView, BlogEntryBreakingView, CategoryListView, CategoryDetailView
from . import views

urlpatterns = [
    path("", views.BlogEntryListView.as_view()),
    path("new/", views.BlogEntryCreateView.as_view()),
    path("breaking/", views.BlogEntryBreakingView.as_view()),
    path("categories/", views.CategoryListView.as_view()),
    path("categories/<category_name>", views.CategoryDetailView.as_view()),
    path("edit/<slug>", views.BlogEntryEditView.as_view()),
    path("<slug>/", views.BlogEntryDetailView.as_view()),
]
