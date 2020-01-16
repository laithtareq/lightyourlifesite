from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django.utils import timezone
class UserCreationForm(forms.ModelForm):
    username = forms.CharField(label='اسم المستخدم',max_length=20)
    first_name = forms.CharField(label='الاسم الاول',max_length=20)
    last_name = forms.CharField(label='الاسم الاخير', max_length=20)
    password1=forms.CharField(label='كلمة المرور',max_length=50,widget=forms.PasswordInput(),min_length=4)
    password2 = forms.CharField(label='تأكيد كلمة المرور', max_length=50, widget=forms.PasswordInput(),min_length=4)
    class Meta:
        model = User
        fields = ('username','first_name','last_name','password1','password2')
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1']!=cd['password2']:
            raise forms.ValidationError('كلمة السر غير مطابقة')
        return cd['password2']
    def clean_username(self):
        cd = self.cleaned_data
        if User.objects.filter(username=cd['username']).exists():
            raise forms.ValidationError('اسم المستخدم مكرر')
        return cd['username']
class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(label='الاسم الاول', max_length=50)
    last_name = forms.CharField(label='الاسم الاخير', max_length=50)
    class Meta:
        model = User
        fields = ('first_name','last_name')
class ProfileUpdateForm(forms.ModelForm):
    email = forms.CharField(label='الايميل الشخصي', max_length=50)
    phone = forms.CharField(label='رقم التلفون', max_length=50)
    class Meta:
        model = Profile
        fields = ('image','phone','email')
class NewFree(forms.Form):
    Days = forms.CharField(max_length=20)
    start_time = forms.TimeField()
    end_time = forms.TimeField()
class NewHomework(forms.Form):
    Quastion_title = forms.CharField(label='عنوان السؤال',max_length=20)
    Quastion_text = forms.CharField(label='نص السؤال',widget=forms.Textarea)
    Sugested_answer = forms.CharField(label='اجوبة مقترحة - لن يتم عرض الاجوبة المقترحة للطلاب بأي شكل من الاشكال و'
                                            ' سيقوم الموقع بالتصليح بشكل تلقائي '
                                            'مع امكانية تدخل المدرس في تغيير العلامة', max_length=20,required=False)
    Dead_line = forms.DateField(label='اخر موعد لاستقبال الاجوبة',widget=forms.SelectDateWidget)
    Max_mark = forms.IntegerField(label='علامة السؤال')
    def clean_Dead_line(self):
        cleaned_data = super().clean()
        Dead_line = cleaned_data.get("Dead_line")
        cd = self.cleaned_data
        if timezone.now().date()>=Dead_line:
            raise forms.ValidationError('يرجى اختيار موعد صحيح')
        return cd['Dead_line']
class SetMark(forms.Form):
    Mark = forms.IntegerField()
class SolveHomwork(forms.Form):
    Answer = forms.CharField(label='الجواب',widget=forms.Textarea)

