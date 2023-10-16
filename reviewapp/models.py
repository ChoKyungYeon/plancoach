from django.db import models

from accountapp.models import CustomUser
from plancoach.choice import agechoice


# Create your models here.
class Review(models.Model):
    customuser = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='review')
    image = models.ImageField(upload_to='review/', null=True, blank=True)
    content = models.TextField(max_length=200)
    userrealname = models.CharField(max_length=6,null=True)
    age = models.CharField(max_length=20, choices=agechoice ,null=True)
    created_at = models.DateField(null=True)


    def safe_username(self):
        return f"{self.userrealname[:1]}00"

    def review_age(self):
        age_display = self.get_age_display()
        age_output_map = {
            'N수': '무소속/ N수',
            '1학년': '고등학교 1학년',
            '2학년': '고등학교 2학년',
            '3학년': '고등학교 3학년',
            '중등': '중학생',
        }
        return age_output_map.get(age_display, 'Unknown Age')