import random

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Definition
import operator
from django.urls import reverse_lazy, reverse
from django.contrib.staticfiles.views import serve

from django.db.models import Q

# Don't think this gets used?
def home(request):
    context = {
        'definitions': Definition.objects.all()
    }
    return render(request, 'blog/home.html', context)

def search(request):
    # Change this to use the search page (with home potentially embedded inside)
    template='blog/home.html'

    query=request.GET.get('q')

    result=Definition.objects.filter(Q(word__icontains=query) | Q(author__username__icontains=query) | Q(description__icontains=query))
    paginate_by=10
    context={ 'definitions':result }
    return render(request,template,context)
   
def learn(request):
    # NOTE: This is obviously not scalable as it fetches all values
    # in the table each time a new set of phrases is picked. Look
    # into efficient ways to randomly select values from a db.
    # IDEA 1: https://stackoverflow.com/questions/1731346/how-to-get-two-random-records-with-django
    # IDEA 2: Fetch 100 rows in order etc. and return 10 at random
    num_phrases = 10
    phrases = Phrase.objects.all()
    #random_phrases = random.sample(list(phrases), num_phrases)
    random_phrase = str(random.choice(list(phrases)))
    print(random_phrase)

    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
    
    if is_ajax:
        # Convert queryset to list of dictionaries so can be serialised to JSON
        #data = {'phrases': [{'content': phrase.content} for phrase in random_phrases]}
        data = {'phrase': random_phrase}
        
        return JsonResponse(data)
    else:
        context = {
            #'phrases': random_phrases
            'phrase': random_phrase
        }
        return render(request, 'blog/learn.html', context)

def getfile(request):
   return serve(request, 'File')


class DefinitionListView(ListView):
    model = Definition
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'definitions'
    ordering = ['-date_posted']
    paginate_by = 10


class UserDefinitionListView(ListView):
    model = Definition
    template_name = 'blog/user_definitions.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'definitions'
    paginate_by = 2

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Definition.objects.filter(author=user).order_by('-date_posted')
   

class DefinitionDetailView(DetailView):
    model = Definition
    template_name = 'blog/definition_detail.html'

    def get_context_data(self, **kwargs):
            
            definition = get_object_or_404(Definition, id=self.kwargs['pk'])
            # Call the base implementation to get the default context data
            context = super().get_context_data(**kwargs)
            # Add additional context data
            context['total_likes'] = definition.total_likes() 

            return context

class DefinitionCreateView(LoginRequiredMixin, CreateView):
    model = Definition
    template_name = 'blog/definition_form.html'
    fields = ['word', 'description']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class DefinitionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Definition
    template_name = 'blog/definition_form.html'
    fields = ['word', 'description']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        definition = self.get_object()
        if self.request.user == definition.author:
            return True
        return False


class DefinitionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Definition
    success_url = '/'
    template_name = 'blog/definition_confirm_delete.html'
    
    def test_func(self):
        definition = self.get_object()
        if self.request.user == definition.author:
            return True
        return False


def LikeView(request, pk):

    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

    if is_ajax:

        definition = get_object_or_404(Definition, id=request.POST.get('definition_id'))
        user = request.user
    
        if definition.likes.filter(id=user.id).exists():

            # The user has already liked the definition, so remove the like
            definition.likes.remove(user)
        else:

            # The user has not liked the definition yet, so add the like
            definition.likes.add(user)

        return JsonResponse({'total_likes': definition.total_likes()})
    else:
        # Non-Ajax requests (Shouldn't be any for likes)
        pass

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})