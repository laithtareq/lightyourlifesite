from django.urls import path
from . import views
from django.contrib.auth.views import LoginView,LogoutView
urlpatterns = [
    path('register/',views.register,name='register'),
    path('login/',LoginView.as_view(template_name='user/login.html'),name='login'),
    path('logout/',LogoutView.as_view(template_name='user/logout.html'),name='logout'),
    path('profile/',views.profile,name='profile'),
    path('profile_update/',views.profile_update,name='profile_update'),
    path('add_free/<int:teaching_id>/',views.add_free,name='add_free'),
    path('delete_free/<int:free_id>/', views.delete_free, name='delete_free'),
    path('add_homework/<int:section_id>/', views.add_homework, name='add_homework'),
    path('homework_detail/<int:homework_id>/', views.homework_detail, name='homework_detail'),
    path('answer_detail/<int:answer_id>/', views.answer_detail, name='answer_detail'),
    path('solve_homework/<int:homework_id>/', views.solve_homework, name='solve_homework'),
    path('my_homeworks/<int:section_id>/', views.my_homeworks, name='my_homeworks'),
]