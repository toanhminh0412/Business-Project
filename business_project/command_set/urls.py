from django.urls import path
from . import views

urlpatterns = [
    path("", view=views.HomePageView.as_view(), name="command_homepage"),
    path("dashboard/", view=views.DashboardView.as_view(), name="dashboard"),
    path("add_commands/", view=views.CommandSetAddView.as_view(), name="command_add_page"),
    path("<int:commandset_id>/", view=views.CommandSetDetailView.as_view(), name="command_detail_page"),
    path("upvote/<int:commandset_id>/", view=views.upvote_view, name='commandset_upvote'),
    path("downvote/<int:commandset_id>/", view=views.downvote_view, name='commandset_downvote'),    
    path("save/<int:commandset_id>/", view=views.save_view, name='commandset_save'),
    path("unsave/<int:commandset_id>/", view=views.unsave_view, name='commandset_unsave'),
]