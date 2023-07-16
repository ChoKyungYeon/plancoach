
from django.db import models
from multiselectfield import MultiSelectField

from plancoach.choice import consulttypechoice
from profileapp.models import Profile



class Profile_consulttype(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='profile_consulttype')
    consulttype = MultiSelectField(max_length=20, choices=consulttypechoice)
    content = models.TextField(max_length=1000)


    def consulttype_name(self):
        return ', '.join(self.consulttype)
