from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.start,name="start"),
    path('login/',views.user_login,name='login'),
    path('signup/',views.user_signup,name='signup'),
    path('tasks/',views.task_list,name="task_list"),
    path('tasks/update/<int:task_id>/',views.task_update,name='task_update'),
    path('tasks_add/', views.task_add, name='task_add'),
    path('user_logout/',views.user_logout,name='user_logout'),
    path('tasks/delete/<int:task_id>/',views.task_delete,name='task_delete'),  
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
