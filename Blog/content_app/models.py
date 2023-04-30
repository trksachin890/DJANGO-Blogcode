from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    date=models.DateField(auto_now_add=True)
    auther=models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title