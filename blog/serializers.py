from rest_framework import serializers
from .models import BlogEntry, Category


class BlogEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogEntry
        fields = "__all__"
        lookup_field = "slug" # this tells the serializer to query the database using the "slug" property instead of "id" when passed a param in the urls.py
        
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "category_name",
            "blogentries", # recall that one category can have many entries, so this is how they are linked
        )
        depth = 1        