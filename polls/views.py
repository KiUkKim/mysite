from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from .models import Question, Choice
from django.utils import timezone
from django.urls import reverse
from django.views import generic
from django.shortcuts import render, get_object_or_404

from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    template_name = 'polls/detail.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        question = get_object_or_404(Question, pk=question_id)
        try:
            # 데이터를 조회했을 때, 데이터가 존재하지 않는다면 예외 발생
            selected_choice = question.choice_set.get(pk=request.POST['choice'])
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
            return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def get_queryset(self):
    """
    Return the last five published questions (not including those set to be
    published in the future).
    """
    return Question.objects.filter(
        pub_date__lte=timezone.now()
    ).order_by('-pub_date')[:5]

# Create your views here.
# # 요청된 페이지의 HttpResponse 객체나 404같은 예외를 발생하게 함
# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     #templates = loader.get_template('polls/index.html')
#     context = {
#         'latest_question_list' : latest_question_list,
#     }
#     return render(request, 'polls/index.html', context)
#     #return HttpResponse(templates.render(context, request))
#     # 문자열로 생성
#     #output = ', '.join([q.question_text for q in latest_question_list])
#     #return HttpResponse(output)
#
# #→ request로 클라이언트로 부터 요청을 받고 HttpResponse로 Response를 해줍니다.
# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {'question': question})
#     # try:
#     #     question = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("Question does not exist")
#     # return render(request, 'polls/detail.html', {'question': question})
#     #return HttpResponse("You're looking at question %s." % question_id)
#
# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})
#
