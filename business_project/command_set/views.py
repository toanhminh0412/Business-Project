from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from .models import CommandSet, UserProfile, WordIndex, Tool, Upvote, Downvote
from django.contrib.auth.models import User

from forms import CommandSetForm
from mixins import LoginRequiredMixin

# Invisible view: Upvote a command set
def upvote_view(request, commandset_id):
    command_set = CommandSet.objects.filter(id=commandset_id)[0]
    user = User.objects.filter(id=request.session.get('user_id', None))[0]
    upvotes = Upvote.objects.filter(user=user, command_set=command_set)
    downvotes = Downvote.objects.filter(user=user, command_set=command_set)
    
    if len(upvotes) == 0:
        new_upvote = Upvote.objects.create(user=user, command_set=command_set)
        for downvote in downvotes:
            command_set.upvote_num = command_set.upvote_num + 1
            downvote.delete()
        command_set.save()
    
    return redirect(f"/{commandset_id}/")

# Invisible view: Downvote a command set
def downvote_view(request, commandset_id):
    command_set = CommandSet.objects.filter(id=commandset_id)[0]
    user = User.objects.filter(id=request.session.get('user_id', None))[0]
    upvotes = Upvote.objects.filter(user=user, command_set=command_set)
    downvotes = Downvote.objects.filter(user=user, command_set=command_set)
    
    if len(downvotes) == 0:
        new_downvote = Downvote.objects.create(user=user, command_set=command_set)
        for upvote in upvotes:
            command_set.upvote_num = command_set.upvote_num - 1
            upvote.delete()
        command_set.save()
    
    return redirect(f"/{commandset_id}/")

# Invisible view: Save a command set
def save_view(request, commandset_id):
    command_set = CommandSet.objects.filter(id=commandset_id)[0]
    user = User.objects.filter(id=request.session.get('user_id', None))[0]
    user_profile = UserProfile.objects.filter(user=user)[0]
    user_profile.saved_command_set.add(command_set)
    user_profile.save()
    return redirect(f"/{commandset_id}/")

# Invisible view: Unsave a command set
def unsave_view(request, commandset_id):
    command_set = CommandSet.objects.filter(id=commandset_id)[0]
    user = User.objects.filter(id=request.session.get('user_id', None))[0]
    user_profile = UserProfile.objects.filter(user=user)[0]
    user_profile.saved_command_set.remove(command_set)
    user_profile.save()
    return redirect(f"/{commandset_id}/")

# Search engine algorithm for command set
def search_algorithm(search_input):
    '''
    This function takes in a search input, excludes all command sets that do not have 
    any word in the search input. And sort the remaining command sets from most matched
    to least matched
    Args: str - search input
    Return: List of command set id (sorted from the most matched to the least matches)
    '''

    search_words = search_input.split()
    command_point = {}
    for sw in search_words:
        word_indexes = WordIndex.objects.filter(word=sw)
        for word_ind in word_indexes:
            command_id = word_ind.command_set.id
            point = word_ind.points
            if not command_point.get(command_id, None):
                command_point[command_id] = point
            else:
                command_point[command_id] = command_point[command_id] + point
    
    # Sort in descending order the points for each command set
    command_point = sorted(command_point, key=lambda x: command_point[x], reverse=True)
    return command_point

# Users can search for command sets on this page
class HomePageView(ListView):
    model = CommandSet
    template_name = "command_set/homepage.html"
    context_object_name = "command_sets"

    # Handle search request
    def post(self, request):
        search_input = request.POST['search-input']
        if search_input != "":
            command_ids = search_algorithm(search_input.lower())
            commands = []
            for id in command_ids:
                command = CommandSet.objects.filter(id=id)
                commands.append(command[0])
            context={'command_sets': commands}
            return render(request, self.template_name, context)
        else:
            context = {}
            context = self.get_context_data()
            context['message'] = 'Search bar cannot be empty'
            return render(request, self.template_name, context)

# Users can create new command sets on this page
class CommandSetAddView(LoginRequiredMixin, TemplateView):
    template_name = "command_set/add_page.html"

    def post(self,request):
        # Check if all values in the form are set properly
        commands_form = CommandSetForm(request.POST)
        # Valid form
        if commands_form.is_valid():
            # Get data from form and create a new CommandSet instance
            commands_data = commands_form.cleaned_data
            new_command_set = CommandSet.objects.create(title=commands_data['title'], commands=commands_data['commands'], created_by=User.objects.get(id=request.session.get('user_id')))
            for tool in commands_data['tool']:
                new_command_set.tool.add(tool)
            new_command_set.save()
            # Redirect to homepage
            return redirect("/")
        # Invalid form
        else:
            # Redirect to add page with an error message
            return render(request, self.template_name, {'all_tools': Tool.objects.all(), 'message': 'Please fill out the from properly'})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_tools'] = Tool.objects.all()
        return context

# Users view a single command set on this page
class CommandSetDetailView(DetailView):
    model = CommandSet
    pk_url_kwarg = 'commandset_id'
    template_name = 'command_set/detail_page.html'
    context_object_name = 'command_set'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Check and set context based on if user has upvoted or downvoted the command set
        command_set = self.get_object()

        # Add one to number of times users view the command set
        command_set.visited_num = command_set.visited_num + 1
        command_set.save()

        user = User.objects.filter(id=int(self.request.session.get('user_id', None)))[0]
        upvotes = Upvote.objects.filter(user=user, command_set=command_set)
        downvotes = Downvote.objects.filter(user=user, command_set=command_set)
        if len(upvotes) > 0:
            context['upvote'] = True
        if len(downvotes) > 0:
            context['downvote'] = True
        
        # Check and set context based on if user has saved the command set
        user_profile = UserProfile.objects.filter(user=user)[0]
        if command_set in user_profile.saved_command_set.all():
            context['user_saved'] = True

        return context

# Dashboard is where users can manage the application activity
# such as viewing command sets added, saved and searched by them
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get all command sets that were created by the current user
        user = User.objects.filter(id=int(self.request.session.get("user_id", None)))[0]
        created_commands = CommandSet.objects.filter(created_by=user) 
        # Sorted by last updated
        context['created_commands'] = created_commands
        # Sorted by popularity
        context['created_commands_sorted_by_popularity'] = sorted(created_commands, key=lambda x: x.visited_num, reverse=True)
        # Sorted by number of upvotes
        context['created_commands_sorted_by_upvote'] = sorted(created_commands, key=lambda x: x.upvote_num, reverse=True)

        # Get all tools that this user has created a command set for
        created_tools = []
        for command in created_commands:
            for tool in command.tool.all():
                if tool not in created_tools:
                    created_tools.append(tool)
        context['created_tools'] = created_tools

        # Get all command sets that were saved by the current user
        user_profile = UserProfile.objects.filter(user=user)[0]
        saved_commands = user_profile.saved_command_set.all()
        # Sorted by last updated
        context['saved_commands'] = saved_commands
        # Sorted by popularity
        context['saved_commands_sorted_by_popularity'] = sorted(saved_commands, key=lambda x: x.visited_num, reverse=True)
        # Sorted by number of upvotes
        context['saved_commands_sorted_by_upvote'] = sorted(saved_commands, key=lambda x: x.upvote_num, reverse=True)

        # Get all tools that this user has saved a command set for
        saved_tools = []
        for command in saved_commands:
            for tool in command.tool.all():
                if tool not in saved_tools:
                    saved_tools.append(tool)
        context['saved_tools'] = saved_tools

        # Get the upvotes that user made
        upvotes = Upvote.objects.filter(user=user)
        context['upvotes'] = upvotes

        # Get the downvotes that user made
        downvotes = Downvote.objects.filter(user=user)
        context['downvotes'] = downvotes

        # Get all tools available in the application
        context['all_tools'] = Tool.objects.all()

        return context