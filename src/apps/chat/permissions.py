from rest_framework.permissions import BasePermission
from .models import Thread


class IsParticipant(BasePermission):
    """
    Checking whether a user is a member of a trend.
    """

    def has_permission(self, request, view):
        thread_id = request.data.get("thread_id")
        if thread_id:
            try:
                thread = Thread.objects.get(id=thread_id)
                return request.user in thread.participants.all()
            except Thread.DoesNotExist:
                return False
        return False
