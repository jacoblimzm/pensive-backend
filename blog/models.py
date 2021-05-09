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
        ("WORLD", "World"), # first element is the actual value to be set on the model, the second element is the human readable name
        ("ENVIRONMENT", "Environment"),
        ("TECHNOLOGY", "Technology"),
        ("DESIGN", "Design"),
        ("CULTURE", "Culture"),
        ("TRAVEL", "Travel"),
        ("STYLE", "Style"),
        ("HEALTH", "Health"),
        ("SCIENCE", "Science"),
        ("OPINION", "Opinion"),
        ("POLITICS", "Politics"),
        ("BUSINESS", "Business"),
    ]
    category_name = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default="World",
    )
    
    def __str__(self):
        return self.category_name
    
