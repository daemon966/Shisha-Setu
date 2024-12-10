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

    def __str__(self):
        return self.question

# User's Quiz Results
class UserQuizResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.CharField(max_length=255)
    score = models.IntegerField()
    total_questions = models.IntegerField()
    date_taken = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.topic} - {self.score}/{self.total_questions}"

# Leaderboard Model
class Leaderboard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    topic = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username} - {self.score}"

# Quiz Result Model
class QuizResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link the result to the user
    score = models.IntegerField()  # Store the score
    timestamp = models.DateTimeField(auto_now_add=True)  # Store the timestamp of the result

    def __str__(self):
        return f"{self.user.username} - {self.score} points"

# Category Model
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


from django.db import models

class QuizScore(models.Model):
    user = models.CharField(max_length=100)
    topic = models.CharField(max_length=100)
    score = models.IntegerField()

    def __str__(self):
        return f"{self.user} - {self.topic} - {self.score}"
