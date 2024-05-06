from django.urls import path, include
from .views import ThreadView, ThreadMessagesView

urlpatterns = [
    path("threads/", ThreadView.as_view(), name="threads"),
    path("messages/", ThreadMessagesView.as_view(), name="messages"),
]
