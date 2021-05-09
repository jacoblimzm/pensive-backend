from django.shortcuts import render
from rest_framework import permissions, generics, status
from rest_framework.response import Response
from django.http import JsonResponse

from .models import BlogEntry, Category
from .serializers import BlogEntrySerializer, CategorySerializer

from django.contrib.auth.models import User # the default User model from django
from django.contrib.auth import authenticate, login



class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.AllowAny,)   
    
class CategoryDetailView(generics.RetrieveAPIView): 
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "category_name" # returns the individual category along with all related posts
    permission_classes = (permissions.AllowAny,)

class BlogEntryListView(generics.ListAPIView):
    queryset = BlogEntry.objects.order_by("-created_on")
    serializer_class = BlogEntrySerializer
    lookup_field = "slug" # this tells the view class to lookup the list of posts using the "slug" property instead of the usual pk
    permission_classes = (permissions.AllowAny,)

class BlogEntryDetailView(generics.RetrieveAPIView): # "retrieveAPIview" always needs a lookup field which must correspond to the url param in urls.py. retrive is a specific search for 1 it
    queryset = BlogEntry.objects.order_by("-created_on")
    serializer_class = BlogEntrySerializer
    lookup_field = "slug"
    permission_classes = (permissions.AllowAny,)
    
class BlogEntryBreakingView(generics.ListAPIView):
    queryset = BlogEntry.objects.all().filter(breaking=True)
    serializer_class = BlogEntrySerializer
    lookup_field = "slug"
    permission_classes = (permissions.AllowAny,)
    
class BlogEntryCreateView(generics.ListCreateAPIView):
    
    """
    POST new/
    """
    
    queryset = BlogEntry.objects.all()
    serializer_class = BlogEntrySerializer
    permission_classes = (permissions.AllowAny,)
    
    def post(self, request, *args, **kwargs):
        
        
        # "slug" and "created_at" not necessary since those will be automatically generated on save
        title = request.data.get("title")
        image = request.data.get("image")
        excerpt = request.data.get("excerpt")
        month = request.data.get("month") # should be a dropdown in frontend with THREE LETTER MONTHS
        day = request.data.get("day") # should be a dropdown in frontend with DIGIT DAYS
        content = request.data.get("content") 
        breaking = request.data.get("breaking") # boolean. drop down in FRONTEND
        category = request.data.get("category") # should be a dropdown in frontend with uncapped category names
        # print(request.data["title"])
        # print(title, image, excerpt, month, day, content, breaking, category)
        if not request.data:
            return Response(data={
                    "success": False,
                    "message": "no data received"
                    }
            )
        elif not title or not image or not excerpt or not month or not day or not content or not category: # cannot include "breaking" here as it will mess up the conditional
            return Response(data={
                    "success": False,
                    "message": "ensure all fields are filled in!"
                }
            )
        
        else:
            # category_instance = Category(category_name=category)
            # print(category_instance["id"])
            # request.data["category"] = category_instance
            # print(request.data["category"])
            category_result = Category.objects.get(category_name__iexact = category) # search database to get back categories and their respective id
            category_id = category_result.id
            # print(category_id)
            new_entry = BlogEntry(title=title, image=image, excerpt=excerpt, month=month, day=day, content=content, breaking=breaking, category_id=category_id)
            # print(new_entry.category_id)
            new_entry.save()
            
            return Response(data={
                "success": True,
                "message": f"{new_entry.title} has been created successfully!"
            }, status=status.HTTP_201_CREATED)
    
    
    
    ## Create Blog Edit/Update/Delete View
    

class BlogEntryEditView(generics.RetrieveUpdateDestroyAPIView):
    
    queryset = BlogEntry.objects.order_by("-created_on")
    serializer_class = BlogEntrySerializer
    lookup_field = "slug"
    permission_classes = (permissions.AllowAny,)
    
    def put(self, request, *args, **kwargs):
        # "slug" and "created_at" not necessary since those will be automatically generated on save
        entry_id = request.data.get("id")
        title = request.data.get("title")
        image = request.data.get("image")
        excerpt = request.data.get("excerpt")
        month = request.data.get("month") # should be a dropdown in frontend with THREE LETTER MONTHS
        day = request.data.get("day") # should be a dropdown in frontend with DIGIT DAYS
        content = request.data.get("content") 
        breaking = request.data.get("breaking") # boolean. drop down in FRONTEND
        category = request.data.get("category") # should be a dropdown in frontend with uncapped category names
        print(entry_id)
        # print(title, image, excerpt, month, day, content, breaking, category)
        if not request.data:
            return Response(data={
                    "success": False,
                    "message": "no data received"
                    }
            )
        elif not title or not image or not excerpt or not month or not day or not content or not category: # cannot include "breaking" here as it will mess up the conditional
            return Response(data={
                    "success": False,
                    "message": "ensure all fields are filled in!"
                }
            )
        
        else:
            existing_post = BlogEntry.objects.get(pk=entry_id)
            category_result = Category.objects.get(category_name__iexact = category) # search database to get back categories and their respective id
            category_id = category_result.id # with the new updated category, need to find the id and assign it accordingly
            
            existing_post.title = title
            existing_post.image = image
            existing_post.excerpt = excerpt
            existing_post.month = month
            existing_post.day = day
            existing_post.content = content
            existing_post.breaking = breaking
            existing_post.category_id = category_id # the django model automatically assigns and _id to a foreign key. remember to include
            
            serializer = BlogEntrySerializer(existing_post) # serialise the updated data to be sent back to the front end
            # print(serializer.data)
            # print(existing_post.category_id) 
            # existing_post.save()
            
            
            return Response(data={
                "data": serializer.data,
                "success": True,
                "message": f"'{title}' has been updated!",
                
            })
            
            # return JsonResponse(existing_post.values("title"), safe=False)
        
    