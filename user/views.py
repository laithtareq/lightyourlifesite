from django.shortcuts import render,redirect
from .forms import UserCreationForm,UserUpdateForm,ProfileUpdateForm,NewFree,NewHomework ,SetMark ,SolveHomwork
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import sqlite3
from Bloger import models
# Create your views here.
def register(request):
    if request.method=='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password1'])
            new_user.save()
            messages.success(request,'تم الاضافة بنجاح')
            return redirect('login')
    else:
        form = UserCreationForm()
    context = {
        'title':'مستخدم جديد',
        'form':form,
    }
    return render(request,'user/register.html',context)
@login_required(login_url='login')
def profile(request):
    if request.user.profile.isTeacher:
        Mats = models.Teacher.objects.filter(Teacher_Name=request.user)
        Sections = models.Section.objects.filter(Teacher_Name=request.user)
    elif request.user.profile.isStudent:
        Mats = models.fillForm.objects.filter(Student_User=request.user)
        Sections = db.execute(sql)
    else:
        Mats = ""
        Sections =False
    context = {
        'title': request.user,
        'user': request.user,
        'Mats':Mats,
        'Sections':Sections
    }
    return render(request, 'user/profile.html', context)
@login_required(login_url='login')
def profile_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST,instance=request.user)
        profile_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        if user_form.is_valid and profile_form.is_valid:
            user_form.save()
            profile_form.save()
            messages.success(
                request, 'Profile Updated')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'title':'تحديث الصفة الشخصية',
        'user_form':user_form,
        'profile_form':profile_form,
    }
    return render(request,'user/profile_update.html',context)
@login_required(login_url='login')
def add_free(request,teaching_id):
    Free_Key = models.Teacher.objects.get(pk=teaching_id)
    Material_Key = Free_Key.Material_Key
    freeDate = models.Teacher_Free.objects.filter(Free_Key=Free_Key)
    form = NewFree(request.POST)
    if request.method=='POST':
        form = NewFree(request.POST)
        if form.is_valid():
            Days = form.cleaned_data['Days']
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']
            models.Teacher_Free.objects.update_or_create(Free_Key=Free_Key,Material_Key=Material_Key,Days=Days,start_time=start_time,end_time=end_time)
            return redirect('add_free',teaching_id)
    else:
        form = NewFree()
    context = {
        'title':'اضافة موعد جديد',
        'form':form,
        'freeDate':freeDate  # booked times
    }
    return render(request,'user/add_free.html',context)
@login_required(login_url='login')
def delete_free(request,free_id):
    Teacher_Free_Key = models.Teacher_Free.objects.get(pk=free_id)
    free_id = Teacher_Free_Key.Free_Key.id
    Teacher_Free_Key.delete()
    context = {
        'title':'تم مسح الموعد'
    }
    return redirect('add_free',free_id)
@login_required(login_url='login')
def add_homework(request,section_id):
    Section_Key = models.Section.objects.get(pk=section_id)
    Homeworks = models.Homework.objects.filter(Section_Key=Section_Key)
    if request.method=='POST':
        form = NewHomework(request.POST)
        if form.is_valid():
            Quastion_title = form.cleaned_data['Quastion_title']
            Quastion_text = form.cleaned_data['Quastion_text']
            Sugested_answer = form.cleaned_data['Sugested_answer']
            Dead_line = form.cleaned_data['Dead_line']
            Max_mark = form.cleaned_data['Max_mark']
            models.Homework.objects.update_or_create(Section_Key=Section_Key,Quastion_title=Quastion_title,Quastion_text=Quastion_text,
            Sugested_answer=Sugested_answer,Dead_line=Dead_line,Max_mark=Max_mark)
            return redirect('add_homework',section_id)
    else:
        form = NewHomework()
    context = {
        'title':'اضافة سؤال جديد',
        'form':form,
        'Homeworks':Homeworks
    }
    return render(request,'user/add_homework.html',context)
@login_required(login_url='login')
def homework_detail(request,homework_id):
    Homework_Key = models.Homework.objects.get(pk=homework_id)
    Answers = models.Answer.objects.filter(Homework_Key=Homework_Key)
    context={
        'title':'تفاصيل السؤال',
        'Answers':Answers
    }
    return render(request,'user/homework_detail.html',context)
@login_required(login_url='login')
def answer_detail(request,answer_id):
    Answer_Key = models.Answer.objects.get(pk=answer_id)
    homework_id = Answer_Key.Homework_Key.id
    if request.method=='POST':
        form = SetMark(request.POST)
        if form.is_valid():
            mark = form.cleaned_data['Mark']
            Answer_Key.Mark = mark
            Answer_Key.save()
            return redirect('homework_detail',homework_id)
    else:
        form = SetMark()
    context = {
        'title':'اجابات الطالب',
        'Answer_Key':Answer_Key,
        'form':form
    }
    return render(request,'user/answer_detail.html',context)
@login_required(login_url='login')
def my_homeworks(request,section_id):
    Section_Key = models.Section.objects.get(pk=section_id)
    Homeworks = models.Homework.objects.filter(Section_Key=Section_Key)
    context = {
        'title':'واجبات الشعبة',
        'Homeworks':Homeworks
    }
    return render(request,'user/my_homeworks.html',context)
@login_required(login_url='login')
def solve_homework(request,homework_id):
    Homework_Key = models.Homework.objects.get(pk=homework_id)
    models.Answer.objects.update_or_create(Student_User=request.user,Homework_Key=Homework_Key)
    Answer_info = models.Answer.objects.get(Student_User=request.user,Homework_Key=Homework_Key)
    if request.method=='POST':
        form = SolveHomwork(request.POST)
        if form.is_valid():
            Answer = form.cleaned_data['Answer']
            Student_Name = request.user.username
            sugested_answers =  Homework_Key.Sugested_answer
            Max_Mark = Homework_Key.Max_mark
            Mark = 0
            A = ""
            for x in range(len(sugested_answers.split('/'))):
                A = sugested_answers.split('/')[x]
                if A == Answer:
                    Mark = Max_Mark
            Answer_info.Mark = Mark
            Answer_info.Answer = Answer
            Answer_info.Trials = Answer_info.Trials + 1
            Answer_info.save()
            messages.success(
                request, 'تم ارسال اجابتك ')
            return redirect('profile')
    else:
        form = SolveHomwork()
    context = {
        'title':'حل السؤال',
        'Answer_info':Answer_info,
    }
    return render(request,'user/solve_homework.html',context)