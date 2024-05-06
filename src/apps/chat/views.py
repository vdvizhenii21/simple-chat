from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Thread, Message
from .pagination import PaginationMessages, PaginationThread
from .permissions import IsParticipant
from .serializers import ThreadSerializer, MessageSerializer
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied


class ThreadView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ThreadSerializer
    pagination_class = PaginationThread

    def get(self, request, *args, **kwargs):
        # Retrieve the list of threads for any user
        threads = Thread.objects.filter(participants=request.user)
        paginator = self.pagination_class()
        paginated_threads = paginator.paginate_queryset(threads, request)
        serializer = self.serializer_class(
            paginated_threads, many=True, context={"request": request}
        )
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, *args, **kwargs):
        participants = request.data.get("participants", [])

        # Check if a thread with particular users exists
        thread = (
            Thread.objects.filter(participants__in=participants)
            .annotate(num_participants=Count("participants"))
            .filter(num_participants=len(participants))
            .first()
        )

        if thread:
            serializer = self.serializer_class(thread)
            return Response(serializer.data)

        # Create a new thread if it doesn't exist
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        # Removing a thread
        thread_id = request.data.get("pk")
        thread = get_object_or_404(Thread, pk=thread_id)
        if request.user not in thread.participants.all():
            raise PermissionDenied("You don't have permission to delete this thread.")
        thread.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ThreadMessagesView(APIView):
    permission_classes = [IsParticipant, IsAuthenticated]
    pagination_class = PaginationMessages

    def get_thread(self, thread_id):
        try:
            return Thread.objects.get(id=thread_id)
        except Thread.DoesNotExist:
            return None

    def get(self, request):
        thread_id = request.data.get("thread_id")
        thread = self.get_thread(thread_id)
        if not thread:
            return Response(
                {"error": "Thread not found"}, status=status.HTTP_404_NOT_FOUND
            )

        unread_messages = thread.messages.exclude(sender=request.user).filter(
            is_read=False
        )
        if unread_messages:
            unread_messages.update(is_read=True)

        messages = thread.messages.all()
        paginator = self.pagination_class()
        paginated_messages = paginator.paginate_queryset(messages, request)
        serializer = MessageSerializer(paginated_messages, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        request_data = request.data.get("thread_id")
        thread = self.get_thread(request_data)
        if not thread:
            return Response(
                {"error": "Thread not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(thread=thread, sender=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
