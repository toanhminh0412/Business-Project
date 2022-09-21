from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# A technology tool (Git, Kubernestes, Docker, etc)
class Tool(models.Model):
    title = models.CharField(max_length=200)

    class Meta:
        ordering = ['title']
        db_table = 'tool'

    # String representation
    def __str__(self):
        return self.title

# A set of commands to do something
class CommandSet(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False)
    commands = models.CharField(max_length=1000, null=False, blank=False)
    description = models.CharField(max_length=500, null=True, blank=True)
    tool = models.ManyToManyField(Tool)
    upvote_num = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1)


    # For each word in the command set, there is a corresponding points of appearance for that word
    # Save the points for all words, which is later used in the search engine
    def add_word_index(self):
        # Construct string of all tools
        tool_str = ""
        for tool in self.tool.all():
            tool_str = tool_str + tool.title + " "

        # Current evaluation:
        # Tool: 5 points
        # Title: 3 points
        # Command: 2 points
        # Description: 1 point
        evaluate_string = tool_str * 5 + (self.title + " ") * 3 + (self.commands.replace("$", " ") + " ") * 2 + self.description if self.description else (self.title + " ") * 3 + (self.commands + " ") * 2
        evaluate_string = evaluate_string.lower()
        self.wordindex_set.all().delete()
        for word in evaluate_string.split():
            word_index = self.wordindex_set.filter(word=word)
            if len(word_index) == 0:
                WordIndex.objects.create(word=word, points=1, command_set=self)
            else:
                word_index = word_index[0]
                word_index.points = word_index.points + 1
                word_index.save()
    
    # Upvote a command set
    def upvote(self):
        self.upvote_num = self.upvote_num + 1
        self.save()

    # Downvote a command set
    def downvote(self):
        self.upvote_num = self.upvote_num - 1
        self.save()

    def save(self, *args, **kwargs):
        super(CommandSet, self).save(*args, **kwargs)
        self.add_word_index()

    # Display commands to user interface
    def display_commands(self):
        return self.commands.split("$ ")[1:]

    # Display tools that are used by the command set
    def display_tools(self):
        tools_str = ""
        for tool in self.tool.all():
            tools_str = tools_str + tool.title + ", "
        return tools_str[:-2]
        
    # String representation
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
        db_table = "command_set"

# Users can upvote a commamd set if they like it
class Upvote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    command_set = models.ForeignKey(CommandSet, on_delete=models.CASCADE)

    class Meta:
        ordering = ['user']
        db_table = "command_set_upvote"

    def save(self, *args, **kwargs):
        super(Upvote, self).save(*args, **kwargs)
        self.command_set.upvote()


# Users can downvote a commamd set if they like it
class Downvote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    command_set = models.ForeignKey(CommandSet, on_delete=models.CASCADE)

    class Meta:
        ordering = ['user']
        db_table = "command_set_downvote"

    def save(self, *args, **kwargs):
        super(Downvote, self).save(*args, **kwargs)
        self.command_set.downvote()

# Word index table for search engine optimization
class WordIndex(models.Model):
    word = models.CharField(max_length=20)
    points = models.IntegerField(default=0)
    command_set = models.ForeignKey(CommandSet, on_delete=models.CASCADE)

    class Meta:
        ordering = ['word']
        db_table = 'word_index'

    # String representation
    def __str__(self):
        return self.word

