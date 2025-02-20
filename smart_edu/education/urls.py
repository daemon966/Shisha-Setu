# from django.urls import path
# from . import views



# urlpatterns = [
#     path('', views.landing_page, name='landing'),  # Default landing page
#     path('login/', views.user_login, name='login'),  # Login page
#     path('register/', views.register_page, name='register'),  # Registration page
#     path('home/', views.home, name='home'),  # Home page after login
#     path('logout/', views.user_logout, name='logout'),  # Logout
#     path('quiz/', views.quiz, name='quiz'),  # Quiz page
#     path('leaderboard/', views.leaderboard, name='leaderboard'),  # Leaderboard
#     path('results/', views.results, name='results'),  # Results page
    
#     path("chatbot/", views.chatbot, name="chatbot"),
#     path('resources/', views.input_topic, name='resources'),
#     path('quiz/', views.quiz, name='quiz'),
#     path('quiz_result/', views.quiz_result, name='quiz_result'),
#     path('leaderboard/', views.leaderboard, name='leaderboard'),
#     path('results/', views.results, name='results'),
#     path('take_quiz/', views.take_quiz, name='take_quiz'),
#     path('submit_quiz/', views.submit_quiz, name='submit_quiz'),
#     path('input_topic/', views.input_topic, name='input_topic'),
#     path('display_resources/', views.display_resources, name='display_resources'),
#     path('analytics/', views.analytics_dashboard, name='analytics_dashboard'),
# ]
    
from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing'),  # Default landing page
    path('login/', views.user_login, name='login'),  # Login page
    path('register/', views.register_page, name='register'),  # Registration page
    path('home/', views.home, name='home'),  # Home page after login
    path('logout/', views.user_logout, name='logout'),  # Logout
    path('quiz/', views.quiz, name='quiz'),  # Quiz page
    path('leaderboard/', views.leaderboard, name='leaderboard'),  # Leaderboard
    path('results/', views.results, name='results'),  # Results page
    
    path("chatbot/", views.chatbot, name="chatbot"),
    path('resources/', views.input_topic, name='resources'),  # Input resources
    path('quiz_result/', views.quiz_result, name='quiz_result'),  # Quiz result page
    path('take_quiz/', views.take_quiz, name='take_quiz'),  # Take quiz page
    path('submit_quiz/', views.submit_quiz, name='submit_quiz'),  # Submit quiz page
    path('display_resources/', views.display_resources, name='display_resources'),  # Display resources page
    path('analytics/', views.analytics_dashboard, name='analytics_dashboard'),  # Analytics dashboard
    path('transcript/<str:video_id>/', views.display_transcript, name='display_transcript'),
]

