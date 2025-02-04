from django.urls import path, include
from .views import *

urlpatterns = [
    path('question/', QuestionList.as_view(), name='question-list'),
    path('question/<int:pk>/', QuestionDetail.as_view(), name='question-detail'),
    path('users/',UserList.as_view(), name = 'user-list'),
    path('users/<int:pk>/',UserDetail.as_view(), name = 'signup'),
    path('register/',RegisterUser.as_view()),
    path('api-auth/', include('rest_framework.urls')),
    path('vote/',VoteList.as_view()),
    path('vote/<int:pk>/',VoteDetail.as_view()),
]