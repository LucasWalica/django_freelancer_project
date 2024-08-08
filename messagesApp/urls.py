from django.urls import path
from .views import (MessagesWithOtherView, InboxView)


urlpatterns = [
    path('inbox/', InboxView.as_view(), name='inbox'),
    path('messages/<int:pk1>/<int:pk2>/', MessagesWithOtherView.as_view(), name="messageWithOther"),
]
