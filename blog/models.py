from django.db import models
from datetime import datetime
from django.utils.timezone import timezone
from django.template.defaultfilters import slugify 
# slug is a newspaper term
# slugify converts a string to ASCII which makes it compatible with urls
# something similar to encodeURI() in javascript
# Create your models here.

class Category(models.Model):
    CATEGORY_CHOICES = [
        ("world", "World"), # first element is the actual value to be set on the model, the second element is the human readable name
        ("environment", "Environment"),
        ("technology", "Technology"),
        ("design", "Design"),
        ("culture", "Culture"),
        ("travel", "Travel"),
        ("style", "Style"),
        ("health", "Health"),
        ("science", "Science"),
        ("opinion", "Opinion"),
        ("politics", "Politics"),
        ("business", "Business"),
    ]
    category_name = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default="World",
    )
    
    def __str__(self):
        return self.category_name
    
class BlogEntry(models.Model):
    JAN = "JAN"
    FEB = "FEB"
    MAR = "MAR"
    APR = "APR"
    MAY = "MAY"
    JUN = "JUN"
    JUL = "JUL"
    AUG = "AUG"
    SEP = "SEP"
    OCT = "OCT"
    NOV = "NOV"
    DEC = "DEC"
    MONTH_CHOICES = [
        (JAN, "January"),
        (FEB, "February"),
        (MAR, "March"),
        (APR, "April"),
        (MAY,"May"),
        (JUN,"June"),
        (JUL,"July"),
        (AUG,"August"),
        (SEP,"September"),
        (OCT,"October"),
        (NOV,"November"),
        (DEC,"December"),
    ]
    title = models.CharField(max_length=50)
    slug = models.SlugField() # https://docs.djangoproject.com/en/3.2/ref/models/fields/#slugfield slugfield is a term used by news organisations
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="blogentries"
    )
    image = models.URLField(max_length=500) # accepts url fields to be placeholders for blog posts
    excerpt = models.CharField(max_length=150)
    month = models.CharField(max_length=3, choices=MONTH_CHOICES)
    day = models.CharField(max_length=2)
    content = models.TextField()
    breaking = models.BooleanField(default=False) # we only want 1 post to be breaking at any one time
    created_on = models.DateTimeField(default=datetime.now, blank=True)
    
    def save(self, *args, **kwargs): # overriding the default save behaviour with some custom logic
        original_slug = slugify(self.title)
        queryset = BlogEntry.objects.all().filter(slug__iexact=original_slug).count() # count how many posts in the db have the same title
        if queryset == 0:
            self.slug = original_slug
        else:
            count = 1
            while(queryset):
                new_slug = original_slug + "-" + str(count)
                count += 1
                queryset = BlogEntry.objects.all().filter(slug__iexact=new_slug).count()
                
            # self.slug = original_slug + "-" + str(queryset + 1)
            # new_slug += str(count)
            self.slug = new_slug 
        
              
        if self.breaking: # if the new entry "breaking" is true, we want to make sure any other "breaking" post is reverted to False
            try:
                query = BlogEntry.objects.get(breaking=True)
                if self != query: # make sure the post returned is NOT the same as the one being saved
                    query.breaking = False
                    query.save()
            except BlogEntry.DoesNotExist:
                pass
            
        super(BlogEntry, self).save(*args, **kwargs) 
        # It’s important to remember to call the superclass method – super().save(*args, **kwargs) – to ensure that the object still gets saved into the database
    def __str__(self):
        return self.title