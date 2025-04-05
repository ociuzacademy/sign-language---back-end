from django.db import models

# Create your models here.
class Tbl_User(models.Model):
    username=models.CharField(max_length=20)
    email=models.EmailField(max_length=50)
    phone=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    place=models.CharField(max_length=100,null=True,blank=True)
    address=models.CharField(max_length=255,null=True,blank=True)
    

from django.db import models
 # Use Django's built-in User model if applicable
from django.core.exceptions import ValidationError
from django.utils import timezone
# User = get_user_model()  # Use Django's built-in User model if applicable



class UserLevelProgress(models.Model):
    user = models.ForeignKey(Tbl_User, on_delete=models.CASCADE)
    level = models.ForeignKey('adminapp.Level', on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    score = models.IntegerField(default=0)
    last_attempt = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'level')


class UserAnswer(models.Model):
    user = models.ForeignKey(Tbl_User, on_delete=models.CASCADE)
    question = models.ForeignKey('adminapp.Question', on_delete=models.CASCADE)
    selected_option = models.IntegerField()
    answered_at = models.DateTimeField(auto_now_add=True)
