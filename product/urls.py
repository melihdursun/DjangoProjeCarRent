from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    path('addcomment/<int:id>', views.addcomment, name='addcomment'),
    path('addreservation/<int:id>', views.addreservation, name='addreservation')
    # ex: /polls/5/
    #path('<int:question_id>/', views.detail, name='detail'),

]