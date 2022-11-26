from django.http import HttpResponse, HttpResponseRedirect

# 단축 기능
from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.urls import reverse
from django.views import generic

from .models import Choice, Question

# Create your views here.
def index(request):
  latest_question_list = Question.objects.order_by('-pub_date')[:5]
  # polls/index.html 템플릿 불러옴
  # template = loader.get_template('polls/index.html')
  # context = 템플릿에서 쓰이는 변수명과 python 객체를 연결하는 사전형 값
  context = {
    'latest_question_list': latest_question_list,
  }
  # HttpResponse와 loader 이용하지 않아도 됨 nodejs 기능과 같음
  # render 함수는 request 객체를 첫번째 인수로 받고 
  # 템플릿이름을 두번째 인수로 받음, context 세번째 인수로 받음
  # context로 표현된 템플릿이 HttpRespose 객체 반환
  return render(request, 'polls/index.html', context)

def detail(request, question_id):
  try:
    #question = Question.objects.get(pk=question_id)
    # get_object_or_404 함수는 객체가 존재하지 않았을때 404에러
    question = get_object_or_404(Question, pk=question_id)
  except Question.DoesNotExist:
    raise Http404("Question does not exist")
  return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  return render(request, 'polls/results.html', {'question': question})

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


