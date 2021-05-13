from django.urls import path
from . import views # import the FUNCTIONS from views.py in the same level folder. which serve up the html files

# path("",) here will BUILD on the BASE URL defined in urls.py in project folder
# think of this as the tunr.get(), tunr.post().

# what is IMPORTANT here is that what you assign to "name" will be what you use in <a> tags in HTML to link to other HTMLs
# this is to create a 'once source of truth' for your paths, in case the path is used many times across the app

urlpatterns = [
    path("<str:room_name>/", views.chat_room, name="chat_room")
]