import random
from datetime import datetime, timedelta
from typing import Any
from django.db.models.query import QuerySet

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

from . import constants

from .models import (
    Definition,
    Category
    )

from .forms import DefinitionForm

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
    template='blog/search.html'

    query=request.GET.get('q')

    result=Definition.objects.filter(Q(word__icontains=query) | Q(author__username__icontains=query) | Q(description__icontains=query))
    paginate_by = constants.DEFINITIONS_PER_PAGE
    context={
        'title': f'Search results for "{query}"',
        'query_string': query,
        'definitions': result
        }
    return render(request,template,context)

def getfile(request):
   return serve(request, 'File')


class DefinitionListView(ListView):
    model = Definition
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'definitions'
    #ordering = ['-date_posted']
    paginate_by = constants.DEFINITIONS_PER_PAGE

    def get_queryset(self) -> QuerySet[Any]:

        ordering = self.kwargs.get('ordering', 'most-recent')

        # Filter by date range based on ordering option
        now = datetime.now()

        ordering_map = {
            'most-recent': Definition.objects.order_by('-date_posted'),
            'popular-day': Definition.objects.filter(Q(date_posted__gte=(now - timedelta(days=1)))).order_by('likes'),
            'popular-week': Definition.objects.filter(Q(date_posted__gte=(now - timedelta(weeks=1)))).order_by('likes'),
            'popular-all-time': Definition.objects.order_by('likes'),
        }

        # Return definition objects in correct order or default to date posted order
        return ordering_map.get(ordering, Definition.objects.order_by('-date_posted'))
        #return super().get_queryset()

    # Override this method to add categories to context
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        # Order categories alphabetically
        context['categories'] = Category.objects.all().order_by('name')

        # This is sloppy. The whole view needs cleaning up.
        ordering = self.kwargs.get('ordering')
        ordering = (
            ordering
            if ordering in ['most-recent', 'popular-day', 'popular-week', 'popular-all-time']
            else 'most-recent'
            )
        
        context['ordering'] = ordering
        
        # Map ordering to list title
        list_title_map = {
            'most-recent' : 'Most recent',
            'popular-day': 'Hot today',
            'popular-week': 'Hot this week',
            'popular-all-time': 'All time most popular'
        }
        
        context['list_title'] = list_title_map[ordering]

        return context


class UserDefinitionListView(ListView):
    model = Definition
    template_name = 'blog/user_definitions.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'definitions'
    paginate_by = constants.DEFINITIONS_PER_PAGE

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Definition.objects.filter(author=user).order_by('-date_posted')


class CategoryDefinitionListView(ListView):
    model = Definition
    template_name = 'blog/category.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'definitions'
    paginate_by = constants.DEFINITIONS_PER_PAGE

    def get_queryset(self):
        category = get_object_or_404(Category, name=self.kwargs.get('category'))
        return Definition.objects.filter(categories=category).order_by('-date_posted')

    # Override this method to add categories to context
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        category = self.kwargs.get('category')

        context['title'] = f'{category} definitions'
        context['category'] = category
        # Need to pass categories back for 
        context['categories'] = Category.objects.all().order_by('name')

        return context

class DefinitionDetailView(DetailView):
    model = Definition
    template_name = 'blog/definition_detail.html'

    def get_context_data(self, **kwargs):
            
            definition = get_object_or_404(Definition, id=self.kwargs['pk'])
            # Call the base implementation to get the default context data
            context = super().get_context_data(**kwargs)
            # Add additional context data
            context['title'] = f"{definition} definition"
            context['total_likes'] = definition.total_likes() 

            return context

# NOTE: DefinitionCreateView and DefinitionUpdate view are very similar and can probably be
# be combined through the use of a conditional to check if the definition already exists
class DefinitionCreateView(LoginRequiredMixin, CreateView):
    model = Definition
    template_name = 'blog/definition_form.html'
    form_class = DefinitionForm

    def form_valid(self, form):

        categories = form.cleaned_data['categories']
        
        if len(categories) > 5:

            form.add_error('categories', "A definition can belong to at most five categories")
            return self.form_invalid(form)

        form.instance.author = self.request.user

        # Returns an instance of the Definition model, which can then be manipulated before saving
        # to the database
        new_definition: Definition = form.save(commit=False)

        # Can't save the many to many categories until the definition has been saved with an ID, so
        # save the definition object to generate an id value. Calling save method on model instance
        # only saves fields defined directly on model and not many-to-many relationships
        new_definition.save()

        # Now the definition exists with an ID, the many-to-many relationships (categories) can be
        # saved
        form.save_m2m()  # Save many-to-many relationships

        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        # Add additional context data
        context['title'] = 'Create new definition'

        return context

class DefinitionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Definition
    template_name = 'blog/definition_form.html'
    form_class = DefinitionForm

    def form_valid(self, form):

        categories = form.cleaned_data['categories']

        if len(categories) > 5:

            form.add_error('categories', "A definition can belong to at most five categories")
            return self.form_invalid(form)

        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        definition = self.get_object()
        if self.request.user == definition.author:
            return True
        return False
    
    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        # Add additional context data
        context['title'] = 'Update definition'

        return context



class DefinitionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Definition
    success_url = '/'
    template_name = 'blog/definition_confirm_delete.html'
    
    def test_func(self):
        definition = self.get_object()
        if self.request.user == definition.author:
            return True
        return False


def like_view(request, pk):

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