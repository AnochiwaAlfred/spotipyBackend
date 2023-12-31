from django.db import models
from users.models import CustomUser
from plugins.generate_filename import generate_filename

CLIENT_DISPLAY = ['id', 'email', 'username', 'firstName', 'lastName']
class Client(CustomUser):
    image = models.ImageField(null=True, blank=True, upload_to=generate_filename)
    # favoriteTracks = models.ManyToManyField(
    #     "audio.Track",
    #     blank=True,
    #     related_name="favoriteTracks",
    # )

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    def __str__(self):
        return self.username
    
    def custom_list_display():
        return CLIENT_DISPLAY
