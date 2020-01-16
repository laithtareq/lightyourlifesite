from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from PIL import Image
# Create your models here.
class Profile(models.Model):
    image = models.ImageField(default='default.jpg',upload_to='profiles')
    phone = models.CharField(max_length=14,default='')
    email = models.CharField(default='None', max_length=50)
    isAdmin = models.BooleanField(default=False)
    isTeacher = models.BooleanField(default=False)
    isStudent = models.BooleanField(default=False)
    #Booked_Count = models.IntegerField(default=0)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    def __str__(self):
        return "{}".format(self.user.username)
    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        img = Image.open(self.image.path)
        if img.width>100 or img.height > 100:
            img.thumbnail((100,100))
            img.save(self.image.path)
def creat_profile(sender,**kwargs):
    if kwargs['created']:
        Profile.objects.create(user=kwargs['instance'])
post_save.connect(creat_profile,sender=User)

