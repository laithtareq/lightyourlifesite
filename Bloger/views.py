from django.shortcuts import render,redirect
from Bloger import forms,models
from user.models import Profile
import sqlite3
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Count
import os
# Create your views here.

def home(request):
    Ads = models.newAd.objects.all()
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db = sqlite3.connect(os.path.join(BASE_DIR, 'db.sqlite3'))
    try:
        db.execute("create view fillform_view as select Bloger_fillform.*,\
        Bloger_material.id as Material_id,Bloger_material.name as Material_Name \
            ,Bloger_dep.id as Dep_id,Bloger_dep.name as Dep_Name ,\
                Bloger_specialty.id as Specialty_id,Bloger_specialty.name as Specialty_Name from Bloger_fillform \
        inner join Bloger_material on Bloger_material.id = Bloger_fillform.Material_Key_id \
            inner join Bloger_dep on Bloger_dep.id = Bloger_material.Dep_Key_id \
                inner join Bloger_specialty on Bloger_specialty.id = Bloger_dep.Specialty_Key_id")
    except:
        pass
    '''
    
    try:
        db.execute("create view Sections_View as select Bloger_section.id,Days,start_time,end_time,auth_user.username,Bloger_material.name,Section_Num,Section_Class,start_date,end_date,user_profile.phone,user_profile.email,auth_user.first_name,auth_user.last_name from Bloger_section \
                 inner join auth_user on auth_user.id =Bloger_section.Teacher_Name_id \
                 inner join Bloger_material on Bloger_material.id = Bloger_section.Material_Key_id \
                     inner join user_profile on user_id = Bloger_section.Teacher_Name_id")

        db.execute("create view fillform_View as select Bloger_fillform.id,times,Bloger_fillform.post_date,Material_Key_id,auth_user.username,user_profile.phone,user_profile.email,auth_user.first_name,auth_user.last_name from Bloger_fillform \
            inner join auth_user on auth_user.id = Bloger_fillform.Student_User_id  \
                inner join user_profile on user_id = Bloger_fillform.Student_User_id")
        db.execute("create view booking_view as select Bloger_booking.id,Bloger_booking.Section_Key_id,Bloger_section.Material_Key_id,Bloger_booking.Section_Key_id,Bloger_booking.post_date,auth_user.username,user_profile.phone,user_profile.email,auth_user.first_name,auth_user.last_name from Bloger_booking \
            inner join auth_user on auth_user.id = Bloger_booking.Student_User_id \
                inner join user_profile on user_id = Bloger_booking.Student_User_id \
                    inner join Bloger_section on Bloger_section.id = Bloger_booking.Section_Key_id")
        db.execute("create view presence_view as select Bloger_presence.id,Bloger_presence.Section_Key_id,Bloger_presence.Presence_Date,auth_user.username,user_profile.phone,user_profile.email,auth_user.first_name,auth_user.last_name from Bloger_presence \
            inner join auth_user on auth_user.id = Bloger_presence.Student_User_id \
                inner join user_profile on user_id = Bloger_presence.Student_User_id ")
        db.execute("create view paied_view as select auth_user.username,user_profile.phone,user_profile.email,count(Section_Key_id),auth_user.first_name,auth_user.last_name from user_profile \
            inner join auth_user on user_id = auth_user.id \
                left join Bloger_booking on Bloger_booking.Student_User_id = user_id \
                    group by username having user_profile.isStudent = 1")
    except:
        pass
    
    
    #data = db.execute("select Bloger_dep.name,Bloger_specialty.name from Bloger_dep inner join Bloger_specialty on Bloger_specialty.id = Bloger_dep.Specialty_Key_id")
    '''
    Specialty = models.Specialty.objects.all()
    context = {
        'title': 'الصفحة الرئيسية',
        'Specialty':Specialty,
        #'data':data,
        'Ads':Ads,
    }
    return render(request,'Bloger/home.html',context)
def pickDep(request,specialty_id):
    Specialty_Key = models.Specialty.objects.get(pk=specialty_id)
    Deps = models.Dep.objects.filter(Specialty_Key=Specialty_Key)
    context = {
        'title': Specialty_Key.name,
        'specialty':Specialty_Key,
        'Deps':Deps
    }
    return render(request,'Bloger/pickDep.html',context)
def pickMat(request,dep_id):
    Dep_Key = models.Dep.objects.get(pk=dep_id)
    Materials = models.Material.objects.filter(Dep_Key=Dep_Key)
    context = {
        'title': Dep_Key.name,
        'dep':Dep_Key,
        'Materials':Materials
    }
    return render(request,'Bloger/pickMat.html',context)
def fillForm(request,mat_id):
    Phone = ""
    form = forms.fillForm()
    Material_Key = models.Material.objects.get(pk=mat_id)
    sections = models.Section.objects.filter(Material_Key=Material_Key)
    if request.method=='POST':
        form = forms.fillForm(data=request.POST)
        if form.is_valid():
            name = request.user.username
            phone = form.cleaned_data['phone']
            emailOrFace = form.cleaned_data['emailOrFace']
            request.user.profile.phone = phone
            request.user.profile.email = emailOrFace
            request.user.profile.save()
            times = form.cleaned_data['times']
            models.fillForm.objects.update_or_create(Student_User=request.user,
            Material_Key=Material_Key ,times=times)
            messages.success(request, 'تم الاضافة بنجاح')
            return redirect('home')
        else:
            form = forms.fillForm()
    context = {
        'title':  'نموذج التسجيل الخاص بمادة {}'.format(Material_Key.name),
        'form':form,
        'mat':Material_Key,
        'sections':sections,
        'Phone':Phone
    }
    return render(request,'Bloger/fillForm.html',context)

@login_required(login_url='login')
def AllMaterials(request):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db = sqlite3.connect(os.path.join(BASE_DIR, 'db.sqlite3'))
    Materials = models.fillForm.objects.all().values('Material_Key').annotate(total=Count('Student_User')).order_by('total')
    Materials = db.execute("select count(Student_User_id),* from fillform_view group by Material_Key_id ")
    form = forms.bicDep
    Dep=""
    if request.method=='POST':
        form = forms.bicDep(request.POST)
        if form.is_valid():
            Dep = form.cleaned_data['Dep_Key']
            #Materials = models.fillForm.objects.filter(Material_Key__in=models.Material.objects.filter(Dep_Key=Dep)).values('Material_Key').annotate(total=Count('Student_User')).order_by('total')
            Materials = db.execute("select *,count(Student_User_id) from fillform_view group by Material_Key_id ")
    else:
        form = forms.bicDep()
    
    context = {
        'title':'نتائج تعبئة النماذج',
        'Materials':Materials,
        'form':form,
        'Dep':Dep
    }
    return render(request,'Bloger/AllMaterials.html',context)
def MatSt(request,mat_id):
    mat = models.Material.objects.get(pk=mat_id)
    Students = models.fillForm.objects.filter(Material_Key=mat)
    context = {
        'title':'الطلاب المسجلين في مادة {}'.format(mat),
        'Students':Students,
        'mat':mat
    }
    return render(request,'Bloger/MatSt.html',context)
def AddThing(request,addTo,Father_id):
    
    wanted =""
    if addTo=='Specialty':
        wanted = 'اسم التخصص المراد اضافته'
    elif addTo=='Dep':
        wanted = 'اسم القسم المراد اضافته'
    elif addTo=='Mat':
        wanted = 'اسم المادة المراد اضافتها'
    if request.method=='POST':
        form = forms.AddThing(data=request.POST)
        if form.is_valid():
            Thing = form.cleaned_data['name']
            if addTo == 'Specialty':
                models.Specialty.objects.update_or_create(name=Thing)
                messages.success(request, 'تم الاضافة بنجاح')
                return redirect('home')
            elif addTo=='Dep':
                Specialty_Key = models.Specialty.objects.get(pk=Father_id)
                models.Dep.objects.update_or_create(name=Thing,Specialty_Key=Specialty_Key)
                messages.success(request, 'تم الاضافة بنجاح')
                return redirect('pickDep',Father_id)
            elif addTo=='Mat':
                Dep_Key = models.Dep.objects.get(pk=Father_id)
                models.Material.objects.update_or_create(name=Thing,Dep_Key=Dep_Key)
                messages.success(request, 'تم الاضافة بنجاح')
                return redirect('pickMat', Father_id)
        else:
            form = forms.AddThing()

    context = {
        'title':wanted,
        'wanted':wanted
    }
    return render(request,'Bloger/AddThing.html',context)
@login_required(login_url='login')
def ConformDelete(request,delete,Thing_id):
    
    wanted =""
    if delete=='Specialty':
        Thing = models.Specialty.objects.get(pk=Thing_id)
        wanted = 'هل انت متأكد من حذف التخصص {}'.format(Thing.name)
        Dep_Will_delete = models.Dep.objects.filter(Specialty_Key=Thing)
        Mat_Will_delete = models.Material.objects.filter(Dep_Key__in=Dep_Will_delete)
        St_Will_delete = models.fillForm.objects.filter(Material_Key__in=Mat_Will_delete)
    elif delete=='Dep':
        Thing = models.Dep.objects.get(pk=Thing_id)
        wanted = 'هل انت متأكد من حذف القسم {}'.format(Thing.name)
        Dep_Will_delete = False
        Mat_Will_delete = models.Material.objects.filter(Dep_Key=Thing)
        St_Will_delete = models.fillForm.objects.filter(Material_Key__in=Mat_Will_delete)
    elif delete=='Mat':
        Thing = models.Material.objects.get(pk=Thing_id)
        wanted = 'هل انت متأكد من حذف المادة {}'.format(Thing.name)
        Dep_Will_delete = False
        Mat_Will_delete = False
        St_Will_delete = models.fillForm.objects.filter(Material_Key=Thing)
    '''
    elif delete=='teacherMat':
        wanted = 'هل انت متأكد من حذف المادة {}'.format(Thing.name)
        elif delete == 'teacherMat':
        sqlDelete = "delete from Material where Mat_Name = '{}' ".format(Thing)
        sqlDeleteSt = "select * from Students where Mat_Name = '{}'".format(Thing)
        Dep_Will_delete = False
        Mat_Will_delete = False
        St_Will_delete = False
    '''   
    context = {
        'title':'تأكيد عملية المسح',
        'wanted':wanted,
        'Dep_Will_delete':Dep_Will_delete,
        'Mat_Will_delete':Mat_Will_delete,
        'St_Will_delete':St_Will_delete,
        'delete':delete,
        'Thing_id':Thing_id
    }
    return render(request,'Bloger/ConformDelete.html',context)
@login_required(login_url='login')
def DeleteThing(request,delete,Thing_id):
    if delete == 'Specialty':
        Thing = models.Specialty.objects.get(pk=Thing_id)
        Thing.delete()
    elif delete == 'Dep':
        Thing = models.Dep.objects.get(pk=Thing_id)
        Thing.delete()
    elif delete == 'Mat':
        Thing = models.Material.objects.get(pk=Thing_id)
        Thing.delete()
    '''    
    elif delete == 'teacherMat':
        
        return redirect('profile')
    '''
    messages.success(request, 'تم مسح {}'.format(Thing.name))
    return redirect('home')
    context = {
        'title':'تم مسح {}'.format(Thing.name),
        'delete':delete,
        'Thing_id':Thing_id
    }
    return render(request,'Bloger/DeleteThing.html',context)
def NewAd(request,Mat_id):
    add = ""
    form = forms.NewAd
    if request.method=='POST':
        form = forms.NewAd(request.POST,request.FILES)
        if form.is_valid():
            Material_Key = models.Material.objects.get(pk=Mat_id)
            new_Ad = form.save(commit=False)
            new_Ad.author = request.user
            new_Ad.Material_Key = Material_Key
            new_Ad.save()
            redirect('home')
    else:
        form = forms.NewAd()
    context = {'title':'اضافة اعلان جديد',
               'form':form,
               }
    return render(request,'Bloger/NewAd.html',context)
@login_required(login_url='login')
def selectTeacher(request,mat_id):
    Material_Key = models.Material.objects.get(pk=mat_id)
    models.Teacher.objects.update_or_create(Teacher_Name=request.user,Material_Key=Material_Key)
    return render(request,'Bloger/selectTeacher.html',{'title':'selectTeacher'})
@login_required(login_url='login')
def AddSection(request,mat_id):
    
    form = forms.AddSection(data=request.POST)
    Material_Key = models.Material.objects.get(pk=mat_id)
    Teachers = ""
    Section_Num = 0
    Data = models.Section.objects.filter(Material_Key=Material_Key)
    x=0
    for data in Data:
        Section_Num = max(Data[x].Section_Num,Section_Num)
        x=x+1
    Section_Num = Section_Num +1
    if request.method=='POST':
        form = forms.AddSection(data=request.POST)
        if form.is_valid():
            
            Material_Key = models.Material.objects.get(pk=mat_id)
            teacher_username = form.cleaned_data['teacher_username']
            Teacher_Name = User.objects.get(username=teacher_username)
            Days = form.cleaned_data['Days']
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            Section_Class = form.cleaned_data['Section_Class']
            models.Section.objects.all()
            models.Section.objects.update_or_create(Teacher_Name=Teacher_Name,Material_Key=Material_Key,Days=Days,
            start_time=start_time,end_time=end_time,
            start_date=start_date,end_date=end_date,
            Section_Class=Section_Class,Section_Num=Section_Num)
            return redirect('fillForm',mat_id)
        
    else:
        Teachers = models.Teacher_Free.objects.filter(Material_Key=Material_Key)
        form = forms.AddSection()
    context = {
        'title':'اضافة شعبة جديدة',
        'form':form,
        'maxValue':Section_Num,
        'Teachers':Teachers}
    return render(request,'Bloger/AddSection.html',context)
@login_required(login_url='login')
def EditSection(request,section_id):
    
    form = forms.AddSection(data=request.POST)
    Section = models.Section.objects.get(pk=section_id)
    Material_Key = Section.Material_Key
    Teachers = ""
    Section_Num = Section.Section_Num
    if request.method=='POST':
        form = forms.AddSection(data=request.POST)
        if form.is_valid():
            
            teacher_username = form.cleaned_data['teacher_username']
            Teacher_Name = User.objects.get(username=teacher_username)
            Days = form.cleaned_data['Days']
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            Section_Class = form.cleaned_data['Section_Class']
            models.Section.objects.filter(pk=section_id).update(Teacher_Name=Teacher_Name,
            Days=Days,start_time=start_time,end_time=end_time,
            start_date=start_date,end_date=end_date,
            Section_Class=Section_Class)
            return redirect('fillForm',Section.Material_Key.id)
        
    else:
        Teachers = models.Teacher_Free.objects.filter(Material_Key=Material_Key)
        form = forms.AddSection()
    context = {
        'title':'تعديل الشعبة',
        'form':form,
        'maxValue':Section_Num,
        'Section':Section,
        'Teachers':Teachers}
    return render(request,'Bloger/EditSection.html',context)
def AllSections(request):
    sections = models.Section.objects.all()
    context = {
        'title':'كل الشعب',
        'sections':sections
    }
    return render(request,'Bloger/AllSections.html',context)
def AddSectionStudents(request,section_id):
    Students = ""
    SectionStudents = ""
    Section_Key = models.Section.objects.get(pk=section_id)
    Material_id = Section_Key.Material_Key.id
    form = forms.AddThing()
    if request.method=='POST':
        form = forms.AddThing(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            nameDelete = form.cleaned_data['nameDelete']
            if name != "":
                    Student_User = User.objects.get(username=name)
                    models.Booking.objects.update_or_create(Student_User=Student_User,Section_Key=Section_Key)
                    profile = Profile.objects.get(user=User.objects.get(username=name))
                    Booked_Count = models.Booking.objects.filter(Student_User=Student_User).count()
                    profile.isStudent = True
                    profile.Booked_Count=Booked_Count
                    profile.save()
                    models.fillForm.objects.filter(Student_User=Student_User,Material_Key=Section_Key.Material_Key).update(booked=True)
            if nameDelete != "":
                    Student_Delete = User.objects.get(username=nameDelete)
                    models.Booking.objects.filter(Student_User=Student_Delete,Section_Key=Section_Key).delete()
                    models.fillForm.objects.filter(Student_User=Student_Delete,Material_Key=Section_Key.Material_Key).update(booked=False)
                    Booked_Count = models.Booking.objects.filter(Student_User=Student_Delete).count()
                    profile = Profile.objects.get(user=User.objects.get(username=nameDelete))
                    profile.Booked_Count=Booked_Count
                    profile.save()
            return redirect('AddSectionStudents',section_id)
    else:
        Students = models.fillForm.objects.filter(Material_Key=Section_Key.Material_Key,booked=False) # from Students
        SectionStudents = models.Booking.objects.filter(Section_Key=Section_Key) # form Booking
    context = {
        'title':'اضافة طلاب الى الشعبة',
        'Students':Students,
        'SectionStudents':SectionStudents,
        'form':form,
        'Section_Key':Section_Key,
    }
    return render(request,'Bloger/AddSectionStudents.html',context)
def Presence(request,section_id):
    
    Students = ""
    SectionStudents = ""
    Section_Key = models.Section.objects.get(pk=section_id)
    Presence_Date = timezone.now().date()
    if request.method == 'POST':
        form = forms.AddThing(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            nameDelete = form.cleaned_data['nameDelete']
            if name != "":
                Student_User = User.objects.get(username=name)
                Booking_Key = models.Booking.objects.get(Student_User=Student_User,Section_Key=Section_Key)
                models.Presence.objects.update_or_create(Booking_Key=Booking_Key,Student_User=Student_User,Section_Key=Section_Key,Presence_Date=Presence_Date)
                Presence_times = models.Booking.objects.filter(Student_User=Student_User,Section_Key=Section_Key).count()
                models.Booking.objects.filter(Student_User=Student_User,Section_Key=Section_Key).update(Presence_times=Presence_times)
                
            if nameDelete != "":
                Student_User = User.objects.get(username=nameDelete)
                Booking_Key = models.Booking.objects.get(Student_User=Student_User,Section_Key=Section_Key)
                models.Presence.objects.get(Student_User=Student_User,Section_Key=Section_Key,Presence_Date=Presence_Date).delete()
                Presence_times = models.Booking.objects.filter(Student_User=Student_User,Section_Key=Section_Key).count()
                models.Booking.objects.filter(Student_User=Student_User,Section_Key=Section_Key).update(Presence_times=Presence_times)
        return redirect('Presence', section_id)
            
    else:
        Students = models.Booking.objects.filter(Section_Key=Section_Key)
        SectionStudents = models.Presence.objects.filter(Section_Key=Section_Key,Presence_Date=Presence_Date)
    context = {
        'title':'الحضور و الغياب',
        'Students':Students, # not Presence
        'SectionStudents':SectionStudents, # Presence
        'time':timezone.now().date(),
        'Section_Key':Section_Key
    }
    return render(request,'Bloger/Presence.html',context)
def Presence_Record(request,section_id):
    
    Section_Key = models.Section.objects.get(pk=section_id)
    Students = models.Presence.objects.filter(Section_Key=Section_Key)
    context = {
        'title':'سجل الحضور',
        'Students':Students,
        #'Mat_sec':Mat_sec
    }
    return render(request,'Bloger/Presence_Record.html',context)
def Student_Presence(request,Student_username,section_id):
    
    Student = User.objects.get(username=Student_username)
    Section_Key = models.Section.objects.get(pk=section_id)
    Students = models.Presence.objects.filter(Student_User=Student,Section_Key=Section_Key)
    Student_Name = Student.username
    context = {
        'title':'سجل الحضور للطالب {}'.format(Student_Name),
        'Student_Name':Student_Name,
        'Students':Students,
        'Student':Student
    }
    return render(request,'Bloger/Student_Presence.html',context)
def Paied_Students(request):
    
    sql = "select * from paied_view "
    Students = Profile.objects.filter(isStudent=True)
    context={
        'title':'الطلاب المحاسبين',
        'Students':Students
    }
    return render(request,'Bloger/Paied_Students.html',context)