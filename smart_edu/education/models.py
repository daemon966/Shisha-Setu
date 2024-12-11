from django.db import models
from django.contrib.auth.models import User

# Quiz Question Model
class QuizQuestion(models.Model):
    question = models.CharField(max_length=255)
    option_1 = models.CharField(max_length=255)
    option_2 = models.CharField(max_length=255)
    option_3 = models.CharField(max_length=255)
    option_4 = models.CharField(max_length=255)
    correct_option = models.CharField(max_length=255)
    topic = models.CharField(max_length=255)

    class Meta:
        unique_together = ['question', 'topic']

    def __str__(self):
        return self.question


# Quiz Score Model
class QuizScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.CharField(max_length=255)
    score = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'topic']

    def __str__(self):
        return f"{self.user.username} - {self.topic} - {self.score}"


# Leaderboard Model
class Leaderboard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    topic = models.CharField(max_length=255)

    class Meta:
        ordering = ['-score']

    def __str__(self):
        return f"{self.user.username} - {self.score}"


# Category Model
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# User Activity Log

from django.db import models
from django.contrib.auth.models import User

class UserActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    topic = models.CharField(max_length=255, null=True, blank=True)
    additional_info = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)



# Topic Popularity
class TopicPopularity(models.Model):
    topic = models.CharField(max_length=255, unique=True)
    search_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.topic} - {self.search_count}"


class QuizPerformanceSummary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    average_score = models.FloatField(default=0.0)
    total_quizzes = models.IntegerField(default=0)

    def update_performance(self):
        """Updates the user's performance summary."""
        quiz_scores = QuizScore.objects.filter(user=self.user)
        total_score = sum([score.score for score in quiz_scores])
        total_quizzes = quiz_scores.count()
        self.average_score = total_score / total_quizzes if total_quizzes else 0
        self.total_quizzes = total_quizzes
        self.save()

    def __str__(self):
        return f"{self.user.username} - Avg Score: {self.average_score} - Total Quizzes: {self.total_quizzes}"



# YouTube Search Log
class YouTubeSearchLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query = models.CharField(max_length=255)
    video_title = models.CharField(max_length=255)
    video_url = models.URLField()
    search_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} searched for '{self.query}'"


# Resource Search Log
class ResourceSearchLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.CharField(max_length=255)
    search_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} searched for {self.topic} at {self.search_timestamp}"


# Quiz Attempt Log
class QuizAttemptLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz_name = models.CharField(max_length=255)
    score = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} attempted {self.quiz_name} with score {self.score} at {self.timestamp}"


class QuizResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.score} points"
