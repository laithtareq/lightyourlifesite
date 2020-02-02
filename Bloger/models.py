from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image
# Create your models here.
class Specialty(models.Model):
    name = models.CharField(max_length=40)
    def __str__(self):
        return "{}".format(self.name)
class Dep(models.Model):
    name = models.CharField(max_length=40)
    Specialty_Key = models.ForeignKey(Specialty,on_delete=models.CASCADE)
    def __str__(self):
        return "{}".format(self.name)
class Material(models.Model):
    name = models.CharField(max_length=40)
    Dep_Key = models.ForeignKey(Dep,on_delete=models.CASCADE)
    def __str__(self):
        return "{}".format(self.name)
class filled_Material(models.Model):
    Material_Key = models.ForeignKey(Material,on_delete=models.CASCADE)
    Students_Count = models.IntegerField(default=0)
    def __str__(self):
        return "{}".format(self.Material_Key.name)
class fillForm(models.Model):
    Student_User = models.ForeignKey(User,on_delete=models.CASCADE)
    Material_Key = models.ForeignKey(Material,on_delete=models.CASCADE)
    times = models.CharField(max_length=20)
    booked = models.BooleanField(default=False)
    post_date = models.DateTimeField(default=timezone.now)
    post_update = models.DateTimeField(auto_now=True)
    def __str__(self):
        return "{} - {}".format(self.Student_User.username,self.Material_Key.name)
class newAd(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    Material_Key = models.ForeignKey(Material,on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    file = models.FileField(default='logo.jpg', upload_to='Ad_Files')
    text = models.TextField(default='وصف الاعلان')
    expirDate = models.DateTimeField(default=timezone.now)
    post_date = models.DateTimeField(default=timezone.now)
    post_update = models.DateTimeField(auto_now=True)
    def __str__(self):
        return "{} - Posted at {}".format(self.title,self.post_date.strftime("%b %d %Y %H:%M:%S"))
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.file.path)
        if img.width > 300 or img.height > 300:
            img.thumbnail((300, 300))
            img.save(self.file.path)
class Teacher(models.Model):
    Teacher_Name = models.ForeignKey(User,on_delete=models.CASCADE)
    Material_Key = models.ForeignKey(Material,on_delete=models.CASCADE)
    post_date = models.DateTimeField(default=timezone.now)
    post_update = models.DateTimeField(auto_now=True)
    def __str__(self):
        return "{} - {}".format(self.Teacher_Name.username,self.Material_Key.name)
class Teacher_Free(models.Model):
    Free_Key = models.ForeignKey(Teacher,on_delete=models.CASCADE)
    Material_Key = models.ForeignKey(Material,on_delete=models.CASCADE)
    Days = models.CharField(max_length=20)
    start_time = models.TimeField()
    end_time = models.TimeField()
class Section(models.Model):
    Teacher_Name = models.ForeignKey(User,on_delete=models.CASCADE)
    Material_Key = models.ForeignKey(Material,on_delete=models.CASCADE)
    Days = models.CharField(max_length=20)
    start_time = models.TimeField()
    end_time = models.TimeField()
    start_date = models.DateField()
    end_date = models.DateField()
    Section_Class = models.IntegerField()
    Section_Num = models.IntegerField()
class Booking(models.Model):
    Student_User = models.ForeignKey(User,on_delete=models.CASCADE)
    Section_Key = models.ForeignKey(Section,on_delete=models.CASCADE)
    post_date = models.DateTimeField(default=timezone.now)
    Presence_times = models.IntegerField(default=0)
    post_update = models.DateTimeField(auto_now=True)
class Presence(models.Model):
    Booking_Key = models.ForeignKey(Booking,on_delete=models.CASCADE)
    Student_User = models.ForeignKey(User,on_delete=models.CASCADE)
    Section_Key = models.ForeignKey(Section,on_delete=models.CASCADE)
    Presence_Date = models.DateField()
class Homework(models.Model):
    Section_Key = models.ForeignKey(Section,on_delete=models.CASCADE)
    Quastion_text = models.CharField(max_length=20)
    Quastion_title = models.TextField()
    Max_mark = models.IntegerField()
    Dead_line = models.DateField()
    Sugested_answer = models.CharField(max_length=20,default="")
class Answer(models.Model):
    Homework_Key = models.ForeignKey(Homework,on_delete=models.CASCADE)
    Student_User = models.ForeignKey(User,on_delete=models.CASCADE)
    Answer = models.TextField()
    Mark = models.IntegerField(default=0)
    Trials = models.IntegerField(default=0)
    post_date = models.DateTimeField(default=timezone.now)
    post_update = models.DateTimeField(auto_now=True)




    
