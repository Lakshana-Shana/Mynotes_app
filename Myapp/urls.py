from django.urls import path

from .views import (
    RegisterView,
    LoginView,
    NoteListCreateView,
    NoteDetailView
)

from rest_framework_simplejwt.views import (
    TokenRefreshView
)


urlpatterns = [

    path('register/',RegisterView.as_view()),
    path('login/',LoginView.as_view()),
    path('token/refresh/',TokenRefreshView.as_view()),
    path('notes/',NoteListCreateView.as_view()),
    path('notes/<int:pk>/',NoteDetailView.as_view()),
]