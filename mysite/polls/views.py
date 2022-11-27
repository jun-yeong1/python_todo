from django.http import HttpResponseRedirect

# 단축 기능
from django.shortcuts import get_object_or_404, render

from django.urls import reverse
from django.views import generic

from .models import Choice, Question
from django.utils import timezone

# Create your views here.
class IndexView(generic.ListView):
  template_name: str = 'polls/index.html'
  context_object_name: str = 'latest_question_list'
  
  def get_queryset(self):
    return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
  # polls/index.html 템플릿 불러옴
  # context = 템플릿에서 쓰이는 변수명과 python 객체를 연결하는 사전형 값
  # render 함수는 request 객체를 첫번째 인수로 받고 
  # 템플릿이름을 두번째 인수로 받음, context 세번째 인수로 받음
  # context로 표현된 템플릿이 HttpRespose 객체 반환

class DetailView(generic.DetailView):
  model = Question
  template_name: str = 'polls/detail.html'
  def get_queryset(self):
    return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
  model = Question
  template_name: str = 'polls/results.html'

def vote(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  try:
    selected_choice = question.choice_set.get(pk=request.POST['choice'])  # type: ignore
  except (KeyError, Choice.DoesNotExist):
    # Redisplay the question voting form.
    return render(request, 'polls/detail.html', {
      'question': question,
      'error_message': "You didn't select a choice.",
    })
  else:
    selected_choice.votes += 1
    selected_choice.save()
    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    # 재전송할 url
    return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))


