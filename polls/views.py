
import datetime
from django.core.exceptions import AppRegistryNotReady
#from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect , HttpResponse , Http404  
from django.urls import reverse , reverse_lazy
from django.views import generic
from django.utils import timezone
from .models import Choice, Question
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import UserCreationForm

# def index(request):
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # template = loader.get_template('polls/index.html')
    # context = {
        # 'latest_question_list': latest_question_list,
    # }
    # return HttpResponse(template.render(context, request))

#def index(request):
#    latest_question_list = Question.objects.order_by('-pub_date')[:5]
#    context = {'latest_question_list': latest_question_list}
#    return render(request, 'polls/index.html', context)


class HomeView(generic.TemplateView):
    template_name = 'polls/home.html'

class ContactUsView(generic.TemplateView):
    template_name = 'polls/contact_us.html'


@method_decorator(login_required, name='get')
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        # """Return the last five published questions."""
        # return Question.objects.order_by('-pub_date')[:5]
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]

# def detail(request, question_id):
    # try:
        # question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
        # raise Http404("Question does not exist")
    # return render(request, 'polls/detail.html', {'question': question})

#def detail(request, question_id):
#    question = get_object_or_404(Question, pk=question_id)
#    return render(request, 'polls/detail.html', {'question': question})

@method_decorator(login_required, name='get')
class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

#def results(request, question_id):
#    response = "You're looking at the results of question %s."
#    return HttpResponse(response % question_id)

#def results(request, question_id):
#    question = get_object_or_404(Question, pk=question_id)
#    return render(request, 'polls/results.html', {'question': question})

@method_decorator(login_required, name='get')
class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        user = request.user
        exist = question.users.all()
        if user in exist:
            return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
        else:
            selected_choice.votes += 1
            selected_choice.save()
            question.users.add(user)
            question.save()

        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
