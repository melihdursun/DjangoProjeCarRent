from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    path('update/', views.user_update, name='user_update'),
    path('password/', views.change_password, name='change_password'),
    path('comments/', views.comments, name='comments'),
    path('deletecomment/<int:id>', views.deletecomment, name='deletecomment'),
    path('bookings/', views.bookings, name='bookings'),


    #path('addcomment/<int:id>', views.addcomment, name='addcomment')
    # ex: /polls/5/
    #path('<int:question_id>/', views.detail, name='detail'),

]