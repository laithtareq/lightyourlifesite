from django.urls import path
from . import views
from django.contrib.auth.views import LoginView,LogoutView
urlpatterns = [
    path('',views.home,name='home'),
    path('pickDep/<int:specialty_id>/',views.pickDep,name='pickDep'),
    path('pickMat/<int:dep_id>/',views.pickMat,name='pickMat'),
    path('fillForm/<int:mat_id>/',views.fillForm,name='fillForm'),
    path('AllMaterials/',views.AllMaterials,name='AllMaterials'),
    path('MatSt/<int:mat_id>/',views.MatSt,name='MatSt'),
    path('AddThing/<str:addTo>/<int:Father_id>/',views.AddThing,name='AddThing'),
    path('ConformDelete/<str:delete>/<int:Thing_id>/',views.ConformDelete,name='ConformDelete'),
    path('DeleteThing/<str:delete>/<int:Thing_id>/',views.DeleteThing,name='DeleteThing'),
    path('NewAd/<int:Mat_id>/', views.NewAd, name='NewAd'),
    path('selectTeacher/<int:mat_id>/',views.selectTeacher,name='selectTeacher'),
    path('AddSection/<int:mat_id>/',views.AddSection,name='AddSection'),
    path('EditSection/<int:section_id>/',views.EditSection,name='EditSection'),
    path('AllSections/', views.AllSections, name='AllSections'),
    path('AddSectionStudents/<int:section_id>/',views.AddSectionStudents,name='AddSectionStudents'),
    path('Presence/<int:section_id>/', views.Presence, name='Presence'),
    path('Presence_Record/<int:section_id>/', views.Presence_Record, name='Presence_Record'),
    path('Student_Presence/<str:Student_username>/<int:section_id>/', views.Student_Presence, name='Student_Presence'),
    path('Paied_Students/', views.Paied_Students, name='Paied_Students'),
]