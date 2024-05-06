from rest_framework import serializers
from .models import Thread, Message
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class ThreadSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all()
    )
    unread_messages_count = serializers.SerializerMethodField()

    class Meta:
        model = Thread
        fields = ["id", "participants", "created", "updated", "unread_messages_count"]

    def validate_participants(self, value):
        if len(value) > 2:
            raise ValidationError("Thread can only have 2 participants.")
        return value

    def validate(self, data):
        participants = data.get("participants", [])
        user = self.context["request"].user
        if user not in participants:
            raise ValidationError(
                "You can create a thread only with yourself as a participant."
            )
        return data

    def get_unread_messages_count(self, obj):
        user = self.context["request"].user
        if user:
            return obj.messages.exclude(sender=user).filter(is_read=False).count()
        return 0


class MessageSerializer(serializers.ModelSerializer):
    thread_id = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        model = Message
        fields = ["id", "sender", "text", "thread_id", "created", "is_read"]
        read_only_fields = ["id", "sender", "created", "is_read"]
