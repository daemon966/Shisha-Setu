from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.http import JsonResponse
from .utils import fetch_youtube_videos, extract_keywords
from .models import QuizQuestion, QuizResult
from django.contrib.auth.decorators import login_required
from collections import Counter
import re
import requests
# education/views.py
from .forms import CustomUserCreationForm



from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render
from .models import QuizQuestion  # Assuming this is where your quiz questions are stored
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests


import json
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq
from dotenv import load_dotenv

# Load environment variables (GROQ API key)
load_dotenv()
groq_api_key = "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"

# Chatbot View
@csrf_exempt
def chatbot(request):
    """
    Handles user interaction with the Groq chatbot.
    """
    if request.method == "POST":
        try:
            # Get user input from the request
            data = json.loads(request.body)
            user_message = data.get("message", "")
            conversational_memory_length = data.get("memory_length", 5)

            if not user_message:
                return JsonResponse({"response": "Please enter a message."}, status=400)

            # Initialize memory
            memory = ConversationBufferWindowMemory(k=conversational_memory_length)

            # Initialize Groq Langchain chat object and conversation
            groq_chat = ChatGroq(groq_api_key=groq_api_key, model_name="mixtral-8x7b-32768")
            conversation = ConversationChain(llm=groq_chat, memory=memory)

            # Get response from the chatbot
            response = conversation(user_message)
            bot_message = response['response']

            # Save conversation history in session state
            if 'chat_history' not in request.session:
                request.session['chat_history'] = []
            request.session['chat_history'].append({'human': user_message, 'AI': bot_message})

            return JsonResponse({"response": bot_message})

        except Exception as e:
            print(f"Error occurred: {e}")
            return JsonResponse({"response": "Sorry, there was an error processing your request."}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=405)







   


# Landing Page view
def landing_page(request):
    """
    Landing page view which will be displayed first.
    """
    return render(request, 'education/landing.html')

# Login page view
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate the user
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to the home page or dashboard
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'education/login.html')

# Register page view
from django.shortcuts import render, redirect
from django.contrib import messages


from .forms import CustomUserCreationForm


def register_page(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login after successful registration
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserCreationForm()

    return render(request, 'education/register.html', {'form': form})


# Home page view after login
@login_required
def home(request):
    """
    Home page view which is visible after the user logs in.
    """
    if request.method == "POST":
        text = request.POST.get('content', '')
        keywords = extract_keywords(text)
        videos = fetch_youtube_videos(' '.join(keywords), api_key='AIzaSyBJLB6CtjTZX46dOjRgDcNWmcKaPTPa-8A')
        return render(request, 'education/home.html', {'videos': videos})
    return render(request, 'education/home.html')

# Logout view
def user_logout(request):
    """
    View for logging out the user.
    """
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('landing')  # Redirect to landing page after logout



def extract_keywords(text):
    """
    Extract keywords from the given text using regex and Counter.
    """
    # Convert text to lowercase and remove punctuation
    text = text.lower()
    words = re.findall(r'\b\w+\b', text)  # Extract words using regex
    
    # Define a basic stopwords list (can be expanded as needed)
    stopwords = {
        "the", "is", "in", "and", "to", "of", "a", "an", "on", "for", "with", 
        "as", "by", "at", "this", "that", "from", "or", "it", "was", "be", "are"
    }
    filtered_words = [word for word in words if word not in stopwords]
    
    # Count word frequencies
    word_frequencies = Counter(filtered_words)
    
    # Get the top 5 keywords
    keywords = [word for word, _ in word_frequencies.most_common(5)]
    return keywords


def fetch_youtube_videos(query, api_key):
    """
    Fetch YouTube videos based on a query and filter videos longer than 5 minutes.
    """
    youtube_search_url = "https://www.googleapis.com/youtube/v3/search"
    youtube_video_url = "https://www.googleapis.com/youtube/v3/videos"
    search_params = {
        'part': 'snippet',
        'q': query,
        'type': 'video',
        'maxResults': 10,
        'key': api_key,
    }
    try:
        # Fetch search results
        search_response = requests.get(youtube_search_url, params=search_params)
        search_response.raise_for_status()
        search_results = search_response.json().get('items', [])
        
        # Extract video IDs
        video_ids = [item['id']['videoId'] for item in search_results]
        
        # Fetch video details
        video_params = {
            'part': 'snippet,contentDetails',
            'id': ','.join(video_ids),
            'key': api_key,
        }
        video_response = requests.get(youtube_video_url, params=video_params)
        video_response.raise_for_status()
        video_details = video_response.json().get('items', [])
        
        # Filter videos longer than 5 minutes
        videos = []
        for video in video_details:
            duration = video['contentDetails']['duration']
            match = re.match(r'PT(\d+H)?(\d+M)?(\d+S)?', duration)
            hours = int(match.group(1)[:-1]) if match.group(1) else 0
            minutes = int(match.group(2)[:-1]) if match.group(2) else 0
            seconds = int(match.group(3)[:-1]) if match.group(3) else 0
            total_minutes = hours * 60 + minutes + seconds / 60
            
            if total_minutes >= 7:
                videos.append({
                    'video_id': video['id'],
                    'title': video['snippet']['title'],
                    'description': video['snippet']['description'],  # Added description
                    'thumbnail': video['snippet']['thumbnails']['high']['url'],
                    'duration': f"{hours}h {minutes}m {seconds}s" if hours else f"{minutes}m {seconds}s",
                })
        return videos
    except requests.exceptions.RequestException as e:
        print(f"Error fetching YouTube videos: {e}")
        return []


@login_required
def home(request):
    """
    Home view to handle the main page functionality.
    """
    if request.method == "POST":
        text = request.POST.get('content', '')
        keywords = extract_keywords(text)
        videos = fetch_youtube_videos(' '.join(keywords), api_key='AIzaSyBJLB6CtjTZX46dOjRgDcNWmcKaPTPa-8A')
        return render(request, 'education/home.html', {'videos': videos})
    return render(request, 'education/home.html')


from django.shortcuts import render

def register(request):
    return render(request, 'register.html')

def login_view(request):
    return render(request, 'login.html')

def signin(request):
    return render(request, 'login.html')

def get_started(request):
    return render(request, 'register.html')



import random
import spacy
import wikipediaapi
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from .models import QuizScore

# Load spaCy model for NLP
nlp = spacy.load("en_core_web_sm")

# Global dictionary to store quiz data
quiz_data = {}

def input_topic(request):
    if request.method == "POST":
        topic = request.POST.get("topic", "").strip()
        if not topic:
            return render(request, 'education/input_topic.html', {"error": "Please enter a valid topic."})

        # Update the user agent to be more descriptive
        user_agent = "SmartEducationSystem/1.0 (Contact: your_email@example.com)"
        wiki_wiki = wikipediaapi.Wikipedia(language='en', user_agent=user_agent)

        page = wiki_wiki.page(topic)

        if not page.exists():
            return render(request, 'education/input_topic.html', {
                "error": f"Sorry, no information found for '{topic}'. Please try a different topic."
            })

        # Store topic and content in session
        request.session['topic'] = topic
        request.session['content'] = page.text[:5000]  # Limit to the first 5000 characters

        return render(request, 'education/display_resources.html', {
            "topic": topic.title(),
            "summary": page.summary,
            "details": page.text[:5000],
            "url": page.fullurl,
        })

    return render(request, 'education/input_topic.html')


def generate_quiz(content):
    """
    Generates a quiz from the provided content using NLP.
    """
    doc = nlp(content)
    sentences = [sent.text for sent in doc.sents]
    quiz = []

    for sentence in sentences[:10]:  # Limit to the first 10 sentences
        # Extract nouns or proper nouns
        words = [token.text for token in nlp(sentence) if token.pos_ in ["NOUN", "PROPN"]]
        if not words:
            continue

        # Generate a question
        correct_answer = random.choice(words)
        distractors = random.sample(
            [word.text for word in doc if word.pos_ == "NOUN" and word.text != correct_answer],
            k=min(3, len(words) - 1)  # Ensure there are enough distractors
        )

        question = sentence.replace(correct_answer, "_____")
        options = [correct_answer] + distractors
        random.shuffle(options)

        quiz.append({
            "question": question,
            "options": options,
            "answer": correct_answer,
        })

    return quiz

def take_quiz(request):
    if request.method == "POST":
        answers = request.POST
        quiz = request.session.get("quiz")
        score = 0

        # List to hold selected answers for each question
        selected_answers = []

        for index, question in enumerate(quiz):
            selected_answer = answers.get(f"q{index}")
            selected_answers.append(selected_answer)

            if selected_answer == question["answer"]:
                score += 1

        # Update leaderboard (or handle as needed)
        leaderboard = request.session.get("leaderboard", [])
        leaderboard.append(score)
        request.session["leaderboard"] = leaderboard

        # Zip the quiz questions with selected answers
        quiz_with_answers = zip(quiz, selected_answers)

        # Pass the zipped quiz data to the result template
        return render(request, "education/quiz_result.html", {
            "score": score,
            "quiz_with_answers": quiz_with_answers,  # Pass zipped data
        })

    # Retrieve content from session
    content = request.session.get("content")
    if not content:
        return redirect("input_topic")  # Redirect to input page if content is missing

    quiz = generate_quiz(content)
    request.session["quiz"] = quiz

    return render(request, "education/quiz.html", {"quiz": quiz})




def submit_quiz(request):
    """
    Handles quiz submission and leaderboard update.
    """
    if request.method == "POST":
        topic = request.session.get('topic', "Unknown Topic")
        quiz = request.session.get('quiz', [])
        user = request.POST.get("user", "Anonymous")

        score = 0
        for i, q in enumerate(quiz):
            user_answer = request.POST.get(f"answer_{i}", "")
            if user_answer == q['answer']:
                score += 1

        # Save the score to the database
        QuizScore.objects.create(user=user, topic=topic, score=score)

        # Get the leaderboard
        leaderboard = QuizScore.objects.filter(topic=topic).order_by("-score")[:10]

        return render(request, 'education/leaderboard.html', {
            "user": user,
            "score": score,
            "total": len(quiz),
            "leaderboard": leaderboard,
            "topic": topic,
        })

def display_resources(request):
    """
    Displays the resources for the selected topic.
    """
    topic = request.session.get('topic')
    content = request.session.get('content')
    if not topic or not content:
        return redirect('input_topic')

    # Use the content stored in the session
    wiki_url = f"https://en.wikipedia.org/wiki/{topic.replace(' ', '_')}"
    summary = content[:500]
    details = content

    return render(request, 'education/display_resources.html', {
        'topic': topic,
        'summary': summary,
        'details': details,
        'url': wiki_url,
    })










import requests
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import QuizResult, Category

# Get quiz questions from Open Trivia Database based on a category or custom topic
def get_quiz_questions(category, difficulty, num_questions=5):
    url = f"https://opentdb.com/api.php?amount={num_questions}&category={category}&difficulty={difficulty}&type=multiple"
    response = requests.get(url)
    data = response.json()
    return data['results']

# Quiz View
@login_required
def quiz(request):
    if request.method == 'POST':
        # Handle quiz submission (calculate score)
        score = 0
        total_questions = len(request.POST.getlist('question_ids'))

        for i in range(total_questions):
            selected_answer = request.POST.get(f"answer_{i}")
            correct_answer = request.POST.get(f"correct_answer_{i}")

            if selected_answer == correct_answer:
                score += 1
        
        # Save the result in the database
        QuizResult.objects.create(user=request.user, score=score)
        return redirect('quiz_result')

    # Handle the form to choose a topic or enter custom one
    categories = Category.objects.all()  # Get predefined categories from database
    custom_topic = request.POST.get('custom_topic', '')  # Get custom topic input

    if custom_topic:
        # You can use a custom search or similar logic to get questions based on the entered topic
        # For simplicity, let's assume you can fetch a category ID by topic name (but the API doesn’t directly support custom topics)
        category = 9  # Replace with the correct category ID for a custom topic
        difficulty = request.POST.get('difficulty', 'easy')
        quiz_questions = get_quiz_questions(category, difficulty)
        return render(request, 'quiz/quiz_page.html', {'quiz_questions': quiz_questions, 'topic': custom_topic})

    return render(request, 'quiz/select_quiz.html', {'categories': categories})

# Quiz Result View
@login_required
def quiz_result(request):
    # Fetch user's score from the database
    results = QuizResult.objects.filter(user=request.user).order_by('-score')
    return render(request, 'quiz/quiz_result.html', {'results': results})

# Leaderboard View
@login_required
def leaderboard(request):
    leaderboard_results = QuizResult.objects.all().order_by('-score')
    return render(request, 'quiz/leaderboard.html', {'leaderboard_results': leaderboard_results})


# education/views.py

from django.shortcuts import render
from .models import QuizResult

# Add the results view
def results(request):
    # Fetch all quiz results from the database, ordered by score (descending)
    quiz_results = QuizResult.objects.all().order_by('-score')

    context = {
        'quiz_results': quiz_results
    }

    return render(request, 'education/results.html', context)



