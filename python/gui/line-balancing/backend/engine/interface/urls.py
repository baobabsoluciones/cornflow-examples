from django.urls import path

from interface.views import StationsView, TasksView, PrecedenceViews, SolveView, SolutionView

urlpatterns = [
    path('stations/', StationsView.as_view(), name='stations'),
    path('tasks/', TasksView.as_view(), name='tasks'),
    path('precedences/', PrecedenceViews.as_view(), name='precedences'),
    path('solution/', SolutionView.as_view(), name='solution'),
    path('solve/', SolveView.as_view(), name='solve')
]