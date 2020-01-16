from django import forms
from Bloger import models
class fillForm(forms.Form):
    phone = forms.CharField(required=True)
    emailOrFace = forms.CharField(required=True)
    times = forms.CharField()
class bicDep(forms.ModelForm):
    class Meta:
        model = models.Material
        fields = ('Dep_Key',)
class AddThing(forms.Form):
    name = forms.CharField(required=False)
    nameDelete = forms.CharField(required=False)
class NewAd(forms.ModelForm):
    class Meta:
        model = models.newAd
        fields = ('title','file','text','expirDate',)
class AddSection(forms.Form):
    teacher_username = forms.CharField(max_length=20)
    Days = forms.CharField(max_length=20)
    start_time = forms.TimeField()
    end_time = forms.TimeField()
    start_date = forms.DateField()
    end_date = forms.DateField()
    Section_Class = forms.IntegerField()