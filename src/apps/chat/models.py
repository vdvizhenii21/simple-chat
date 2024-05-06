from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from .validators import ThreadValidators
from django.core.exceptions import ValidationError


class Thread(models.Model):
    participants = models.ManyToManyField(
        User,
        related_name="threads",
    )
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        participant_names = ", ".join(
            str(participant) for participant in self.participants.all()
        )
        return f"Thread with participants: {participant_names}"


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    thread = models.ForeignKey(
        Thread, on_delete=models.CASCADE, related_name="messages"
    )
    created = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender} in thread {self.thread}"
