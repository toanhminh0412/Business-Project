from django.shortcuts import render
from django.views.generic.list import ListView
from .models import CommandSet, WordIndex
from django.contrib.auth.models import User

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

# Get command sets that are added by the current users
def command_set_by_curuser(user_id):
    return user_id

# Create your views here.
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