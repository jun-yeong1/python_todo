# URLconf 
from django.urls import path

from . import views

#url 이름공간(namespace) 추가
app_name = 'polls'
urlpatterns = [
  # question_id -> pk
    # ex: /polls/
    path('', views.index, name='index'),
    # ex: /polls/5/
    path('<int:pk>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
]